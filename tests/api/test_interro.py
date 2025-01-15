"""
    Creator:
        B.Delorme
    Creation date:
        20th April 2024
    Main purpose:
        Test script for
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
from fastapi.responses import JSONResponse

from src.api import interro as interro_api
from src.interro import PremierTest, Rattrap



class TestInterroAPI(unittest.TestCase):
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
        mock_loader_object.test_length = 10
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
            test_length=test_length,
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
        mock_test.test_length = 1
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
        mock_test.test_length = 1
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
        params.testCount = '2'
        params.interroDict = {'foreign': ['zero', 'one', 'two']}
        params.testIndex = '1'
        params.databaseName = ''
        params.faultsDict = {'fault_key': 'fault_value'}
        params.interroCategory = 'test'
        params.message = ''
        params.oldInterroDict = {'old_key': 'old_value'}
        params.testPerf = '0'
        params.testScore = '2'
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
            'contentBox1': 'one',
            'databaseName': params.databaseName,
            'faultsDict': params.faultsDict,
            'interroCategory': params.interroCategory,
            'interroDict': params.interroDict,
            'message': params.message,
            'oldInterroDict': params.oldInterroDict,
            'progressPercent': 20,
            'testCount': 3,
            'testIndex': 1,
            'testPerf': params.testPerf,
            'testScore': params.testScore,
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
        params.testCount = '1'
        params.databaseName = 'mock_db_name'
        params.faultsDict = 'mock_faults_dict'
        params.testIndex = '2'
        params.interroCategory = 'mock_interro_category'
        params.interroDict = 'mock_interro_dict'
        params.oldInterroDict = 'mock_old_interro_dict'
        params.testPerf = 1
        params.testScore = 3
        params.testLength = 10
        params.testType = 'version'
        mock_decode_dict.return_value = pd.DataFrame({
            'foreign': ['Hi', 'one', 'two'],
            'contentBox2': ['Salut', 'un', 'deux']
        })
        # ----- ACT
        result = interro_api.load_interro_answer(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            'contentBox1': 'two',
            'contentBox2': 'deux',
            'databaseName': params.databaseName,
            'faultsDict': params.faultsDict,
            'interroCategory': params.interroCategory,
            'interroDict': params.interroDict,
            'oldInterroDict': params.oldInterroDict,
            'progressPercent': 10,
            'testCount': '1',
            'testIndex': 2,
            'testLength': params.testLength,
            'testPerf': params.testPerf,
            'testScore': params.testScore,
            'testType': params.testType,
            'token': token,
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
        params.testScore = 3
        params.testType = 'version'
        # ----- ACT
        result = interro_api.propose_rattrap(
            token=token,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            "databaseName": params.databaseName,
            "faultsDict": params.faultsDict,
            "testIndex": 0,
            "interroCategory": params.interroCategory,
            "interroDict": [],
            "oldInterroDict": params.oldInterroDict,
            "testLength": len(params.interroDict),
            "testScore": params.testScore,
            "testType": params.testType,
            "token": token,
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
            'databaseName': 'mock_db_name',
            'interroCategory': 'mock_category',
            'key': 'value',
            'message': "Rattrap created successfully",
            'testCount': 0,
            'testScore': 0,
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
        params.testScore = '2'
        mock_decode_dict.return_value = pd.DataFrame({
            'foreign': ['zero', 'one', 'two'],
            'native': ['zero', 'un', 'deux'],
            'col_1': ['val_1', 'val_2', 'val_3']
        })
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
            'testScore': '2',
        }
        self.assertEqual(result, expected_dict)
        mock_decode_dict.assert_called_once_with('mock_interro_dict')
        mock_turn_df_into_dict.assert_called_once()
        mock_update_test.assert_called_once()

    @patch('src.api.interro.turn_df_into_dict')
    @patch('src.api.interro.decode_dict')
    def test_end_interro_rattrap(
            self,
            mock_decode_dict,
            mock_turn_df_into_dict,
        ):
        """
        Should end the interro.
        """
        # ----- ARRANGE
        token = 'mock_token'
        params = MagicMock()
        params.interroCategory = 'rattrap'
        params.interroDict = 'mock_interro_dict'
        params.oldInterroDict = 'mock_old_interro_dict'
        params.testLength = '10'
        params.testScore = '2'
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
            'headers': ['headers'],
            'rows': ['rows'],
            'testLength': '10',
            'testScore': '2',
            'token': token,
        }
        self.assertEqual(result, expected_dict)
        mock_decode_dict.assert_called_once_with('mock_old_interro_dict')
        mock_turn_df_into_dict.assert_called_once()



class TestHelper(unittest.TestCase):
    """
    Designed to test all back-end functions of the API use case.
    """
    @patch('ast.literal_eval')
    def test_get_old_interro_dict(self, mock_literal_eval):
        # ----- ARRANGE
        interro_dict = {
            'foreign': ['zero', 'one', 'two'],
            'native': ['zero', 'un', 'deux']
        }
        # ----- ACT
        result = interro_api.get_old_interro_dict(interro_dict)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        expected_result = ''.join([
            '[{"foreign":"zero","native":"zero"}',
            ',',
            '{"foreign":"one","native":"un"}',
            ',',
            '{"foreign":"two","native":"deux"}]'
        ])
        self.assertEqual(result, expected_result)

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

    def test_get_interro_category(self):
        # ----- ARRANGE
        interro = PremierTest(
            interro_df=pd.DataFrame({'col_1': ['val_1', 'val_2']}),
            test_length=10,
            guesser=MagicMock()
        )
        # ----- ACT
        result = interro_api.get_interro_category(interro)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'test')

    def test_get_interro_category_rattrap(self):
        # ----- ARRANGE
        interro = Rattrap(
            interro_df=pd.DataFrame({'col_1': ['val_1', 'val_2']}),
            guesser=MagicMock(),
            old_interro_df=pd.DataFrame({'col_2': ['val_3', 'val_4']}),
        )
        # ----- ACT
        result = interro_api.get_interro_category(interro)
        # ----- ASSERT
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'rattrap')

    @patch('src.api.interro.logger')
    def test_get_interro_category_error(self, mock_logger):
        # ----- ARRANGE
        interro = 'mock_interro'
        # ----- ACT
        # ----- ASSERT
        with self.assertRaises(ValueError):
            interro_api.get_interro_category(interro)
            self.assertEqual(mock_logger.error.call_count, 2)
            mock_logger.error.assert_any_call(
                "Unknown interro object, should have either a perf or a rattrap attribute!"
            )
            mock_logger.error.assert_any_call(
                f"Interro object: {type(interro)}"
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

    def test_decode_dict(self):
        # ----- ARRANGE
        interro_dict = {
            'foreign': ['zero', 'one', 'two'],
            'native': ['zero', 'un', 'deux']
        }
        # ----- ACT
        result = interro_api.decode_dict(interro_dict)
        # ----- ASSERT
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (3, 2))
        pd.testing.assert_frame_equal(result, pd.DataFrame(interro_dict))

    def test_decode_dict_creation_date(self):
        # ----- ARRANGE
        interro_dict = {
            'foreign': ['zero', 'one', 'two'],
            'native': ['zero', 'un', 'deux'],
            'creation_date': [12789033445, 12785033445, 12786033445],
            'index': [0, 1, 2]
        }
        # ----- ACT
        result = interro_api.decode_dict(interro_dict)
        # ----- ASSERT
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (3, 3))
        expected_df = pd.DataFrame({
            'foreign': ['zero', 'one', 'two'],
            'native': ['zero', 'un', 'deux'],
            'creation_date': ["1970-05-29", "1970-05-28", "1970-05-28"]
        })
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('src.api.interro.pd.to_datetime')
    def test_decode_dict_error(self, mock_to_datetime):
        # ----- ARRANGE
        interro_dict = {
            'foreign': ['zero', 'one', 'two'],
            'native': ['zero', 'un', 'deux'],
            'creation_date': [12789033445, 12785033445, 12786033445],
        }
        mock_to_datetime.side_effect = ValueError()
        # ----- ACT
        result = interro_api.decode_dict(interro_dict)
        # ----- ASSERT
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (3, 3))
        expected_df = pd.DataFrame(interro_dict)
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('src.api.interro.decode_dict')
    def test_get_faults_df(self, mock_decode_dict):
        # ----- ARRANGE
        expected_df = pd.DataFrame({'col_1': ['val_1', 'val_2']})
        mock_decode_dict.return_value = expected_df
        # ----- ACT
        result = interro_api.get_faults_df('mock_faults_dict')
        # ----- ASSERT
        pd.testing.assert_frame_equal(result, expected_df)

    def test_get_faults_df_none(self):
        # ----- ARRANGE
        # ----- ACT
        result = interro_api.get_faults_df({'key': 'val'})
        # ----- ASSERT
        expected_df = pd.DataFrame(columns=['foreign', 'native'])
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('src.api.interro.get_faults_df')
    @patch('src.api.interro.decode_dict')
    def test_get_interro_test(
            self,
            mock_decode_dict,
            mock_get_faults_df
        ):
        # ----- ARRANGE
        params = MagicMock()
        params.interroDict = 'mock_interro_dict'
        params.faultsDict = 'mock_faults_dict'
        params.testIndex = '3'
        params.interroCategory = 'test'
        params.testLength = '10'
        params.testPerf = '1'
        mock_decode_dict.return_value = pd.DataFrame({'col_1': ['val_1', 'val_2']})
        mock_get_faults_df.return_value = pd.DataFrame({'col_2': ['val_3', 'val_4']})
        # ----- ACT
        result = interro_api.get_interro(params)
        # ----- ASSERT
        self.assertIsInstance(result, PremierTest)

    @patch('src.api.interro.Rattrap')
    @patch('src.api.interro.FastapiGuesser')
    @patch('src.api.interro.decode_dict')
    def test_get_interro_rattrap(
            self,
            mock_decode_dict,
            mock_guesser,
            mock_rattrap
        ):
        # ----- ARRANGE
        params = MagicMock()
        params.interroDict = 'mock_interro_dict'
        params.faultsDict = 'mock_faults_dict'
        params.testIndex = '3'
        params.interroCategory = 'rattrap'
        params.testLength = '10'
        params.testPerf = '1'
        mock_decode_dict.return_value = pd.DataFrame({'col_1': ['val_1', 'val_2']})
        mock_guesser.return_value = 'mock_guesser'
        mock_rattrap_object = MagicMock()
        mock_rattrap.return_value = mock_rattrap_object
        # ----- ACT
        result = interro_api.get_interro(params)
        # ----- ASSERT
        self.assertIsInstance(result, MagicMock)
        mock_rattrap.assert_called_once()
        mock_rattrap_object.reshuffle_words_table.assert_called_once()

    @patch('src.api.interro.logger')
    @patch('src.api.interro.decode_dict')
    def test_get_interro_error(
            self,
            mock_decode_dict,
            mock_logger
        ):
        # ----- ARRANGE
        params = MagicMock()
        params.interroDict = 'mock_interro_dict'
        params.interroCategory = 'bizarre_bizarre'
        mock_decode_dict.return_value = pd.DataFrame({'col_1': ['val_1', 'val_2']})
        # ----- ACT
        # ----- ASSERT
        with self.assertRaises(ValueError):
            interro_api.get_interro(params)
            mock_logger.error.assert_called_once_with(
                "Unknown interro category: bizarre_bizarre"
            )

    def test_update_interro_guessed(self):
        # ----- ARRANGE
        interro = MagicMock()
        params= MagicMock()
        params.userAnswer = 'Yes'
        params.interroCategory = 'test'
        params.interroDict = 'mock_interro_dict'
        params.testCount = 9
        params.testIndex = '3'
        params.testScore = '1'
        params.testLength = 10
        # ----- ACT
        result = interro_api.update_interro(
            interro=interro,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], MagicMock)
        self.assertEqual(result[1], 2)
        interro.update_interro_df.assert_called_once_with(
            word_guessed=True
        )
        interro.update_index.assert_called_once()

    @patch('src.api.interro.decode_dict')
    def test_update_interro_not_guessed(self, mock_decode_dict):
        # ----- ARRANGE
        interro = MagicMock()
        params= MagicMock()
        params.testIndex = '2'
        params.interroDict = 'mock_interro_dict'
        params.testScore = '1'
        params.userAnswer = 'No'
        params.testCount = 9
        params.testLength = 10
        params.interroCategory = 'test'
        mock_decode_dict.return_value = pd.DataFrame({
            'foreign': ['one', 'two', 'three'],
            'native': ['un', 'deux', 'trois']
        })
        # ----- ACT
        result = interro_api.update_interro(
            interro=interro,
            params=params
        )
        # ----- ASSERT
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], MagicMock)
        self.assertEqual(result[1], 1)
        interro.update_faults_df.assert_called_once_with(
            word_guessed=False,
            row=['three', 'trois']
        )
        interro.update_interro_df.assert_called_once_with(
            word_guessed=False
        )
        interro.update_index.assert_called_once()

    def test_get_attributes_dict(self):
        # ----- ARRANGE
        token = 'mock_token'
        interro = MagicMock()
        interro.to_dict.return_value = {
            'mock_key': 'mock_value'
        }
        params = MagicMock()
        params.databaseName = 'mock_db_name'
        params.interroCategory = 'not_a_test'
        params.oldInterroDict = 'mock_old_interro_dict'
        params.testCount = '2'
        params.testType = 'mock_test_type'
        score = 3
        # ----- ACT
        result = interro_api.get_attributes_dict(
            token=token,
            interro=interro,
            params=params,
            score=score
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            'databaseName': 'mock_db_name',
            'interroCategory': 'not_a_test',
            'message': "User response stored successfully",
            'mock_key': 'mock_value',
            'oldInterroDict': 'mock_old_interro_dict',
            'testCount': '2',
            'testIndex': 0,
            'testScore': 3,
            'testType': 'mock_test_type',
            'token': token,
        }
        self.assertEqual(result, expected_dict)
        interro.to_dict.assert_called_once()

    @patch('src.api.interro.Updater')
    @patch('src.api.interro.Loader')
    @patch('src.api.interro.DbQuerier')
    @patch('src.api.interro.get_user_name_from_token')
    @patch('src.api.interro.PremierTest')
    @patch('src.api.interro.get_faults_df')
    @patch('src.api.interro.decode_dict')
    def test_save_result(
            self,
            mock_decode_dict,
            mock_get_faults_df,
            mock_premier_test,
            mock_get_user_name_from_token,
            mock_db_querier,
            mock_loader,
            mock_updater
        ):
        # ----- ARRANGE
        token = 'mock_token'
        params = MagicMock()
        params.databaseName = 'mock_db_name'
        params.faultsDict = 'mock_faults_dict'
        params.interroDict = 'mock_interro_dict'
        params.testIndex = 'mock_index'
        params.testPerf = 'mock_perf'
        params.testType = 'mock_test_type'
        params.testLength = 'mock_test_length'
        mock_decode_dict.return_value = pd.DataFrame({'col_1': ['val_1', 'val_2']})
        mock_get_faults_df.return_value = pd.DataFrame({'col_2': ['val_3', 'val_4']})
        mock_premier_test_object = MagicMock()
        mock_premier_test.from_dict.return_value = mock_premier_test_object
        mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_db_querier.return_value = 'mock_db_querier'
        mock_loader_object = MagicMock()
        mock_loader.return_value = mock_loader_object
        mock_updater_object = MagicMock()
        mock_updater.return_value = mock_updater_object
        # ----- ACT
        interro_api.save_result(
            token=token,
            params=params
        )
        # ----- ASSERT
        mock_decode_dict.assert_called_once_with('mock_interro_dict')
        mock_get_faults_df.assert_called_once_with('mock_faults_dict')
        mock_premier_test.from_dict.assert_called_once()
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_db_querier.assert_called_once_with(
            user_name='mock_user_name',
            db_name='mock_db_name',
            test_type='mock_test_type'
        )
        mock_loader.assert_called_once_with(
            test_length='mock_test_length',
            data_querier='mock_db_querier'
        )
        mock_loader_object.load_tables.assert_called_once()
        mock_updater.assert_called_once_with(
            loader=mock_loader_object,
            interro=mock_premier_test_object,
        )
        mock_updater_object.update_data.assert_called_once_with()

    @patch('src.api.interro.Updater')
    @patch('src.api.interro.Loader')
    @patch('src.api.interro.DbQuerier')
    @patch('src.api.interro.get_user_name_from_token')
    @patch('src.api.interro.PremierTest')
    @patch('src.api.interro.get_faults_df')
    def test_update_test(
            self,
            mock_get_faults_df,
            mock_premier_test,
            mock_get_user_name_from_token,
            mock_db_querier,
            mock_loader,
            mock_updater
        ):
        # ----- ARRANGE
        params = MagicMock()
        params.databaseName = 'mock_db_name'
        params.faultsDict = 'mock_faults_dict'
        params.testIndex = 'mock_index'
        params.testLength = 'mock_test_length'
        params.testPerf = 'mock_perf'
        params.testType = 'mock_test_type'
        interro_df = MagicMock()
        token = 'mock_token'
        mock_get_faults_df.return_value = pd.DataFrame({'col_2': ['val_3', 'val_4']})
        mock_premier_test_object = MagicMock()
        mock_premier_test.from_dict.return_value = mock_premier_test_object
        mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_db_querier.return_value = 'mock_db_querier'
        mock_loader_object = MagicMock()
        mock_loader.return_value = mock_loader_object
        mock_updater_object = MagicMock()
        mock_updater.return_value = mock_updater_object
        # ----- ACT
        interro_api.update_test(
            token=token,
            params=params,
            interro_df=interro_df
        )
        # ----- ASSERT
        mock_get_faults_df.assert_called_once_with(params.faultsDict)
        mock_premier_test.from_dict.assert_called_once()
        mock_get_user_name_from_token.assert_called_once_with(token=token)
        mock_db_querier.assert_called_once_with(
            user_name='mock_user_name',
            db_name='mock_db_name',
            test_type='mock_test_type'
        )
        mock_loader.assert_called_once_with(
            test_length='mock_test_length',
            data_querier='mock_db_querier'
        )
        mock_loader_object.load_tables.assert_called_once()
        mock_updater.assert_called_once_with(
            loader=mock_loader_object,
            interro=mock_premier_test_object,
        )
        mock_updater_object.update_data.assert_called_once_with()
