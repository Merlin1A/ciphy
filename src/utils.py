import os
import csv
import yaml

def load_passwords(filename):
    """
    Loads a list of passwords from a file.

    Parameters
    ----------
    filename : str
        The name of the file containing the passwords.

    Returns
    ----------
    list
        A list of passwords read from the file.
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        passwords = list(reader)
    return passwords

def read_config(file_path):
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data

def set_secure_permissions(file_path: str):
    """Sets secure file permissions (readable and writable only by the owner)."""
    os.chmod(file_path, 0o600)
