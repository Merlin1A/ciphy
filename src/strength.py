import string


class PasswordStrength:
    """
    A class for checking the strength of a password based on various criteria.

    Attributes
    ----------
    password : str
        The password to be checked for strength.
    """

    def __init__(self, password):
        """
        Initializes the PasswordStrengthChecker class.

        Parameters
        ----------
        password : str
            The password to be checked for strength.
        """
        self.password = password

    def __del__(self):
        """
        Destructor for the PasswordStrengthChecker class.

        Deletes sensitive variables when the object is no longer in use.
        """
        del self.password

    def get_password_strength(self):
        """
        Calculates the password strength score based on various criteria.

        Returns
        -------
        str
            The strength level of the password (Very Weak, Weak, Moderate, Strong, Very Strong).
        """
        score = 0

        # Length criteria
        length = len(self.password)
        if length >= 8:
            score += 2
        elif length >= 6:
            score += 1

        # Uppercase and lowercase letters criteria
        has_uppercase = any(char.isupper() for char in self.password)
        has_lowercase = any(char.islower() for char in self.password)
        if has_uppercase and has_lowercase:
            score += 2
        elif has_uppercase or has_lowercase:
            score += 1

        # Digits criteria
        has_digit = any(char.isdigit() for char in self.password)
        if has_digit:
            score += 1

        # Special characters criteria
        has_special_char = any(char in string.punctuation for char in self.password)
        if has_special_char:
            score += 2

        # Determine password strength level
        if score == 0:
            strength = "Very Weak"
        elif score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Moderate"
        elif score <= 6:
            strength = "Strong"
        else:
            strength = "Very Strong"

        return strength