import secrets
import string
import yaml
import gc

class WordGenerator:
    """
    A class to generate pseudo-words using predefined components.

    Attributes
    ----------
    initial_consonants : list
        A list of characters representing possible initial consonants.
    final_consonants : list
        A list of characters representing possible final consonants.
    vowels : list
        A list of characters representing possible vowels.

    Methods
    -------
    generate_word(word_length, start_vowel=False, end_vowel=False)
        Generates a pseudo-word of the specified length.
    generate_words(wordcount=1, word_length=None)
        Generates a list of pseudo-words with the specified count and length.
    """

    def __init__(self, component_file='components.yaml'):
        """
        Constructs a WordGenerator object and loads components from a YAML file.

        Parameters
        ----------
        component_file : str, optional
            A string representing the path to the YAML file containing components.
        """
        with open(component_file) as f:
            components = yaml.safe_load(f)

        self.initial_consonants = list(set(string.ascii_lowercase) - set('aeiou') - set('qxc') | set(''.join(components['initials'])))
        self.final_consonants = list(set(string.ascii_lowercase) - set('aeiou') - set('qxcsj') | set(''.join(components['finals'])))
        self.vowels = list(set(''.join(components['vowels'])))

    def __del__(self):
        """
        Destructor for the WordGenerator class.

        Deletes variables when the object is no longer in use.
        """
        del self.initial_consonants
        del self.final_consonants
        del self.vowels


    def generate_word(self, word_length, start_vowel=False, end_vowel=False):
        """
        Generates a pseudo-word of the specified length.

        Parameters
        ----------
        word_length : int
            The length of the pseudo-word to be generated.
        start_vowel : bool, optional
            If True, the generated word will start with a vowel; otherwise, it will start with a consonant (default is False).
        end_vowel : bool, optional
            If True, the generated word will end with a vowel; otherwise, it will end with a consonant (default is False).

        Returns
        -------
        str
            The generated pseudo-word of the specified length.
        """
        letter_list = []
        if not start_vowel:
            letter_list.append(secrets.choice(self.initial_consonants))
            word_length -= 1

        while len(letter_list) < word_length:
            letter_list.append(secrets.choice(self.vowels))
            if len(letter_list) < word_length:
                letter_list.append(secrets.choice(self.final_consonants))

        if end_vowel and not letter_list[-1] in self.vowels:
            letter_list[-1] = secrets.choice(self.vowels)

        generated_word = ''.join(letter_list)

        # Zero out memory
        del letter_list
        del word_length
        del start_vowel
        del end_vowel
        gc.collect()

        return generated_word

class PasswordGenerator:
    """
    A class for generating secure passwords made of pseudo words, symbols, and numbers.
    
    Attributes
    ----------
    word_generator : WordGenerator
        An instance of the WordGenerator class for generating pseudo words.
    symbols : str
        A string containing punctuation symbols.
    digits : str
        A string containing digits from 0 to 9.
    """
    
    def __init__(self, component_file='components.yaml'):
        """
        Initializes the PasswordGenerator class.

        Parameters
        ----------
        component_file : str, optional
            The path to the file containing word components (default is 'components.yaml').
        """
        self.word_generator = WordGenerator(component_file)
        self.symbols = string.punctuation
        self.digits = string.digits

    def __del__(self):
        """
        Destructor for the PasswordGenerator class.

        Deletes variables when the object is no longer in use.
        """
        del self.word_generator
        del self.symbols
        del self.digits

    def generate_password(self, password_length, num_pseudo_words):
        """
        Generates a secure password made of pseudo words, symbols, and numbers.

        Parameters
        ----------
        password_length : int
            The desired length of the password, up to 40.
        num_pseudo_words : int
            The number of pseudo words to be generated.

        Returns
        -------
        str
            The generated secure password.
        """
        if password_length > 40:
            password_length = 40
        elif password_length < 0:
            password_length = 0

        min_word_length = max(1, password_length // num_pseudo_words)
        pseudo_words = [self.word_generator.generate_word(min_word_length) for _ in range(num_pseudo_words)]

        remaining_length = password_length - sum([len(pw) for pw in pseudo_words])
        extra_characters = [secrets.choice(self.symbols + self.digits) for _ in range(remaining_length)]

        combined = []
        for i in range(len(pseudo_words)):
            combined.append(pseudo_words[i])
            if i < len(extra_characters):
                combined.append(extra_characters[i])

        if password_length > 0 and secrets.randbelow(2):  # Randomly add symbol or digit at the beginning
            combined.insert(0, secrets.choice(self.symbols + self.digits))
            if len(combined) > password_length:
                combined.pop()

        if password_length > 0 and secrets.randbelow(2):  # Randomly add symbol or digit at the end
            combined.append(secrets.choice(self.symbols + self.digits))
            if len(combined) > password_length:
                combined.pop()

        return ''.join(combined)
