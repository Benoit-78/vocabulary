"""
    Creation date:
        28th December 2023
    Main purpose:
        Users management
"""

from abc import ABC, abstractmethod
from typing import List

from dotenv import load_dotenv
from loguru import logger

from src.data.database_interface import DbController, DbDefiner, DbManipulator
from src.api import authentication as auth_api

load_dotenv()


class Account(ABC):
    """
    Types of account:
    - guest
    - user (free version)
    - customer (paid version)
    - contributor:
        - architect,
        - developer,
        - tester,
        - Ops (maintenance, monitoring, etc.)
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
    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name

    def create_account(self, password: str) -> bool:
        """
        Acquire name and password, and store them in the credentials.
        """
        account_exists = self.check_if_account_exists()
        if account_exists:
            return False
        hash_password = auth_api.get_password_hash(password=password)
        db_controller = DbController()
        db_controller.create_user_in_mysql(
            user_name=self.user_name,
            user_password=hash_password
        )
        db_controller.grant_privileges_on_common_database(
            user_name=self.user_name
        )
        db_controller.add_user_to_users_table(
            user_name=self.user_name,
            hash_password=hash_password
        )
        return True

    def check_if_account_exists(self) -> bool:
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
        return False

    def delete(self):
        """
        Delete the user account.
        """

    def log_in(self):
        """
        Enable the user to log in to his account.
        """

    def log_out(self):
        """
        Enable the user to log out of his account.
        """

    def update_name(self):
        """
        Change the name of the user.
        """

    def update_password(self):
        """
        Change the password of the user.
        """

    def create_database(self, db_name: str) -> bool:
        """
        Add a database to the user's space.
        """
        # Check
        database_already_exists = self.check_if_database_exists(
            db_name=db_name
        )
        if database_already_exists:
            return False
        # Create database
        db_definer = DbDefiner(user_name=self.user_name)
        db_created = db_definer.create_database(db_name=db_name)
        if not db_created:
            return False
        db_controller = DbController()
        db_controller.grant_privileges(
            user_name=self.user_name,
            db_name=db_name
        )
        tables_created = db_definer.create_seven_tables(db_name=db_name)
        if not tables_created:
            logger.error(f"Error with the creation of tables for {db_name}.")
            return False
        return True

    def check_if_database_exists(self, db_name: str) -> bool:
        """
        Check if the user's database already exists.
        """
        db_definer = DbDefiner(user_name=self.user_name)
        db_names = db_definer.get_user_databases()
        sql_db_name = self.user_name + '_' + db_name
        if sql_db_name in db_names:
            logger.info(f"Database name {db_name} exists")
            return True
        logger.info(f"Database name {db_name} does not exist")
        return False

    def get_databases_list(self) -> List[str]:
        """
        List the databases of the user.
        """
        db_definer = DbDefiner(user_name=self.user_name)
        databases = db_definer.get_user_databases()
        databases = [
            '_'.join(db.split('_')[1:])
            for db in databases
        ]
        return databases

    def remove_database(self, db_name: str) -> bool:
        """
        Remove a database from the user's space.
        """
        # Remove database
        db_definer = DbDefiner(self.user_name)
        db_dropped = db_definer.drop_database(db_name=db_name)
        # Remove privileges of the user on the database,
        # as they're not removed automatically
        db_controller = DbController()
        privileges_dropped = db_controller.revoke_privileges(
            user_name=self.user_name,
            db_name=db_name
        )
        return bool(db_dropped and privileges_dropped)

    def insert_word(self, db_name: str, foreign: str, native: str) -> bool:
        """
        Add a couple of words to the user's database.
        """
        db_manipulator = DbManipulator(
            user_name=self.user_name,
            db_name=db_name,
            test_type='version',
        )
        result = db_manipulator.insert_word(row=[foreign, native])
        return result

    def remove_word(self):
        """
        Remove a couple of words from the user's database.
        """
