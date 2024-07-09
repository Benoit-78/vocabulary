"""
    Creator:
        B.Delorme
    Creation date:
        20th April 2024
    Main purpose:
        Test script for 
"""

import json
import os
import sys
import unittest
from unittest.mock import patch

import asyncio
import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
# from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import database as db_api


@pytest.fixture
async def csv_file():
    """
    Simulate an async CSV file object
    """
    class AsyncCSVFile:
        async def read(self):
            """
            Simulate an async read operation
            """
            # Simulate some asynchronous operation
            await asyncio.sleep(0.1)
            # Simulated CSV content as bytes
            return b"csv_content_here"
    return AsyncCSVFile()



class TestDatabase(unittest.TestCase):
    @patch('src.data.users.UserAccount.get_databases_list')
    @patch('src.api.database.auth_api.get_user_name_from_token')
    def test_get_user_databases(
            self,
            mock_get_user_name_from_token,
            mock_get_databases_list
        ):
        """
        Test the function get_user_databases
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_get_databases_list.return_value = ['db1', 'db2']
        # ----- ACT
        result = db_api.get_user_databases(token)
        # ----- ASSERT
        self.assertIsInstance(result, list)
        self.assertEqual(result, ['db1', 'db2'])
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_get_databases_list.assert_called_once()

    @patch('src.api.database.get_error_messages')
    @patch('src.api.database.get_user_databases')
    def test_load_user_databases(
            self,
            mock_get_user_databases,
            mock_get_error_messages
        ):
        """
        Test the function load_user_databases
        """
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        error_message = 'mock_error_message'
        mock_get_user_databases.return_value = ['db1', 'db2']
        mock_get_error_messages.return_value = 'mock_db_message'
        # ----- ACT
        result = db_api.load_user_databases(
            request,
            token,
            error_message
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            'request': request,
            'token': token,
            'databases': ['db1', 'db2'],
            'createDatabaseErrorMessage': 'mock_db_message'
        }
        self.assertEqual(result, expected_result)
        mock_get_user_databases.assert_called_once_with(token=token)

    @patch('src.data.users.UserAccount.check_if_database_exists')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_choose_database(
            self,
            mock_get_user_name_from_token,
            mock_check_if_database_exists
        ):
        """
        Test the function choose_database
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_check_if_database_exists.return_value = True
        # ----- ACT
        result = db_api.choose_database(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        expected_result = {
            "message": "Database chosen successfully"
        }
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_check_if_database_exists.assert_called_once_with(db_name=data['db_name'])

    @patch('src.data.users.UserAccount.check_if_database_exists')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_choose_database_not_available(
            self,
            mock_get_user_name_from_token,
            mock_check_if_database_exists
        ):
        """
        Test the function choose_database
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_check_if_database_exists.return_value = False
        # ----- ACT
        result = db_api.choose_database(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        expected_result = {
            "message": f"Database name {data['db_name']} not available"
        }
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_check_if_database_exists.assert_called_once_with(db_name=data['db_name'])

    @patch('src.data.users.UserAccount.create_database')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_create_database(
            self,
            mock_get_user_name_from_token,
            mock_create_database
        ):
        """
        Test the function choose_database
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_create_database.return_value = True
        # ----- ACT
        result = db_api.create_database(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        expected_result = {
            'message': "Database created successfully",
            'token': token,
            'databaseName': data['db_name']
        }
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_create_database.assert_called_once_with(db_name=data['db_name'])

    @patch('src.api.authentication.get_user_name_from_token')
    def test_create_database_no_name(
            self,
            mock_get_user_name_from_token,
        ):
        """
        Test the function choose_database
        """
        # ----- ARRANGE
        data = {'db_name': ''}
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        # ----- ACT
        result = db_api.create_database(
            data=data,
            token=token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'message': "No database name given",
            'token': token,
            'databaseName': ''
        }
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)

    @patch('src.data.users.UserAccount.create_database')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_create_database_not_available(
            self,
            mock_get_user_name_from_token,
            mock_create_database
        ):
        """
        Test the function choose_database
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_create_database.return_value = False
        # ----- ACT
        result = db_api.create_database(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        expected_result = {
            'message': "Database name not available",
            'token': token,
            'databaseName': data['db_name']
        }
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_create_database.assert_called_once_with(db_name=data['db_name'])

    @patch('src.api.database.DbQuerier.get_tables')
    @patch('src.api.database.auth_api.get_user_name_from_token')
    def test_retrieve_database(
            self,
            mock_mock_get_user_name_from_token,
            mock_get_tables
        ):
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name',
            'some_key': 'some_value'
        }
        token = 'mock_token'
        mock_mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_get_tables.return_value = {
            'version_voc': 'mock_version_table',
            'theme_voc': 'mock_theme_table'
        }
        # ----- ACT
        result = db_api.retrieve_database(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        expected_result = {
            "message": "Retrieved database words successfully",
            "token": token,
            'versionTable': 'mock_version_table',
            'themeTable': 'mock_theme_table'
        }
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(content_dict, expected_result)

    def test_see_database(self):
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        db_name = 'mock_db_name'
        version_table = 'mock_version_table'
        theme_table = 'mock_theme_table'
        # ----- ACT
        result = db_api.see_database(
            request=request,
            token=token,
            db_name=db_name,
            version_table=version_table,
            theme_table=theme_table
        )
        # ----- ASSERT
        expected_result = {
            'request': 'mock_request',
            'token': 'mock_token',
            'databaseName': 'mock_db_name',
            'versionTable': 'mock_version_table',
            'themeTable': 'mock_theme_table',
        }
        self.assertEqual(result, expected_result)

    def test_get_error_messages_fail(self):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = "Database name not available"
        # ----- ACT
        result = db_api.get_error_messages(error_message)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'A database of this name already exists')

    def test_get_error_messages_success(self):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = "Database created successfully"
        # ----- ACT
        result = db_api.get_error_messages(error_message)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, '')

    def test_get_error_messages_neutral(self):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = ''
        # ----- ACT
        result = db_api.get_error_messages(error_message)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, '')

    @patch('src.api.database.logger')
    def test_get_error_messages_error(self, mock_logger):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = 'blableblibloblu'
        # ----- ACT
        with self.assertRaises(ValueError):
            db_api.get_error_messages(error_message)
        # ----- ASSERT
        mock_logger.error.assert_any_call(f"Error message incorrect: {error_message}")
        expected_list = [
            "No database name given",
            "Database name not available",
            "Database created successfully",
            ''
        ]
        mock_logger.error.assert_any_call(
            f"Should be in: {expected_list}"
        )

    def test_get_error_messages_no_name(self):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = "No database name given"
        # ----- ACT
        result = db_api.get_error_messages(error_message)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, error_message)

    @patch('src.api.authentication.get_user_name_from_token')
    def test_fill_database(self, mock_get_user_name_from_token):
        """
        Test the function fill_database
        """
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        db_name = 'mock_db_name'
        error_message = 'mock_error_message'
        mock_get_user_name_from_token.return_value = 'mock_user'
        # ----- ACT
        result = db_api.fill_database(
            request,
            db_name,
            error_message,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            'request': request,
            'title': "Here you can add words to your database",
            'token': token,
            'databaseName': db_name,
            'wordAlreadyPresentErrorMessage': error_message,
        }
        self.assertEqual(result, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)

    @patch('src.api.database.logger')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_fill_database_no_db(self, mock_get_user_name_from_token, mock_logger):
        """
        Test the function fill_database
        """
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        db_name = None
        error_message = 'mock_error_message'
        mock_get_user_name_from_token.return_value = 'mock_user'
        # ----- ACT
        with self.assertRaises(HTTPException):
            db_api.fill_database(
                request,
                db_name,
                error_message,
                token
            )
        # ----- ASSERT
        mock_logger.error.called_once_with("No database name given")
        assert not mock_get_user_name_from_token.called

    @patch('src.data.users.UserAccount.insert_word')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_create_word(
            self,
            mock_get_user_name_from_token,
            mock_insert_word
        ):
        """
        Test the function create_word
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name',
            'foreign': 'word',
            'native': 'mot'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_insert_word.return_value = True
        # ----- ACT
        result = db_api.create_word(data, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'message': "Word added successfully"
        }
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_insert_word.assert_called_once_with(
            db_name=data['db_name'],
            foreign=data['foreign'],
            native=data['native']
        )

    @patch('src.data.users.UserAccount.insert_word')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_create_word_already_exists(
            self,
            mock_get_user_name_from_token,
            mock_insert_word
        ):
        """
        Test the function create_word
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name',
            'foreign': 'word',
            'native': 'mot'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_insert_word.return_value = "Word already exists"
        # ----- ACT
        result = db_api.create_word(data, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'message': "Word already exists"
        }
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_insert_word.assert_called_once_with(
            db_name=data['db_name'],
            foreign=data['foreign'],
            native=data['native']
        )

    @patch('src.data.users.UserAccount.insert_word')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_create_word_error(
            self,
            mock_get_user_name_from_token,
            mock_insert_word
        ):
        """
        Test the function create_word
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name',
            'foreign': 'word',
            'native': 'mot'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_insert_word.return_value = False
        # ----- ACT
        result = db_api.create_word(data, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'message': "Error with the word creation"
        }
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_insert_word.assert_called_once_with(
            db_name=data['db_name'],
            foreign=data['foreign'],
            native=data['native']
        )

    @patch('src.data.users.UserAccount.remove_database')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_delete_database(
            self,
            mock_get_user_name_from_token,
            mock_remove_database
        ):
        """
        Test the function remove_database
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_remove_database.return_value = True
        # ----- ACT
        result = db_api.delete_database(data, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'message': "Database deleted successfully"
        }
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_remove_database.assert_called_once_with(db_name=data['db_name'])

    @patch('src.data.users.UserAccount.remove_database')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_delete_database_error(
            self,
            mock_get_user_name_from_token,
            mock_remove_database
        ):
        """
        Test the function remove_database
        """
        # ----- ARRANGE
        data = {
            'db_name': 'mock_db_name'
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user'
        mock_remove_database.return_value = False
        # ----- ACT
        result = db_api.delete_database(data, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'message': "Error with the database removal"
        }
        self.assertEqual(content_dict, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_remove_database.assert_called_once_with(db_name=data['db_name'])

    def test_is_malicious_1(self):
        """
        Test the function is_malicious
        """
        # ----- ARRANGE
        csv_content = "DROP DATABASE"
        # ----- ACT
        result = db_api.is_malicious(csv_content)
        # ----- ASSERT
        self.assertTrue(result)

    def test_is_malicious_2(self):
        """
        Test the function is_malicious
        """
        # ----- ARRANGE
        csv_content = "DELETE FROM"
        # ----- ACT
        result = db_api.is_malicious(csv_content)
        # ----- ASSERT
        self.assertTrue(result)

    def test_is_malicious_no(self):
        """
        Test the function is_malicious
        """
        # ----- ARRANGE
        csv_content = "yes"
        # ----- ACT
        result = db_api.is_malicious(csv_content)
        # ----- ASSERT
        self.assertFalse(result)
