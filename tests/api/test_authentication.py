"""
    Creator:
        B.Delorme
    Creation date:
        20th April 2024
    Main purpose:
        Test script for 
"""

import os
from datetime import datetime, timedelta

import unittest
from fastapi import HTTPException, status
from freezegun import freeze_time
from jose import JWTError
from unittest.mock import patch, MagicMock

from src.api import authentication as auth_api



class TestAuthentication(unittest.TestCase):
    """
    Test the functions of the authentication module.
    """
    def test_create_guest_user_name(self):
        """
        Test the creation of a guest user name.
        """
        # ----- ARRANGE
        # ----- ACT
        result = auth_api.create_guest_user_name()
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.keys()), ['sub'])
        self.assertIsInstance(result['sub'], str)
        self.assertIn('guest', result['sub'])
        guest_nb = result['sub'].split('_')[1]
        guest_nb = int(guest_nb)
        self.assertGreater(guest_nb, 0)
        self.assertLess(guest_nb, 1_000_001)

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @freeze_time("2024-04-23 23:23:49")
    @patch("src.api.authentication.jwt.encode")
    def test_create_token(
            self,
            mock_jwt_encode
        ):
        """
        Test the creation of a token.
        """
        # ----- ARRANGE
        data = {"sub": 123}
        expires_delta = 15
        # ----- ACT
        token = auth_api.create_token(data, expires_delta)
        # ----- ASSERT
        assert token is not None
        mock_jwt_encode.assert_called_once_with(
            {
                "sub": 123,
                "exp": datetime.now() + timedelta(minutes=expires_delta)
            },
            "your_secret_key",
            algorithm=auth_api.ALGORITHM
        )

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @freeze_time("2024-04-23 23:23:49")
    @patch("src.api.authentication.jwt.encode")
    @patch("src.api.authentication.create_guest_user_name")
    def test_create_token_no_data(
            self,
            mock_create_guest_user_name,
            mock_jwt_encode
        ):
        """
        Test the creation of a token with no data.
        """
        # ----- ARRANGE
        data = None
        expires_delta = 15
        mock_create_guest_user_name.return_value = {"sub": "user"}
        # ----- ACT
        token = auth_api.create_token(data, expires_delta)
        # ----- ASSERT
        assert token is not None
        mock_jwt_encode.assert_called_once_with(
            {
                "sub": 'user',
                "exp": datetime.now() + timedelta(minutes=expires_delta)
            },
            "your_secret_key",
            algorithm=auth_api.ALGORITHM
        )
        mock_create_guest_user_name.assert_called_once()

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @freeze_time("2024-04-23 23:23:49")
    @patch("src.api.authentication.jwt.encode")
    def test_create_token_std_expire_delta(
            self,
            mock_jwt_encode
        ):
        """
        Test the creation of a token with the standard expiration delta.
        """
        # ----- ARRANGE
        data = {"sub": 123}
        # ----- ACT
        token = auth_api.create_token(data)
        # ----- ASSERT
        assert token is not None
        mock_jwt_encode.assert_called_once_with(
            {
                "sub": 123,
                "exp": datetime.now() + timedelta(minutes=15)
            },
            "your_secret_key",
            algorithm=auth_api.ALGORITHM
        )

    @patch('src.data.database_interface.DbController.get_users_list')
    def test_get_users_list(self, mock_get_users_list):
        """
        Test the retrieval of the users list.
        """
        # ----- ARRANGE
        mock_users_list = [
            {"user1": "user1"},
            {"user2": "user2"},
            {"user3": "user3"}
        ]
        mock_get_users_list.return_value = mock_users_list
        # ----- ACT
        result = auth_api.get_users_list()
        # ----- ASSERT
        self.assertIsInstance(result, list)
        self.assertEqual(result, mock_users_list)
        mock_get_users_list.assert_called_once()

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @patch('src.api.authentication.jwt.decode')
    def test_get_user_name_from_token(self, mock_decode):
        """
        Test the retrieval of the user name from a token.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_dict = {"sub": "mock_user_name"}
        mock_decode.return_value = mock_dict
        # ----- ACT
        result = auth_api.get_user_name_from_token(token)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, "mock_user_name")
        mock_decode.assert_called_once_with(
            token,
            "your_secret_key",
            algorithms=[auth_api.ALGORITHM]
        )

    @patch('src.api.authentication.get_user_name_from_token')
    def test_check_token_guest(
            self,
            mock_get_user_name_from_token
        ):
        """
        Test the check of a token for a guest user.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'guest_user1'
        # ----- ACT
        result = auth_api.check_token(token)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, token)
        mock_get_user_name_from_token.assert_called_once_with(token)

    @patch('src.api.authentication.get_users_list')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_check_token(
            self,
            mock_get_user_name_from_token,
            mock_get_users_list
        ):
        """
        Test the check of a token for a registered user.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_get_users_list.return_value = [
            {"username": "user1"},
            {"username": "user2"},
            {"username": "user3"}
        ]
        mock_get_user_name_from_token.return_value = 'user1'
        # ----- ACT
        result = auth_api.check_token(token)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, token)
        mock_get_user_name_from_token.assert_called_once_with(token)
        mock_get_users_list.assert_called_once()

    @patch('src.api.authentication.get_users_list')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_check_token_user_unknown(
            self,
            mock_get_user_name_from_token,
            mock_get_users_list
        ):
        """
        Test the check of a token for an unknown user.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_get_users_list.return_value = [
            {"username": "user1"},
            {"username": "user2"},
            {"username": "user3"}
        ]
        mock_get_user_name_from_token.return_value = 'user_very_very_strange'
        # ----- ACT
        with self.assertRaises(HTTPException):
            auth_api.check_token(token)
        # ----- ASSERT
        mock_get_user_name_from_token.assert_called_once_with(token)
        mock_get_users_list.assert_called_once()

    @patch('src.api.authentication.get_user_name_from_token')
    def test_check_token_error(self, mock_get_user_name_from_token):
        # ----- ARRANGE
        mock_get_user_name_from_token.side_effect = JWTError
        # credentials_exception = HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Could not validate credentials",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        # ----- ACT
        # ----- ASSERT
        with self.assertRaises(HTTPException):
            auth_api.check_token('mock_token')

    @patch('src.api.authentication.CryptContext.hash')
    def test_get_password_hash(self, mock_hash):
        """
        Test the retrieval of the password hash.
        """
        # ----- ARRANGE
        password = 'mock_password'
        mock_hash.return_value = 'mock_hash'
        # ----- ACT
        result = auth_api.get_password_hash(password)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'mock_hash')
        mock_hash.assert_called_once_with(password)

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @patch('src.data.database_interface.DbController.get_users_list')
    @patch('src.api.authentication.jwt.decode')
    def test_get_username_from_token(
            self,
            mock_decode,
            mock_get_users_list
        ):
        """
        Test the retrieval of the user name from a token.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_dict = {"sub": "user1"}
        mock_decode.return_value = mock_dict
        mock_get_users_list.return_value = [
            {"username": "user1"},
            {"username": "user2"},
            {"username": "user3"}
        ]
        # ----- ACT
        result = auth_api.get_user_name_from_token_oauth(token)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'user1')
        mock_decode.assert_called_once_with(
            token,
            "your_secret_key",
            algorithms=[auth_api.ALGORITHM]
        )
        mock_get_users_list.assert_called_once()

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @patch('src.api.authentication.jwt.decode')
    def test_get_username_from_token_no_user_name(
            self,
            mock_decode,
        ):
        """
        Test the retrieval of the user name from a token
        that does not contain any user name.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_dict = {"sub": None}
        mock_decode.return_value = mock_dict
        # ----- ACT
        with self.assertRaises(HTTPException):
            auth_api.get_user_name_from_token_oauth(token)
        # ----- ASSERT
        mock_decode.assert_called_once_with(
            token,
            "your_secret_key",
            algorithms=[auth_api.ALGORITHM]
        )

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @patch('src.api.authentication.jwt.decode')
    def test_get_username_from_token_error(
            self,
            mock_decode,
        ):
        """
        Test the retrieval of the user name from a token
        that does not contain any user name.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_decode.side_effect = JWTError
        # ----- ACT
        with self.assertRaises(HTTPException):
            auth_api.get_user_name_from_token_oauth(token)
        # ----- ASSERT
        mock_decode.assert_called_once_with(
            token,
            "your_secret_key",
            algorithms=[auth_api.ALGORITHM]
        )

    @patch.dict(os.environ, {"SECRET_KEY": "your_secret_key"})
    @patch('src.data.database_interface.DbController.get_users_list')
    @patch('src.api.authentication.jwt.decode')
    def test_get_username_from_token_unknown_user(
            self,
            mock_decode,
            mock_get_users_list
        ):
        """
        Test the retrieval of the user name from a token if the user is unknown.
        """
        # ----- ARRANGE
        token = 'mock_token'
        mock_dict = {"sub": "user4"}
        mock_decode.return_value = mock_dict
        mock_get_users_list.return_value = [
            {"username": "user1"},
            {"username": "user2"},
            {"username": "user3"}
        ]
        # ----- ACT
        with self.assertRaises(HTTPException):
            auth_api.get_user_name_from_token_oauth(token)
        # ----- ASSERT
        mock_decode.assert_called_once_with(
            token,
            "your_secret_key",
            algorithms=[auth_api.ALGORITHM]
        )
        mock_get_users_list.assert_called_once()

    @patch('src.api.authentication.CryptContext.verify')
    def test_user_exists_correct_password(self, mock_pwt_verify):
        """
        Test the authentication of a user with the correct password.
        """
        # ----- ARRANGE
        users_list = [
            {'username': 'user1', 'password_hash': 'hashed_password1'},
            {'username': 'user2', 'password_hash': 'hashed_password2'},
        ]
        mock_pwt_verify.return_value = True
        # ----- ACT
        authenticated_user = auth_api.authenticate_user(
            users_list,
            'user1',
            'password1'
        )
        # ----- ASSERT
        self.assertIsInstance(authenticated_user, auth_api.UserInDB)

    @patch('src.api.authentication.CryptContext.verify')
    def test_user_exists_incorrect_password(self, mock_pwt_verify):
        """
        Test the authentication of a user with an incorrect password.
        """
        # ----- ARRANGE
        users_list = [
            {'username': 'user1', 'password_hash': 'hashed_password1'},
            {'username': 'user2', 'password_hash': 'hashed_password2'},
        ]
        mock_pwt_verify.return_value = False
        # ----- ACT
        wrong_password_user = auth_api.authenticate_user(
            users_list,
            'user1',
            'wrong_password'
        )
        # ----- ASSERT
        self.assertEqual(wrong_password_user, 'Password incorrect')

    def test_user_does_not_exist(self):
        """
        Test the authentication of a user that does not exist.
        """
        # ----- ARRANGE
        users_list = [
            {'username': 'user1', 'password_hash': 'hashed_password1'},
            {'username': 'user2', 'password_hash': 'hashed_password2'},
        ]
        # ----- ACT
        unknown_user = auth_api.authenticate_user(
            users_list,
            'non_existing_user',
            'password'
        )
        # ----- ASSERT
        self.assertEqual(unknown_user, 'Unknown user')

    @patch('src.api.authentication.authenticate_user')
    def test_authenticate_with_oauth(self, mock_authenticate_user):
        # ----- ARRANGE
        form_data = MagicMock()
        form_data.username = 'user1'
        form_data.password = 'password1'
        mock_authenticate_user.return_value = 'authenticated_user'
        # ----- ACT
        result = auth_api.authenticate_with_oauth(form_data)
        # ----- ASSERT
        self.assertEqual(result, 'authenticated_user')
        mock_authenticate_user.assert_called_once_with(
            users_list=auth_api.users_dict,
            username='user1',
            password='password1'
        )

    def test_sign_in(self):
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        error_message = 'mock_error_message'
        # ----- ACT
        result = auth_api.sign_in(
            request=request,
            token=token,
            error_message=error_message
        )
        # ----- ASSERT
        expected_dict = {
            'request': request,
            'token': token,
            'errorMessage': error_message,
        }
        self.assertEqual(result, expected_dict)
