"""
    Main purpose:
        User web interfaces.
"""

from abc import ABC, abstractmethod
from typing import List




class FastapiGuesser():
    """FastApi UI"""
    def ask_word(self, row: List[str]):
        """Ask a word to the user"""
        mot_etranger = row[1]
        return mot_etranger

    def return_translation(self, row: List[str]):
        """Return translation to the user"""
        mot_natal = row[2]
        return mot_natal

    def get_user_answer(self) -> bool:
        """Ask the user to decide if the answer was correct or not."""
        user_answer = "No"
        if user_answer == 'Yes':
            word_guessed = True
        if user_answer == 'No':
            word_guessed = False
        return word_guessed

    def guess_word(self, row: List[str], i: int, words: int):
        """Steps of the user's guessing process."""
        self.ask_word(row)
        self.return_translation(row)
        self.get_user_answer()



class Account(ABC):
    """
    Types of account:
    - developer
        o architect
        o developer
        o devops
        o tester
    - customer (paid version)
    - user (free version)
    - guest
    """

    @abstractmethod
    def log_in(self):
        """
        All user should be able to log in.
        The concrete method for the 'guest' account should have no effect.
        """

    @abstractmethod
    def log_out(self):
        """
        All users should be able to log out.
        The concrete method for the 'guest' account should have no effect.
        """



class UserAccount(Account):
    """Class dedicated to user accounts management."""

    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_passsword = user_password

    def create(self):
        """
        Create a user account and triggers the creation of the user's database.
        """
        return None

    def log_in(self):
        """Enable the user to log in to his account."""
        return None

    def log_out(self):
        """Enable the user to log out of his account."""
        return None

    def add_word(self):
        """Add a couple of words to the user's database."""
        return None

    def remove_word(self):
        """Remove a couple of words from the user's database."""
        return None

    def update_name(self):
        """Change the name of the user."""
        return None

    def update_password(self):
        """Change the password of the user."""
        return None

    def delete(self):
        """Delete the user account."""
        return None
