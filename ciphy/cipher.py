import gc
import os
import struct
import hashlib
import secrets
from Crypto.Cipher import AES

class AESCipher:
    """
    A class for encrypting and decrypting files using AES 256.

    Attributes:
        key (bytes): The encryption key.

    Methods:
        __init__(self, key=None): Initializes the AESCipher object.
        _generate_key(self): Generates a new random encryption key.
        encrypt_file(self, in_filename, out_filename=None, chunksize=64*1024): Encrypts a file.
        decrypt_file(self, in_filename, out_filename=None, chunksize=24*1024): Decrypts a file.
        print_key(self): Prints the encryption key to stdout.
        save_key(self, filename): Saves the encryption key to a file.
    """

    def __init__(self, key=None):
        """
        Initializes the AESCipher object.

        Parameters
        ----------
        key (str) : 
            The encryption key as a hex string. If None, generates a new key.

        """
        if key is None:
            key = self._generate_key()
        self.key = hashlib.sha256(key.encode()).digest()

    def __del__(self):
        """
        Zero out memory.
        """
        del self.key
        gc.collect()

    def _generate_key(self):
        """
        Generates a new random encryption key.

        Returns
        ----------
        str
            A hex string representing the new encryption key.
        """
        return secrets.token_hex(32)

    def encrypt_file(self, in_filename, out_filename=None, chunksize=64*1024, override=True):
        """
        Encrypts a file using AES 256.

        Parameters
        ----------
        in_filename : str
            The input file path.
        out_filename : str
            The output file path. If None, replaces the file suffix with ".enc".
        chunksize : int 
            The size of the file chunks to read and write.
        override : bool 
            Whether to delete or override the existing encrypted file.

        Returns
        ----------
        None
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0] + '.enc'
            
        if not override:
            i = 1
            while os.path.exists(out_filename):
                out_filename = f"{os.path.splitext(in_filename)[0]}.enc.{i}"
                i += 1
        elif os.path.exists(out_filename):
            os.remove(out_filename)

        iv = os.urandom(16)
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))


    def decrypt_file(self, in_filename, out_filename=None, chunksize=24*1024):
        """
        Decrypts a file that was encrypted using AES 256.

        Parameters
        ----------
        in_filename : str 
            The input file path.
        out_filename : str
            The output file path. If None, removes the ".enc" extension from the input filename.
        chunksize : int
            The size of the file chunks to read and write.

        Returns
        ----------
        None
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            filesize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(self.key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(filesize)


    def print_key(self):
        """
        Prints the encryption key to stdout.
        """
        print(self.key.hex())

    def save_key_to_file(self, key, file_path):
        # Set umask to 0o077, which ensures the file will be created with secure permissions (rw-------, 0600)
        old_umask = os.umask(0o077)
        
        try:
            with open(file_path, "wb") as key_file:
                key_file.write(key)
        finally:
            # Restore the original umask
            os.umask(old_umask)

    def load_key(self, filename):
        """
        Loads an encryption key from a file.

        Parameters
        ----------
        filename : str 
            The name of the file containing the key.

        Returns
        ----------
        None
        """
        with open(filename, 'rb') as f:
            self.key = f.read()


