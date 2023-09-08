import os
import struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def zero_fill(byte_var):
    """
    Fill a bytes or bytearray object with zeros.

    Parameters
    ----------
    byte_var : bytes or bytearray
        The variable to fill with zeros.
    """
    for i in range(len(byte_var)):
        byte_var[i] = 0


def encrypt_file(in_filename, out_filename=None, override=True, password=None):
    """
    Encrypts a file using AES-GCM with a password-based key derivation function.

    Parameters
    ----------
    in_filename : str
        The input file path.
    out_filename : str, optional
        The output file path. If None, replaces the file suffix with ".enc".
    override : bool, optional
        Whether to delete or override the existing encrypted file (default: True).
    password : str
        The password used for key derivation.

    Raises
    ------
    ValueError
        If parameters are of invalid types.
    FileNotFoundError
        If input file is not found.
    FileExistsError
        If output file already exists and override is set to False.
    """
    if not isinstance(in_filename, str) or not isinstance(password, str):
        raise ValueError("Filename and password must be strings.")

    if out_filename and not isinstance(out_filename, str):
        raise ValueError("Output filename must be a string.")

    if not os.path.exists(in_filename):
        raise FileNotFoundError(f"{in_filename} not found.")

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0] + '.enc'

    if not override and os.path.exists(out_filename):
        raise FileExistsError(f"{out_filename} already exists.")

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

    try:
        with open(in_filename, 'rb') as infile:
            data = infile.read()
            ciphertext = aesgcm.encrypt(nonce, data, None)
            with open(out_filename, 'wb') as outfile:
                outfile.write(b"V1")  # Version of the file format
                outfile.write(struct.pack(">I", 100000))  # Number of PBKDF2 iterations, as a 4-byte big-endian integer
                outfile.write(nonce)
                outfile.write(salt)
                outfile.write(ciphertext)

    except Exception as e:
        raise e
    finally:
        zero_fill(derived_key)


def decrypt_file(in_filename, out_filename=None, password=None):
    """
    Decrypts a file that was encrypted using AES-GCM.

    Parameters
    ----------
    in_filename : str
        The input file path.
    out_filename : str, optional
        The output file path. If None, removes the ".enc" extension.
    password : str
        The password used for key derivation.

    Raises
    ------
    ValueError
        If parameters are of invalid types.
    FileNotFoundError
        If input file is not found.
    """
    if not isinstance(in_filename, str) or not isinstance(password, str):
        raise ValueError("Filename and password must be strings.")

    if out_filename and not isinstance(out_filename, str):
        raise ValueError("Output filename must be a string.")

    if not os.path.exists(in_filename):
        raise FileNotFoundError(f"{in_filename} not found.")

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    try:
        with open(in_filename, 'rb') as infile:
            version = infile.read(2)
            if version != b"V1":
                raise ValueError("Unsupported file version.")
                
            iterations = struct.unpack(">I", infile.read(4))[0]
            nonce = infile.read(12)
            salt = infile.read(16)
            ciphertext = infile.read()

            backend = default_backend()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=iterations,
                backend=backend
            )
            derived_key = kdf.derive(password.encode())
            aesgcm = AESGCM(derived_key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            with open(out_filename, 'wb') as outfile:
                outfile.write(plaintext)
    except Exception as e:
        raise e
    finally:
        zero_fill(derived_key)
