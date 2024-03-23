"""
    Creation date:
        28th December 2023
    Main purpose:
        Users management
"""

import os
import sys
from abc import ABC, abstractmethod
from dotenv import load_dotenv

from fastapi import HTTPException
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data.data_handler import DbController, DbDefiner, DbManipulator
from src.api import authentication as auth_api

load_dotenv()
DB_ROOT_PWD = os.getenv('VOC_DB_ROOT_PWD')



class CredChecker():
    """Class dedicated to the credentials checking process."""
    def __init__(self):
        self.name = ""
        self.password = ""
        self.db_controller = DbController()

    def check_input_name(self, name_to_check):
        """Check if the input name belongs to the users list."""
        users_list = self.db_controller.get_users_list_from_mysql()
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
        return bool(password_to_check == secrets[user_name])

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
        super().__init__()
        self.user_name = user_name
        self.user_password = user_password

    def create_account(self):
        """
        Acquire name and password, and store them in the credentials.
        """
        account_exists = self.check_if_account_exists()
        if account_exists:
            return False
        db_controller = DbController()
        logger.debug(f"User password: {self.user_password}")
        hash_password = auth_api.get_password_hash(self.user_password)
        logger.debug(f"Hash password: {hash_password}")
        db_controller.create_user_in_mysql(self.user_name, hash_password)
        logger.debug("User created in mysql")
        db_controller.grant_privileges_on_common_database(self.user_name)
        logger.debug("User granted privileges on common database")
        return True

    def check_if_account_exists(self):
        """
        Check if the account exists.
        """
        db_controller = DbController()
        users_list = db_controller.get_users_list_from_mysql()
        if self.user_name in users_list:
            logger.error(f"User name '{self.user_name}' already exists.")
            return True
        users_list = db_controller.get_users_list()
        users_list = [element['username'] for element in users_list]
        if self.user_name in users_list:
            logger.error(f"User name '{self.user_name}' already exists.")
            return True
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
        db_definer = DbDefiner(self.user_name)
        db_created = db_definer.create_database(
            DB_ROOT_PWD,
            db_name
        )
        if not db_created:
            return 1
        db_controller = DbController()
        db_controller.grant_privileges(self.user_name, db_name)
        tables_created = db_definer.create_seven_tables(self.user_password, db_name)
        if not tables_created:
            logger.error(f"Error with the creation of tables for {db_name}.")
            return 1
        return True

    def check_if_database_exists(self, db_name):
        """
        Check if the user's database already exists.
        """
        db_definer = DbDefiner(self.user_name)
        db_names = db_definer.get_user_databases(DB_ROOT_PWD)
        sql_db_name = self.user_name + '_' + db_name
        if sql_db_name in db_names:
            logger.error(f"Database name {db_name} already exists.")
            return True
        logger.success(f"Database name {db_name} is available.")
        return False

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
        db_manipulator = DbManipulator(
            self.user_name,
            db_name,
            'version',
        )
        result = db_manipulator.insert_word(
            self.user_password,
            [foreign, native]
        )
        return result

    def remove_word(self):
        """
        Remove a couple of words from the user's database.
        """
        return None
