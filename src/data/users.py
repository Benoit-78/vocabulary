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
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data.data_handler import DbController, DbDefiner, DbManipulator 



class CredChecker():
    """Class dedicated to the credentials checking process."""
    def __init__(self):
        self.name = ""
        self.password = ""
        self.db_controller = DbController(
            host='localhost'
        )

    def check_input_name(self, name_to_check):
        """Check if the input name belongs to the users list."""
        users_list = self.db_controller.get_users_list()
        if name_to_check in users_list:
            return True
        return False

    def check_input_password(self, user_name, password_to_check):
        """Check if the input password is correct."""
        secrets = {
            'benoit': "vive la vie",
            'Donald Trump': "Make America Great Again",
            'Caesar': "Veni, vidi, vici",
            'usr': 'pwd'
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
            logger.warning("Input name is empty or somewhat sneaky.")
            self.flag_incorrect_user_name(name_to_check)
        if not self.check_input_name(name_to_check):
            logger.warning(f"Input name {name_to_check} unknown.")
            self.flag_incorrect_user_name(name_to_check)

    def check_password(self, name_to_check, password_to_check):
        """Validate user password."""
        if password_to_check in [None, ""]:
            logger.warning("Input password is empty or somewhat sneaky.")
            self.flag_incorrect_user_password(name_to_check, password_to_check)
        if not self.check_input_password(name_to_check, password_to_check):
            logger.warning(f"Input password '{password_to_check}' incorrect.")
            self.flag_incorrect_user_password(name_to_check, password_to_check)
        logger.success("Password valid.")

    def check_credentials(self, name_to_check, password_to_check):
        """Validate user credentials."""
        self.check_user_name(name_to_check)
        self.check_password(name_to_check, password_to_check)
        logger.success(f"Access granted for {name_to_check}.")



class Account(ABC):
    """
    Types of account:
    - guest
    - user (free version)
    - customer (paid version)
    - developer : architect, developer, tester and ops
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
        self.user_password = user_password

    def create_account(self):
        """
        Acquire name and password, and store them in the credentials.
        """
        for host in ['localhost']:  # '%' has been removed from the list
            account_exists = self.check_if_account_exists(host)
            if account_exists:
                return 1
            db_controller = DbController(host=host)
            db_controller.create_user(self.user_name, self.user_password)
            db_controller.grant_privileges_on_common_database(self.user_name)
        return 0

    def check_if_account_exists(self, host):
        db_controller = DbController(host=host)
        users_list = db_controller.get_users_list()
        if self.user_name in users_list:
            logger.error(f"User name '{self.user_name}' already exists.")
            return True
        else:
            logger.success(f"User name '{self.user_name}' is available.")
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

    def create_database(self, db_name):
        """
        Add a database to the user's space.
        """
        # Bad path
        account_exists = self.check_if_database_exists(db_name)
        if account_exists:
            return 1
        # Create database
        with open("conf/hum.json", "r") as hum_file:
            hum_dict = json.load(hum_file)
        hum_pwd = hum_dict['user']['root']['OK']
        for host in ['localhost']:  # '%' has been removed from the list
            db_definer = DbDefiner(host, self.user_name)
            db_created = db_definer.create_database(
                hum_pwd,
                self.user_password,
                db_name
            )
            if not db_created:
                return 1
            db_controller = DbController(host)
            db_controller.grant_privileges(self.user_name, db_name)
            tables_created = db_definer.create_seven_tables(self.user_password, db_name)
            if not tables_created:
                logger.error(f"Error with the creation of tables for {db_name}.")
                return 1
            return 0

    def check_if_database_exists(self, db_name):
        """
        Check if the user's database already exists.
        """
        with open("conf/hum.json", "r") as hum_file:
            hum_dict = json.load(hum_file)
        hum_pwd = hum_dict['user']['root']['OK']
        for host in ['localhost']:  # '%' has been removed from the list
            db_definer = DbDefiner('localhost', self.user_name)
            db_names = db_definer.get_user_databases(hum_pwd, self.user_password)
            sql_db_name = self.user_name + '_' + db_name
            if sql_db_name in db_names:
                logger.error(f"Database name {db_name} already exists.")
                return True
            else:
                logger.success(f"Database name {db_name} is available.")
                return False

    def rename_database(self, old_name, new_name):
        """
        Change the name of the user's database.
        """
        # Copy the database
        # Transfer the privileges to the new database
        # Remove the old database
        return None

    def remove_database(self):
        """
        Remove a database from the user's space.
        """
        # Remove database
        # Remove privileges of the user on the database (they're not removed automatically)
        return None

    def insert_word(self, db_name, foreign, native):
        """
        Add a couple of words to the user's database.
        """
        for host in ['localhost']:  # '%' has been removed from the list
            db_manipulator = DbManipulator(
                'localhost',    
                self.user_name,
                db_name,
                'version',
            )
            result = db_manipulator.insert_word(
                self.user_password,
                [foreign, native]
            )
            return 0

    def remove_word(self):
        """
        Remove a couple of words from the user's database.
        """
        return None
