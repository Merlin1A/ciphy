import gc
import os
import struct
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class AESCipher:
    """
    A class for encrypting and decrypting files using AES-GCM.

    Methods:
        encrypt_file(self, in_filename, out_filename=None, password=None): Encrypts a file.
        decrypt_file(self, in_filename, out_filename=None, password=None): Decrypts a file.
        load_password(self, filename): Loads a password from a file.
    """

    def __init__(self):
        """
        Initializes the AESCipher object.
        """
        pass

    def __del__(self):
        """
        Cleans up the AESCipher object.
        """
        pass

    def encrypt_file(self, in_filename, out_filename=None, override=True, password=None):
        """
        Encrypts a file using AES-GCM with a password-based key derivation function.

        Parameters
        ----------
        in_filename : str
            The input file path.
        out_filename : str, optional
            The output file path. If None, replaces the file suffix with ".enc" (default: None).
        override : bool, optional
            Whether to delete or override the existing encrypted file (default: True).
        password : str
            The password used for key derivation.

        Returns
        -------
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

        salt = os.urandom(16)
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )

        derived_key = kdf.derive(password.encode())
        aesgcm = AESGCM(derived_key)
        nonce = os.urandom(12)
        with open(in_filename, 'rb') as infile:
            data = infile.read()
            ciphertext = aesgcm.encrypt(nonce, data, None)
            with open(out_filename, 'wb') as outfile:
                outfile.write(nonce)
                outfile.write(salt)
                outfile.write(ciphertext)

    def decrypt_file(self, in_filename, out_filename=None, password=None):
        """
        Decrypts a file that was encrypted using AES-GCM.

        Parameters
        ----------
        in_filename : str 
            The input file path.
        out_filename : str
            The output file path. If None, removes the ".enc" extension from the input filename.
        password : str
            The password used for key derivation.

        Returns
        ----------
        None
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            nonce = infile.read(12)
            salt = infile.read(16)
            ciphertext = infile.read()

            backend = default_backend()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=backend
            )

            derived_key = kdf.derive(password.encode())
            aesgcm = AESGCM(derived_key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)

            with open(out_filename, 'wb') as outfile:
                outfile.write(plaintext)

    def load_password(self, filename):
        """
        Loads a password from a file.

        Parameters
        ----------
        filename : str
            The name of the file containing the password.

        Returns
        ----------
        str
            The password read from the file.
        """
        with open(filename, 'r') as f:
            password = f.read()
        return password


    