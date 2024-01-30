"""
    Creation date:
        28th December 2023
    Main purpose:
        Users management
"""

import json
import os
import sys
from abc import ABC, abstractmethod

from fastapi import HTTPException
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data.data_handler import DbManipulator, DbController



class CredChecker():
    """Class dedicated to the credentials checking process."""
    def __init__(self):
        self.name = ""
        self.password = ""
        self.db_controller = DbController(
            host='web_local'
        )

    def check_input_name(self, name_to_check):
        """Check if the input name belongs to the users list."""
        with open("conf/hum.json", "r") as hum_file:
            hum_dict = json.load(hum_file)
        hum_pwd = hum_dict['user']['root']['OK']
        users_list = self.db_controller.get_users_list(
            hum_pwd
        )
        if name_to_check in users_list:
            return True
        else:
            return False

    def check_input_password(self, user_name, password_to_check):
        """Check if the input password is correct."""
        secrets = {
            'benoit': "vive la vie",
            'Donald Trump': "Make America Great Again",
            'Caesar': "Veni, vidi, vici"
        }
        if password_to_check == secrets[user_name]:
            return True
        else:
            return False

    def flag_incorrect_user_name(self, name_to_check):
        """
        Raise exception if unknown user name, and redirect to sign-in page.
        """
        raise HTTPException(
            status_code=303,
            detail=f"Unknown user name: {name_to_check}.",
            headers={"Location": "/sign-in"}
        )

    def flag_incorrect_user_password(self, name_to_check, input_pwd):
        """
        Raise exception if wrong password, and redirect to sign-in page.
        """
        raise HTTPException(
            status_code=303,
            detail=f"Wrong password {input_pwd} for user {name_to_check}.",
            headers={"Location": "/sign-in"}
        )

    def check_user_name(self, name_to_check):
        """Validate user name."""
        if name_to_check in [None, ""]:
            logger.warning(f"Input name is empty or somewhat sneaky.")
            self.flag_incorrect_user_name()
        if not self.check_input_name(name_to_check):
            logger.warning(f"Input name {name_to_check} unknown.")
            self.flag_incorrect_user_name()
        logger.success(f"User name {name_to_check} valid.")

    def check_password(self, name_to_check, password_to_check):
        """Validate user password."""
        if password_to_check in [None, ""]:
            logger.warning(f"Input password is empty or somewhat sneaky.")
            self.flag_incorrect_user_password(name_to_check, password_to_check)
        if not self.check_input_password(name_to_check, password_to_check):
            logger.warning(f"Input password '{password_to_check}' incorrect.")
            self.flag_incorrect_user_password(name_to_check, password_to_check)
        logger.success(f"Password valid.")

    def check_credentials(self, name_to_check, password_to_check):
        """Validate user credentials."""
        self.check_user_name(name_to_check)
        self.check_password(name_to_check, password_to_check)
        logger.success(f"Access granted.")



class Account(ABC):
    """
    Types of account:
    - guest
    - user (free version)
    - customer (paid version)
    - developer
        o architect
        o developer
        o tester
        o ops
    """
    def __init__(self):
        self.account_types = [
            'guest',
            'user',
            'customer',
            'developer'
        ]

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

    def create_account(self, type_of_account='user'):
        """
        Acquire name and password, and store them in the credentials.
        """
        account_exists = self.check_if_account_exists()
        if account_exists:
            return 1
        db_handler = DbController(host='web_local')
        with open("conf/hum.json", "r") as hum_file:
            hum_dict = json.load(hum_file)
        hum_pwd = hum_dict['user']['root']['OK']
        db_handler.create_user(
            root_password=hum_pwd,
            user_name=self.user_name,
            user_password=self.user_passsword
        )
        return 0

    def check_if_account_exists(self):
        db_handler = DbController(host='web_local')
        with open("conf/hum.json", "r") as hum_file:
            hum_dict = json.load(hum_file)
        hum_pwd = hum_dict['user']['root']['OK']
        users_list = db_handler.get_users_list(
            hum_pwd
        )
        if self.user_name in users_list:
            logger.error(f"User name {self.user_name} already exists.")
            return True
        else:
            logger.success(f"User name {self.user_name} is available.")
            return False

    def delete(self):
        """
        Delete the user account.
        """
        return None

    def log_in(self):
        """
        Enable the user to log in to his account.
        """
        return None

    def log_out(self):
        """
        Enable the user to log out of his account.
        """
        return None

    def update_name(self):
        """
        Change the name of the user.
        """
        return None

    def update_password(self):
        """
        Change the password of the user.
        """
        return None

    def create_database(self):
        """
        Add a database to the user's space.
        """
        return None

    def remove_database(self):
        """
        Remove a database from the user's space.
        """
        return None

    def insert_word(self):
        """
        Add a couple of words to the user's database.
        """
        return None

    def remove_word(self):
        """
        Remove a couple of words from the user's database.
        """
        return None
