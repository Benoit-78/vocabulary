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
from unittest.mock import MagicMock, patch

from fastapi.responses import JSONResponse
# from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import user as user_api


class TestUserApi(unittest.TestCase):
    @patch('src.api.authentication.create_token')
    @patch('src.api.user.users.UserAccount.create_account')
    def test_create_account_ok(self, mock_create_account, mock_create_token):
        """
        User account should be created.
        """
        # ----- ARRANGE
        creds = {
            'input_name': 'test_user',
            'input_password': 'test_password'
        }
        token = 'mock_token'
        mock_create_account.return_value = True
        mock_create_token.return_value = 'new_token'
        # ----- ACT
        result = user_api.create_account(creds, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_content = {
            'message': "User account created successfully",
            'userName': creds['input_name'],
            'token': 'new_token'
        }
        self.assertDictEqual(content_dict, expected_content)

    @patch('src.api.user.users.UserAccount.create_account')
    def test_create_account_nok(self, mock_create_account):
        """
        User account should be created.
        """
        # ----- ARRANGE
        creds = {
            'input_name': 'test_user',
            'input_password': 'test_password'
        }
        token = 'mock_token'
        mock_create_account.return_value = False
        # ----- ACT
        result = user_api.create_account(creds, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_content = {
            'message': "User name not available",
            'userName': creds['input_name'],
            'token': 'mock_token'
        }
        self.assertDictEqual(content_dict, expected_content)

    @patch('src.api.authentication.create_token')
    @patch('src.api.authentication.authenticate_user')
    @patch('src.api.authentication.get_users_list')
    def test_authenticate_user(
            self,
            mock_get_users_list,
            mock_authenticate_user,
            mock_create_token
        ):
        """
        User should be authenticated.
        """
        # ----- ARRANGE
        token = 'mock_token'
        form_data = MagicMock()
        form_data.username = 'test_user'
        form_data.password = 'test_password'
        mock_get_users_list.return_value = ['test_user', 'some_other_strange_user_name']
        mock_authenticate_user.return_value = 'test_user'
        mock_create_token.return_value = 'user_token'
        # ----- ACT
        result = user_api.authenticate_user(token, form_data)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_content = {
            'message': "User successfully authenticated",
            'userName': 'test_user',
            'token': 'user_token'
        }
        self.assertDictEqual(content_dict, expected_content)
        mock_get_users_list.assert_called_once()
        mock_authenticate_user.assert_called_once_with(
            ['test_user', 'some_other_strange_user_name'],
            'test_user',
            'test_password'
        )
        mock_create_token.assert_called_once_with(
            data={"sub": 'test_user'}
        )

    @patch('src.api.authentication.authenticate_user')
    @patch('src.api.authentication.get_users_list')
    def test_authenticate_user_unknown(
            self,
            mock_get_users_list,
            mock_authenticate_user,
        ):
        """
        User should be authenticated.
        """
        # ----- ARRANGE
        token = 'mock_token'
        form_data = MagicMock()
        form_data.username = 'test_user'
        form_data.password = 'test_password'
        mock_get_users_list.return_value = ['test_user', 'some_other_strange_user_name']
        mock_authenticate_user.return_value = "Unknown user"
        # ----- ACT
        result = user_api.authenticate_user(token, form_data)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_content = {
            'message': "Unknown user",
            'token': 'mock_token'
        }
        self.assertDictEqual(content_dict, expected_content)
        mock_get_users_list.assert_called_once()
        mock_authenticate_user.assert_called_once_with(
            ['test_user', 'some_other_strange_user_name'],
            'test_user',
            'test_password'
        )

    @patch('src.api.authentication.authenticate_user')
    @patch('src.api.authentication.get_users_list')
    def test_authenticate_user_password_incorrect(
            self,
            mock_get_users_list,
            mock_authenticate_user,
        ):
        """
        User should be authenticated.
        """
        # ----- ARRANGE
        token = 'mock_token'
        form_data = MagicMock()
        form_data.username = 'test_user'
        form_data.password = 'test_password'
        mock_get_users_list.return_value = ['test_user', 'some_other_strange_user_name']
        mock_authenticate_user.return_value = "Password incorrect"
        # ----- ACT
        result = user_api.authenticate_user(token, form_data)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_content = {
            'message': "Password incorrect",
            'token': 'mock_token'
        }
        self.assertDictEqual(content_dict, expected_content)
        mock_get_users_list.assert_called_once()
        mock_authenticate_user.assert_called_once_with(
            ['test_user', 'some_other_strange_user_name'],
            'test_user',
            'test_password'
        )

    @patch('src.api.authentication.get_user_name_from_token')
    def test_load_user_space(self, mock_get_user_name_from_token):
        """
        User space should be loaded.
        """
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'test_user'
        # ----- ACT
        result = user_api.load_user_space(request, token)
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            'request': 'mock_request',
            'token': 'mock_token',
            'user_name': 'test_user'
        }
        self.assertDictEqual(result, expected_result)
        mock_get_user_name_from_token.assert_called_once_with(token)
