# src/__init__.py
import os
import gc
import fire
import getpass
from cipher import AESCipher
from utils import read_config
from generator import PasswordGenerator


class PasswordManager:

   def __init__(self):
      config_data = read_config('config.yaml')

      self.encrypted_file_path = os.path.expanduser(config_data['encrypted_passwords_file_path'])
      self.file_path = os.path.expanduser(config_data['passwords_file_path'])
      self.password_generator = PasswordGenerator()
      self.AESCipher = AESCipher()
      
   def __del__(self):
      del self.password_generator
      del self.AESCipher
      gc.collect()

   def gen_pass(self, password_length=8, num_pseudo_words=1, num_passwords=1):
      passwords = list()

      for i in range(num_passwords):
         passwords.append(self.password_generator.generate_password(password_length, num_pseudo_words))
         
      return passwords
   
   def encrypt(self, in_filename=None, out_filename=None, override=True):
      """
      Encrypts the contents of a file using the AESCipher instance. The user is prompted
      to enter a password, which will be used for the encryption process. The encrypted 
      file can be saved to a new file or overwrite the original file, based on the 
      'override' parameter.

      Parameters
      ----------
      in_filename : str, optional
         The input file path to be encrypted. If not provided, the instance's file_path attribute will be used.

      out_filename : str, optional
         The output file path for the encrypted file. If not provided, the instance's encrypted_file_path attribute will be used.
      
      override : bool, optional
         Determines whether the encrypted content should overwrite the original file. Default is True.

      Returns
      ----------
      None
      """

      password = getpass.getpass("Enter your password: ")

      if not in_filename:
         in_filename = self.file_path

      if not out_filename:
         out_filename = self.encrypted_file_path
      
      self.AESCipher.encrypt_file(in_filename, out_filename, override, password)

   def decrypt(self, in_filename=None, out_filename=None):
      """
      Decrypts the contents of a file using the AESCipher instance. The user is prompted 
      to enter a password, which will be used for the decryption process. The decrypted 
      file can be saved to a new file or overwrite the original encrypted file.

      Parameters
      ----------
      in_filename : str, optional
         The input file path to be decrypted. If not provided, the instance's encrypted_file_path attribute will be used.
         
      out_filename : str, optional
         The output file path for the decrypted file. If not provided, the instance's file_path attribute will be used.

      Returns
      ----------
      None
      """
      password = getpass.getpass("Enter your password: ")

      if not in_filename:
         in_filename = self.encypted_file_path

      if not out_filename:
         out_filename = self.file_path

      self.AESCipher.decrypt_file(in_filename, out_filename, password)

   
def main():
    fire.Fire(PasswordManager)


main()

