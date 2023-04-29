# ciphy/__init__.py
import os
import gc
import yaml
import fire
import getpass
from cipher import AESCipher
from generator import PasswordGenerator

def read_config(file_path):
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data

class PasswordManager:

   def __init__(self):
      config_data = read_config('config.yaml')

      self.file_path = os.path.expanduser(config_data['encrypted_passwords_file_path'])
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
   
   def encrypt(self, in_filename, out_filename=None, override=True):
      password = getpass.getpass("Enter your password: ")

      if not out_filename:
         out_filename = self.file_path
      
      self.AESCipher.encrypt_file(in_filename, out_filename, override, password)

   def decrypt(self, in_filename=None, out_filename=None):
      password = getpass.getpass("Enter your password: ")

      if not in_filename:
         in_filename = self.file_path

      self.AESCipher.decrypt_file(in_filename, out_filename, password)

   
def main():
    fire.Fire(PasswordManager)

main()

