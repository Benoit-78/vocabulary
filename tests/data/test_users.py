"""
    Creator:
        B.Delorme
    Creation date:
        20th April 2024
    Main purpose:
        Test script for 
"""

import os
import sys
import unittest
from unittest.mock import patch

# from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data import users


class TestUserAccount(unittest.TestCase):
    def setUp(self):
        user_name = 'mock_user_name'
        self.account = users.UserAccount(user_name)

    def test_init(self):
        # ----- ARRANGE
        # ----- ACT
        # ----- ASSERT
        self.assertEqual(self.account.user_name, 'mock_user_name')
        account_types = [
            'guest',
            'user',
            'customer',
            'developer'
        ]
        self.assertEqual(self.account.account_types, account_types)

    @patch('src.data.users.DbController.add_user_to_users_table')
    @patch('src.data.users.DbController.grant_privileges_on_common_database')
    @patch('src.data.users.DbController.create_user_in_mysql')
    @patch('src.api.authentication.get_password_hash')
    @patch('src.data.users.UserAccount.check_if_account_exists')
    def test_create_account(
            self,
            mock_check,
            mock_get_pwd_hash,
            mock_create_user_in_mysql,
            mock_grant_privileges,
            mock_add_user
        ):
        # ----- ARRANGE
        password = 'mock_password'
        mock_check.return_value = False
        mock_get_pwd_hash.return_value = 'mock_hash'
        mock_create_user_in_mysql.return_value = True
        mock_grant_privileges.return_value = True
        mock_add_user.return_value = True
        # ----- ACT
        result = self.account.create_account(password)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        mock_check.assert_called_once()
        mock_get_pwd_hash.assert_called_once_with(password)
        mock_create_user_in_mysql.assert_called_once_with('mock_user_name', 'mock_hash')
        mock_grant_privileges.assert_called_once_with('mock_user_name')
        mock_add_user.assert_called_once_with('mock_user_name', 'mock_hash')

    @patch('src.data.users.UserAccount.check_if_account_exists')
    def test_create_account_already_exists(
            self,
            mock_check,
        ):
        # ----- ARRANGE
        password = 'mock_password'
        mock_check.return_value = True
        # ----- ACT
        result = self.account.create_account(password)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, False)
        mock_check.assert_called_once()

    @patch('src.data.users.DbController.get_users_list')
    @patch('src.data.users.DbController.get_users_list_from_mysql')
    def test_check_if_account_exists(
            self,
            mock_get_users_list_from_mysql,
            mock_get_users_list
        ):
        # ----- ARRANGE
        mock_get_users_list_from_mysql.return_value = ['user_1', 'user_2']
        mock_get_users_list.return_value = [
            {'username': 'user_1'},
            {'username': 'user_2'}
        ]
        # ----- ACT
        result = self.account.check_if_account_exists()
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, False)
        mock_get_users_list_from_mysql.assert_called_once()
        mock_get_users_list.assert_called_once()

    @patch('src.data.users.DbController.get_users_list_from_mysql')
    def test_check_if_account_exists_yes(
            self,
            mock_get_users_list_from_mysql,
        ):
        # ----- ARRANGE
        mock_get_users_list_from_mysql.return_value = [
            'user_1',
            'user_2',
            self.account.user_name
        ]
        # ----- ACT
        result = self.account.check_if_account_exists()
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        mock_get_users_list_from_mysql.assert_called_once()

    @patch('src.data.users.DbController.get_users_list')
    @patch('src.data.users.DbController.get_users_list_from_mysql')
    def test_check_if_account_exists_no_yes(
            self,
            mock_get_users_list_from_mysql,
            mock_get_users_list
        ):
        # ----- ARRANGE
        mock_get_users_list_from_mysql.return_value = ['user_1', 'user_2']
        mock_get_users_list.return_value = [
            {'username': 'user_1'},
            {'username': 'user_2'},
            {'username': self.account.user_name}
        ]
        # ----- ACT
        result = self.account.check_if_account_exists()
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        mock_get_users_list_from_mysql.assert_called_once()
        mock_get_users_list.assert_called_once()

    @patch('src.data.users.DbDefiner.create_seven_tables')
    @patch('src.data.users.DbController.grant_privileges')
    @patch('src.data.users.DbDefiner.create_database')
    @patch('src.data.users.UserAccount.check_if_database_exists')
    def test_create_database(
            self,
            mock_check,
            mock_create_db,
            mock_grant,
            mock_create_tables
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_check.return_value = False
        mock_create_db.return_value = True
        mock_grant.return_value = True
        mock_create_tables.return_value = True
        # ----- ACT
        result = self.account.create_database(db_name)
        # ----- ASSERT
        self.assertEqual(result, True)
        mock_check.assert_called_once_with(db_name)
        mock_create_db.assert_called_once_with(db_name)
        mock_grant.assert_called_once_with(self.account.user_name, db_name)
        mock_create_tables.assert_called_once_with(db_name)

    @patch('src.data.users.UserAccount.check_if_database_exists')
    def test_create_database_already_exists(
            self,
            mock_check
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_check.return_value = True
        # ----- ACT
        result = self.account.create_database(db_name)
        # ----- ASSERT
        self.assertEqual(result, False)
        mock_check.assert_called_once_with(db_name)

    @patch('src.data.users.DbDefiner.create_database')
    @patch('src.data.users.UserAccount.check_if_database_exists')
    def test_create_database_not_created(
            self,
            mock_check,
            mock_create_db
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_check.return_value = False
        mock_create_db.return_value = False
        # ----- ACT
        result = self.account.create_database(db_name)
        # ----- ASSERT
        self.assertEqual(result, False)
        mock_check.assert_called_once_with(db_name)
        mock_create_db.assert_called_once_with(db_name)

    @patch('src.data.users.DbDefiner.create_seven_tables')
    @patch('src.data.users.DbController.grant_privileges')
    @patch('src.data.users.DbDefiner.create_database')
    @patch('src.data.users.UserAccount.check_if_database_exists')
    def test_create_database_error(
            self,
            mock_check,
            mock_create_db,
            mock_grant,
            mock_create_tables
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_check.return_value = False
        mock_create_db.return_value = True
        mock_grant.return_value = True
        mock_create_tables.return_value = False
        # ----- ACT
        result = self.account.create_database(db_name)
        # ----- ASSERT
        self.assertEqual(result, False)
        mock_check.assert_called_once_with(db_name)
        mock_create_db.assert_called_once_with(db_name)
        mock_grant.assert_called_once_with(self.account.user_name, db_name)
        mock_create_tables.assert_called_once_with(db_name)

    @patch('src.data.users.logger')
    @patch('src.data.users.DbDefiner.get_user_databases')
    def test_check_if_database_exists(
            self,
            mock_get_user_databases,
            mock_logger
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_get_user_databases.return_value = [
            'db_1',
            'db_2',
        ]
        # ----- ACT
        result = self.account.check_if_database_exists(db_name)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, False)
        mock_logger.success.assert_called_once_with(
            f"Database name {db_name} is available."
        )

    @patch('src.data.users.logger')
    @patch('src.data.users.DbDefiner.get_user_databases')
    def test_check_if_database_exists_yes(
            self,
            mock_get_user_databases,
            mock_logger
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_get_user_databases.return_value = [
            'db_1',
            'db_2',
            self.account.user_name + '_' + db_name
        ]
        # ----- ACT
        result = self.account.check_if_database_exists(db_name)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        mock_logger.error.assert_called_once_with(
            f"Database name {db_name} already exists."
        )

    @patch('src.data.users.DbDefiner.get_user_databases')
    def test_get_databases_list(self, mock_get_user_databases):
        # ----- ARRANGE
        mock_get_user_databases.return_value = [
            'usr_db_1',
            'usr_db_2',
        ]
        # ----- ACT
        result = self.account.get_databases_list()
        # ----- ASSERT
        self.assertIsInstance(result, list)
        self.assertEqual(result, ['db_1', 'db_2'])
        mock_get_user_databases.assert_called_once()

    @patch('src.data.users.DbController.revoke_privileges')
    @patch('src.data.users.DbDefiner.drop_database')
    def test_remove_database(
            self,
            mock_drop,
            mock_revoke
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_drop.return_value = True
        mock_revoke.return_value = True
        # ----- ACT
        result = self.account.remove_database(db_name)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        mock_drop.assert_called_once_with(db_name)
        mock_revoke.assert_called_once_with(self.account.user_name, db_name)

    @patch('src.data.users.DbController.revoke_privileges')
    @patch('src.data.users.DbDefiner.drop_database')
    def test_remove_database_error(
            self,
            mock_drop,
            mock_revoke
        ):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        mock_drop.return_value = True
        mock_revoke.return_value = False
        # ----- ACT
        result = self.account.remove_database(db_name)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, False)
        mock_drop.assert_called_once_with(db_name)
        mock_revoke.assert_called_once_with(self.account.user_name, db_name)

    @patch('src.data.users.DbManipulator.insert_word')
    def test_insert_word(self, mock_insert):
        # ----- ARRANGE
        db_name = 'mock_db_name'
        foreign = 'mock_foreign'
        native = 'mock_native'
        mock_insert.return_value = True
        # ----- ACT
        result = self.account.insert_word(db_name, foreign, native)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        mock_insert.assert_called_once_with([foreign, native])
