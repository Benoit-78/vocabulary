"""
    Creation date:
        28th December 2023
    Main purpose:
        Users management
"""

from abc import ABC, abstractmethod

from fastapi import HTTPException
from loguru import logger


class CredChecker():
    """Class dedicated to the credentials checking process."""
    def __init__(self):
        self.name = ""
        self.password = ""

    def check_input_name(self):
        """Check if the input name belongs to the users list."""
        if self.name in ['benoit', 'Donald Trump', 'Caesar']:
            return True
        else:
            return False

    def check_input_password(self):
        """Check if the input password is correct."""
        secrets = {
            'benoit': "vive la vie",
            'Donald Trump': "Make America Great Again",
            'Caesar': "Veni, vidi, vici"
        }
        if self.password == secrets[self.name]:
            return True
        else:
            return False

    def flag_incorrect_user_name(self):
        """
        Raise exception if unknown user name, and redirect to sign-in page.
        """
        raise HTTPException(
            status_code=303,
            detail=f"Unknown user name: {self.name}.",
            headers={"Location": "/sign-in"}
        )

    def flag_incorrect_user_password(self):
        """
        Raise exception if wrong password, and redirect to sign-in page.
        """
        raise HTTPException(
            status_code=303,
            detail=f"Wrong password {self.password} for user {self.name}.",
            headers={"Location": "/sign-in"}
        )

    def check_credentials(self, name_to_check):
        """Validate user credentials."""
        # Input name is different from the user name.
        if name_to_check != self.name:
            self.flag_incorrect_user_name()
        # Given user name is not in the list of users.
        if not self.check_input_name():
            self.flag_incorrect_user_name()
        # Input password is empty or sneaky.
        if self.password in [None, ""]:
            self.flag_incorrect_user_password()
        # Input password is different from the user password.
        if not self.check_input_password():
            self.flag_incorrect_user_password()



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
    """
    Interface between web_app API and database handlers,
    such as Controller, Definer, and Manipulator.
    """
    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_passsword = user_password
        self.db_handler = MariaDBHandler(
            self.user_name,
            test_type='version',
            mode='web_local',
            language_1='english'
        )

    def create(self):
        """
        Acquire name and password, and store them in the credentials.
        """
        return None

    def delete(self):
        """Delete the user account."""
        return None

    def log_in(self):
        """Enable the user to log in to his account."""
        return None

    def log_out(self):
        """Enable the user to log out of his account."""
        return None

    def update_name(self):
        """Change the name of the user."""
        return None

    def update_password(self):
        """Change the password of the user."""
        return None

    def add_database(self):
        """Add a database to the user's space."""
        return None

    def remove_database(self):
        """Remove a database from the user's space."""
        return None

    def add_word(self):
        """Add a couple of words to the user's database."""
        return None

    def remove_word(self):
        """Remove a couple of words from the user's database."""
        return None