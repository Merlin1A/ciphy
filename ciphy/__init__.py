# ciphy/__init__.py
import gc
import yaml
import fire
import getpass
from cipher import AESCipher
from generator import PasswordGenerator

class PasswordManager:

   def __init__(self):
      self.password_generator = PasswordGenerator()
      self.AESCipher = AESCipher()

   def __del__(self):
      del self.password_generator
      del self.AESCipher
      del self.password
      gc.collect()

   def gen_pass(self, password_length=8, num_pseudo_words=1, num_passwords=1):
      passwords = list()

      for i in range(num_passwords):
         passwords.append(self.password_generator.generate_password(password_length, num_pseudo_words))
         
      return passwords
   
   def encrypt(self, in_filename, out_filename=None, override=True):
      password = getpass.getpass("Enter your password: ")
      
      self.AESCipher.encrypt_file(in_filename, out_filename, override, password)
    

   def decrypt(self, in_filename, out_filename=None):
      password = getpass.getpass("Enter your password: ")

      self.AESCipher.decrypt_file(in_filename, out_filename, password)

   
def main():
    fire.Fire(PasswordManager)

