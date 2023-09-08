import os
import gc
import fire
import getpass
from utils import read_config, set_secure_permissions 
from generator import PasswordGenerator  
from cipher import encrypt_file, decrypt_file  
from typing import List


class PasswordManager:
    """Manages password generation, encryption, and decryption."""

    def __init__(self):
        """Initializes the PasswordManager."""
        config_data = read_config('config.yaml')
        self.encrypted_file_path = os.path.expanduser(config_data['encrypted_passwords_file_path'])
        self.file_path = os.path.expanduser(config_data['passwords_file_path'])
        self.password_generator = PasswordGenerator()

    def generate_passwords(self, password_length: int = 8, num_pseudo_words: int = 1, num_passwords: int = 1) -> List[str]:
        """
        Generates a list of passwords.

        Parameters:
        - password_length (int): The length of each password.
        - num_pseudo_words (int): The number of pseudo-words to use.
        - num_passwords (int): The number of passwords to generate.

        Returns:
        - List[str]: A list of generated passwords.
        """
        return [self.password_generator.generate_password(password_length, num_pseudo_words)
                for _ in range(num_passwords)]

    def encrypt(self, in_filename: str = None, out_filename: str = None, override: bool = True):
        """
        Encrypts a file with AES encryption.

        Parameters:
        - in_filename (str): The path of the input file. Defaults to self.file_path.
        - out_filename (str): The path of the output file. Defaults to self.encrypted_file_path.
        - override (bool): Whether to override the input file. Defaults to True.
        """
        password = getpass.getpass("Enter your password: ")

        if not in_filename:
            in_filename = self.file_path
        if not out_filename:
            out_filename = self.encrypted_file_path

        encrypt_file(in_filename, out_filename, override, password)
        set_secure_permissions(out_filename)

    def decrypt(self, in_filename: str = None, out_filename: str = None):
        """
        Decrypts a file with AES encryption.

        Parameters:
        - in_filename (str): The path of the input file. Defaults to self.encrypted_file_path.
        - out_filename (str): The path of the output file. Defaults to self.file_path.
        """
        password = getpass.getpass("Enter your password: ")

        if not in_filename:
            in_filename = self.encrypted_file_path
        if not out_filename:
            out_filename = self.file_path

        decrypt_file(in_filename, out_filename, password)
        set_secure_permissions(out_filename)


def main():
    """Entry point for the Fire CLI."""
    fire.Fire(PasswordManager)


if __name__ == "__main__":
    main()


