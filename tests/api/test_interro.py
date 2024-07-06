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

import pandas as pd
from fastapi.responses import JSONResponse
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import interro as interro_api
from src.interro import PremierTest, Rattrap
from src.views import api as api_view


class TestInterro(unittest.TestCase):
    """
    Test class for interro.py
    """
    @patch('src.api.interro.PremierTest')
    @patch('src.api.interro.FastapiGuesser')
    @patch('src.api.interro.Loader')
    @patch('src.api.interro.DbQuerier')
    def test_load_test(
            self,
            mock_db_querier,
            mock_loader,
            mock_guesser,
            mock_premier_test
        ):
        """
        Should instanciate a data loader and a corresponding PremierTest object.
        """
        # ----- ARRANGE
        user_name = 'mock_user_name'
        db_name = 'mock_db_name'
        test_type = 'mock_test_type'
        test_length = 10
        mock_db_querier.return_value = 'mock_db_querier'
        mock_loader_object = MagicMock()
        mock_loader_object.words = 10
        mock_loader_object.interro_df = pd.DataFrame({'col_1': ['val_1', 'val_2']})
        mock_loader.return_value = mock_loader_object
        mock_guesser.return_value = 'mock_guesser'
        mock_premier_test.return_value = 'mock_premier_test'
        # ----- ACT
        result = interro_api.load_test(
            user_name=user_name,
            db_name=db_name,
            test_type=test_type,
            test_length=test_length
        )
        # ----- ASSERT
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], MagicMock)
        self.assertEqual(result[1], 'mock_premier_test')
        mock_db_querier.assert_called_once_with(
            user_name=user_name,
            db_name=db_name,
            test_type=test_type,
        )
        mock_loader.assert_called_once_with(
            words=test_length,
            data_querier='mock_db_querier',
        )
        mock_loader_object.load_tables.assert_called_once()
        mock_loader_object.set_interro_df.assert_called_once()
        mock_guesser.assert_called_once()
        mock_premier_test.assert_called_once()

    @patch('src.api.interro.get_error_messages')
    @patch('src.api.interro.get_user_databases')
    def test_get_interro_settings(
            self,
            mock_get_user_databases,
            mock_get_error_messages
        ):
        """
        Test get_interro_settings function
        """
        # ----- ARRANGE
        token = 'mock_token'
        error_message = 'mock_error_message'
        db_message = 'mock_db_message'
        mock_get_error_messages.return_value = db_message
        mock_get_user_databases.return_value = ['db1', 'db2']
        # ----- ACT
        result = interro_api.get_interro_settings(
            token=token,
            error_message=error_message
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        self.assertEqual(
            result,
            {
                'token': 'mock_token',
                'databases': ['db1', 'db2'],
                'emptyTableErrorMessage': db_message,
            }
        )
        mock_get_user_databases.assert_called_once_with(token=token)
        mock_get_error_messages.assert_called_once_with(error_message=error_message)

    @patch('src.api.interro.get_old_interro_dict')
    @patch('src.api.interro.get_interro_category')
    @patch('src.api.interro.load_test')
    @patch('src.api.interro.get_user_name_from_token')
    def test_save_interro_settings(
            self,
            mock_get_user_name_from_token,
            mock_load_test,
            mock_get_interro_category,
            mock_get_old_interro_dict
        ):
        """
        Test save_interro_settings function
        """
        # ----- ARRANGE
        params = {
            'databaseName': 'mock_db_name',
            'testType': 'mock_test_type',
            'testLength': '2',
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_test = MagicMock()
        mock_test.words = 1
        mock_test.to_dict.return_value = {
            'mock_key': 'mock_value',
            'interroDict': 'mock_interro_dict'
        }
        mock_load_test.return_value = ('mock_loader', mock_test)
        mock_get_interro_category.return_value = 'mock_interro_category'
        mock_get_old_interro_dict.return_value = 'mock_old_interro_dict'
        # ----- ACT
        result = interro_api.save_interro_settings(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        assert content_dict['mock_key'] == 'mock_value'
        assert content_dict['message'] == "Settings saved successfully"
        assert content_dict['token'] == token
        assert content_dict['oldInterroDict'] == 'mock_old_interro_dict'
        mock_load_test.assert_called_once()
        mock_get_interro_category.assert_called_once_with(interro=mock_test)
        mock_get_old_interro_dict.assert_called_once_with(
            interro_dict='mock_interro_dict'
        )

    @patch('src.api.interro.load_test')
    @patch('src.api.interro.get_user_name_from_token')
    def test_save_interro_settings_empty_table(
            self,
            mock_get_user_name_from_token,
            mock_load_test,
        ):
        """
        Test save_interro_settings function
        """
        # ----- ARRANGE
        params = {
            'databaseName': 'mock_db_name',
            'testType': 'mock_test_type',
            'testLength': '2',
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_test = MagicMock()
        mock_test.words = 1
        mock_load_test.side_effect = ValueError()
        # ----- ACT
        result = interro_api.save_interro_settings(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        assert content_dict['message'] == "Empty table"
        assert content_dict['token'] == token

    @patch('src.api.interro.decode_dict')
    def test_get_interro_question(
            self,
            mock_decode_dict,
        ):
        # ----- ARRANGE
        token = 'mock_token'
        params = MagicMock()
        params.count = '2'
        params.interroDict = {'foreign': ['zero', 'one', 'two']}
        params.index = '1'
        params.databaseName = ''
        params.faultsDict = {'fault_key': 'fault_value'}
        params.interroCategory = 'test'
        params.message = ''
        params.oldInterroDict = {'old_key': 'old_value'}
        params.perf = '0'
        params.score = '2'
        params.testLength = '10'
        params.testType = 'version'
        mock_decode_dict.return_value = pd.DataFrame({
            'foreign': ['zero', 'one', 'two'],
            'native': ['zero', 'un', 'deux']
        })
        # ----- ACT
        result = interro_api.get_interro_question(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            'content_box1': 'one',
            'count': 3,
            'databaseName': params.databaseName,
            'faultsDict': params.faultsDict,
            'index': 1,
            'interroCategory': params.interroCategory,
            'interroDict': params.interroDict,
            'message': params.message,
            'oldInterroDict': params.oldInterroDict,
            'perf': params.perf,
            'progressPercent': 20,
            'score': params.score,
            'testLength': 10,
            'testType': params.testType,
            'token': token,
        }
        self.assertEqual(
            result,
            expected_dict
        )

    @patch('src.api.interro.decode_dict')
    def test_load_interro_answer(self, mock_decode_dict):
        # ----- ARRANGE
        token = 'mock_token'
        params = MagicMock()
        params.count = '1'
        params.databaseName = 'mock_db_name'
        params.faultsDict = 'mock_faults_dict'
        params.index = '2'
        params.interroCategory = 'mock_interro_category'
        params.interroDict = 'mock_interro_dict'
        params.oldInterroDict = 'mock_old_interro_dict'
        params.perf = 1
        params.score = 3
        params.testLength = 10
        params.testType = 'version'
        mock_decode_dict.return_value = pd.DataFrame({
            'foreign': ['Hi', 'one', 'two'],
            'content_box2': ['Salut', 'un', 'deux']
        })
        # ----- ACT
        result = interro_api.load_interro_answer(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            'token': token,
            'content_box1': 'two',
            'content_box2': 'deux',
            'count': '1',
            'databaseName': params.databaseName,
            'faultsDict': params.faultsDict,
            'index': 2,
            'interroCategory': params.interroCategory,
            'interroDict': params.interroDict,
            'oldInterroDict': params.oldInterroDict,
            'perf': params.perf,
            'progressPercent': 10,
            'score': params.score,
            'testLength': params.testLength,
            'testType': params.testType
        }
        self.assertEqual(result, expected_dict)

    @patch('src.api.interro.get_attributes_dict')
    @patch('src.api.interro.update_interro')
    @patch('src.api.interro.get_interro')
    def test_get_user_answer_test(
            self,
            mock_get_interro,
            mock_update_interro,
            mock_get_attributes_dict,
        ):
        # ----- ARRANGE
        token = 'mock_token'
        params = MagicMock()
        params['key'] = 'value'
        params['oldInterroDict'] = 'mock_old_interro_dict'
        params['faultsDict'] = 'mock_faults_dict'
        params['databaseName'] = 'mock_db_name'
        params['testType'] = 'mock_test_type'
        mock_get_interro.return_value = 'mock_interro'
        mock_update_interro.return_value = ['mock_interro', 2]
        mock_get_attributes_dict.return_value = {'mock_key': 'mock_value'}
        # ----- ACT
        result = interro_api.get_user_answer(
            token=token,
            params=params,
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        actual_dict = content.decode('utf-8')
        actual_dict = json.loads(actual_dict)
        expected_dict = {'mock_key': 'mock_value'}
        self.assertEqual(actual_dict, expected_dict)
        mock_get_interro.assert_called_once_with(params)
        mock_update_interro.assert_called_once_with('mock_interro', params)
        mock_get_attributes_dict.assert_called_once_with(token, 'mock_interro', params, 2)

    @patch('src.api.interro.save_result')
    def test_propose_rattrap(
            self,
            mock_save_result
        ):
        """
        Should propose a new rattrap test to the user.
        """
        # ----- ARRANGE
        token = 'mock_token'
        params = MagicMock()
        params.databaseName = 'mock_db_name'
        params.faultsDict = {'col_1': [1, 2]}
        params.interroCategory = 'test'
        params.interroDict = {'col_2': [3, 4]}
        params.oldInterroDict = {'col_3': [5, 6]}
        params.score = 3
        params.testType = 'version'
        # ----- ACT
        result = interro_api.propose_rattrap(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            "token": token,
            "databaseName": params.databaseName,
            "faultsDict": params.faultsDict,
            "index": 0,
            "interroCategory": params.interroCategory,
            "interroDict": [],
            "oldInterroDict": params.oldInterroDict,
            "score": params.score,
            "testLength": len(params.interroDict),
            "testType": params.testType,
        }
        self.assertEqual(result, expected_result)
        mock_save_result.assert_called_once_with(token, params)

    @patch('src.api.interro.get_interro_category')
    @patch('src.api.interro.Rattrap')
    @patch('src.api.interro.FastapiGuesser')
    @patch('src.api.interro.get_faults_df')
    @patch('src.api.interro.decode_dict')
    def test_launch_rattrap(
            self,
            mock_decode_dict,
            mock_get_faults_df,
            mock_guesser,
            mock_rattrap,
            mock_get_interro_category
        ):
        """
        Should load the rattrap.
        """
        # ----- ARRANGE
        mock_decode_dict.return_value = pd.DataFrame({'col_1': [1, 2]})
        mock_get_faults_df.return_value = pd.DataFrame({'col_2': [3, 4]})
        token = 'mock_token'
        params = MagicMock()
        params.oldInterroDict = 'mock_old_interro_dict'
        params.faultsDict = 'mock_faults_dict'
        params.databaseName = 'mock_db_name'
        params.testType = 'mock_test_type'
        mock_guesser.return_value = 'mock_guesser'
        mock_rattrap_object = MagicMock()
        mock_rattrap_object.to_dict.return_value = {
            'key': 'value'
        }
        mock_rattrap.return_value = mock_rattrap_object
        mock_get_interro_category.return_value = 'mock_category'
        # ----- ACT
        result = interro_api.launch_rattrap(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        actual_dict = content.decode('utf-8')
        actual_dict = json.loads(actual_dict)
        expected_dict = {
            'count': 0,
            'databaseName': 'mock_db_name',
            'interroCategory': 'mock_category',
            'key': 'value',
            'message': "Rattrap created successfully",
            'score': 0,
            'testType': 'mock_test_type',
            'token': token
        }
        self.assertEqual(actual_dict, expected_dict)
        mock_decode_dict.assert_called_once_with('mock_old_interro_dict')
        mock_get_faults_df.assert_called_once_with('mock_faults_dict')
        mock_guesser.assert_called_once()
        mock_rattrap.assert_called_once()
        mock_get_interro_category.assert_called_once_with(interro=mock_rattrap_object)

    @patch('src.api.interro.turn_df_into_dict')
    @patch('src.api.interro.update_test')
    @patch('src.api.interro.decode_dict')
    def test_end_interro(
            self,
            mock_decode_dict,
            mock_update_test,
            mock_turn_df_into_dict,
        ):
        """
        Should end the interro.
        """
        # ----- ARRANGE
        token = 'mock_token'
        params = MagicMock()
        params.interroCategory = 'test'
        params.interroDict = 'mock_interro_dict'
        params.oldInterroDict = 'mock_old_interro_dict'
        params.testLength = '10'
        params.score = '2'
        mock_decode_dict.return_value = pd.DataFrame()
        mock_turn_df_into_dict.return_value = [['headers'], ['rows']]
        # ----- ACT
        result = interro_api.end_interro(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            'token': token,
            'headers': ['headers'],
            'rows': ['rows'],
            'testLength': '10',
            'score': '2',
        }
        self.assertEqual(result, expected_dict)
        mock_decode_dict.assert_called_once_with('mock_interro_dict')
        mock_turn_df_into_dict.assert_called_once()
        mock_update_test.assert_called_once()

    def test_get_error_messages_fail(self):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = "Empty table"
        # ----- ACT
        result = interro_api.get_error_messages(error_message)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'No words in the selected table')

    def test_get_error_messages_success(self):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = "Settings saved successfully"
        # ----- ACT
        result = interro_api.get_error_messages(error_message)
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
        result = interro_api.get_error_messages(error_message)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, '')

    @patch('src.api.interro.logger')
    def test_get_error_messages_error(self, mock_logger):
        """
        Test the function get_error_messages
        """
        # ----- ARRANGE
        error_message = 'blableblibloblu'
        # ----- ACT
        with self.assertRaises(ValueError):
            interro_api.get_error_messages(error_message)
        # ----- ASSERT
        mock_logger.error.assert_any_call(f"Error message incorrect: {error_message}")
        expected_list = [
            "Empty table",
            "Settings saved successfully",
            ''
        ]
        mock_logger.error.assert_any_call(
            f"Should be in: {expected_list}"
        )

    def test_turn_df_into_dict(self):
        # ----- ARRANGE
        words_df = pd.DataFrame({
            'col_1': ['val_1', 'val_2'],
            'col_2': ['val_3', 'val_4']
        })
        # ----- ACT
        result = interro_api.turn_df_into_dict(words_df)
        # ----- ASSERT
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ['col_1', 'col_2'])
        self.assertEqual(result[1], [['val_1', 'val_3'], ['val_2', 'val_4']])
