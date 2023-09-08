import secrets
import string
import yaml


class WordGenerator:
    """
    A class to generate pseudo-words using predefined components.
    """

    def __init__(self, component_file='components.yaml'):
        """
        Initialize and load components from a YAML file.

        Parameters
        ----------
        component_file : str
            The path to the file containing word components.
        """
        try:
            with open(component_file, 'r') as f:
                components = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"File {component_file} not found.")
            return
        except yaml.YAMLError:
            print("Invalid YAML file.")
            return

        self.rng = secrets.SystemRandom()
        self.initial_consonants = bytearray(components['initials'], 'utf-8')
        self.final_consonants = bytearray(components['finals'], 'utf-8')
        self.vowels = bytearray(components['vowels'], 'utf-8')

    def generate_word(self, word_length, start_vowel=False, end_vowel=False):
        """
        Generate a pseudo-word of the specified length.

        Parameters
        ----------
        word_length : int
            The length of the pseudo-word to be generated.
        start_vowel : bool, optional
            If True, the generated word will start with a vowel.
        end_vowel : bool, optional
            If True, the generated word will end with a vowel.

        Returns
        -------
        str
            The generated pseudo-word.
        """
        if word_length <= 0:
            return ""

        letters = bytearray()
        if start_vowel:
            letters.append(self.rng.choice(self.vowels))
        else:
            letters.append(self.rng.choice(self.initial_consonants))

        for _ in range(1, word_length):
            if len(letters) % 2 == 0:
                letters.append(self.rng.choice(self.initial_consonants))
            else:
                letters.append(self.rng.choice(self.vowels))

        if end_vowel:
            letters[-1] = self.rng.choice(self.vowels)

        word = letters.decode('utf-8')

        # Zero out the byte array
        for i in range(len(letters)):
            letters[i] = 0

        return word


class PasswordGenerator:
    """
    A class for generating secure passwords made of pseudo words, symbols, and numbers.
    
    Attributes
    ----------
    word_generator : WordGenerator
        An instance of the WordGenerator class for generating pseudo words.
    symbols : bytearray
        A bytearray containing punctuation symbols.
    digits : bytearray
        A bytearray containing digits from 0 to 9.
    """

    def __init__(self, component_file='components.yaml'):
        """
        Initializes the PasswordGenerator class.

        Parameters
        ----------
        component_file : str, optional
            The path to the file containing word components (default is 'components.yaml').
        """
        self.rng = secrets.SystemRandom()
        self.word_generator = WordGenerator(component_file)
        self.symbols = bytearray(string.punctuation, 'utf-8')
        self.digits = bytearray(string.digits, 'utf-8')

    def generate_password(self, password_length, num_pseudo_words):
        """
        Generates a secure password made of pseudo words, symbols, and numbers.

        Parameters
        ----------
        password_length : int
            The desired length of the password.
        num_pseudo_words : int
            The number of pseudo words to include in the password.

        Returns
        -------
        str
            The generated secure password.
        """
        if password_length < 1:
            return ""

        min_word_length = max(1, password_length // num_pseudo_words)
        pseudo_words = [self.word_generator.generate_word(min_word_length).encode('utf-8') for _ in range(num_pseudo_words)]
        
        remaining_length = password_length - sum([len(pw) for pw in pseudo_words])
        extra_characters = [self.rng.choice(self.symbols + self.digits) for _ in range(remaining_length)]

        combined = bytearray()
        for i in range(len(pseudo_words)):
            combined.extend(pseudo_words[i])
            if i < len(extra_characters):
                combined.append(extra_characters[i])

        if len(combined) < password_length:
            combined.append(self.rng.choice(self.symbols + self.digits))

        # Truncate or pad to meet the required password length
        while len(combined) < password_length:
            combined.append(self.rng.choice(self.symbols + self.digits))

        while len(combined) > password_length:
            del combined[-1]

        password = combined.decode('utf-8')

        # Zero out sensitive byte arrays
        for i in range(len(combined)):
            combined[i] = 0

        for pw in pseudo_words:
            for i in range(len(pw)):
                pw[i] = 0

        for i in range(len(extra_characters)):
            extra_characters[i] = 0

        return password
