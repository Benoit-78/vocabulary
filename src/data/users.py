"""
    Creation date:
        28th December 2023
    Main purpose:
        Users management
"""

from abc import ABC, abstractmethod

from fastapi import HTTPException



def check_input_name(input_name):
    """Check if the input name belongs to the users list."""
    if input_name in ['benoit', 'Donald Trump', 'Caesar']:
        return True
    else:
        return False


def check_input_password(input_name, input_password):
    """Check if the input password is correct."""
    secrets = {
        'benoit': "vive la vie",
        'Donald Trump': "Make America Great Again",
        'Caesar': "Veni, vidi, vici"
    }
    if input_password == secrets[input_name]:
        return True
    else:
        return False


def check_credentials(input_name, input_password):
    """Validate user credentials."""
    if not check_input_name(input_name):
        raise HTTPException(
            status_code=303,
            detail="Unknown user name",
            headers={"Location": "/sign-in"}
        )
    if not check_input_password(input_name, input_password):
        raise HTTPException(
            status_code=303,
            detail="Wrong password",
            headers={"Location": "/sign-in"}
        )




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
