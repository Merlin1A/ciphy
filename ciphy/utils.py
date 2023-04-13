import csv

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
