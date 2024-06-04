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
# from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import interro as interro_api
from src.data.database_interface import DbManipulator
from src.interro import PremierTest, Rattrap, Loader
from src.views import api as api_view


class TestInterro(unittest.TestCase):
    """
    Test class for interro.py
    """
    @patch('src.interro.PremierTest.set_interro_df')
    @patch('src.api.interro.adjust_test_length')
    @patch('src.interro.Loader')
    @patch('src.api.interro.database_interface.check_test_type')
    def test_load_test(
            self,
            mock_check_test_type,
            mock_loader,
            mock_adjust_test_length,
            mock_set_interro_df
        ):
        """
        Should instanciate a data loader and a corresponding PremierTest object.
        """
        # ----- ARRANGE
        user_name = 'mock_user_name'
        db_name = 'mock_db_name'
        test_type = 'mock_test_type'
        test_length = 10
        mock_loader = MagicMock()
        mock_loader.tables = {
            'mock_test_type_voc': pd.DataFrame(),
            'mock_test_type_perf': pd.DataFrame(),
            'mock_test_type_words_count': pd.DataFrame()
        }
        mock_loader.load_tables.return_value = True
        mock_check_test_type.return_value = True
        mock_adjust_test_length.side_effect = lambda arg1, arg2: arg1
        mock_set_interro_df.return_value = True
        # ----- ACT
        result = interro_api.load_test(
            user_name,
            db_name,
            test_type,
            test_length
        )
        # ----- ASSERT
        self.assertEqual(len(result), 2)
        mock_check_test_type.assert_any_call(test_type)
        # mock_loader.load_tables.assert_called_once()
        mock_adjust_test_length.assert_called_once()
        mock_set_interro_df.assert_called_once()
        self.assertIsInstance(result[0], MagicMock)
        self.assertIsInstance(result[1], PremierTest)

    def test_adjust_test_length(self):
        """
        Test adjust_test_length function
        """
        # ----- ARRANGE
        test_length = 10
        words_table = pd.DataFrame({
            'some_column': [1, 2, 3, 4, 5],
        })
        loader_ = MagicMock()
        loader_.test_type = 'test_type'
        loader_.tables = {'test_type_voc': words_table}
        # ----- ACT
        result = interro_api.adjust_test_length(test_length, loader_)
        # ----- ASSERT
        self.assertEqual(result, 5)

    def test_adjust_test_length_small_table(self):
        """
        Test adjust_test_length function
        """
        # ----- ARRANGE
        test_length = 4
        loader_ = MagicMock()
        words_table = pd.DataFrame(
            {
                'some_column': ['value_1', 'value_2', 'value_3'],
            }
        )
        loader_ = MagicMock()
        loader_.test_type = 'test_type'
        loader_.tables = {
            'test_type_voc': words_table
        }
        # ----- ACT
        result = interro_api.adjust_test_length(test_length, loader_)
        # ----- ASSERT
        self.assertEqual(result, 3)

    def test_adjust_test_length_empty_table(self):
        """
        Test adjust_test_length function
        """
        # ----- ARRANGE
        test_length = 4
        loader_ = MagicMock()
        words_table = pd.DataFrame()
        loader_ = MagicMock()
        loader_.test_type = 'test_type'
        loader_.tables = {
            'test_type_voc': words_table
        }
        # ----- ACT
        # ----- ASSERT
        with self.assertRaises(ValueError):
            interro_api.adjust_test_length(test_length, loader_)

    @patch('src.api.interro.get_error_messages')
    @patch('src.api.database.get_user_databases')
    def test_get_interro_settings(
            self,
            mock_get_user_databases,
            mock_get_error_messages
        ):
        """
        Test get_interro_settings function
        """
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        error_message = 'mock_error_message'
        db_message = ('mock_db_message')
        mock_get_error_messages.return_value = db_message
        mock_get_user_databases.return_value = ['db1', 'db2']
        # ----- ACT
        result = interro_api.get_interro_settings(request, token, error_message)
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        self.assertEqual(
            result,
            {
                'request': 'mock_request',
                'token': 'mock_token',
                'databases': ['db1', 'db2'],
                'emptyTableErrorMessage': db_message,
            }
        )
        mock_get_user_databases.assert_called_once_with(token)
        mock_get_error_messages.assert_called_once_with(error_message)

    @patch('src.api.interro.save_loader_in_redis')
    @patch('src.api.interro.save_interro_in_redis')
    @patch('src.api.interro.load_test')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_save_interro_settings(
            self,
            mock_get_user_name_from_token,
            mock_load_test,
            mock_save_interro_in_redis,
            mock_save_loader_in_redis
        ):
        """
        Test save_interro_settings function
        """
        # ----- ARRANGE
        settings = {
            'databaseName': 'mock_db_name',
            'testType': 'mock_test_type',
            'numWords': '2',
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_test = MagicMock()
        mock_test.words = 1
        mock_load_test.return_value = ('mock_loader', mock_test)
        mock_save_interro_in_redis.return_value = True
        mock_save_loader_in_redis.return_value = True
        # ----- ACT
        result = interro_api.save_interro_settings(settings, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        assert content_dict['message'] == "Settings saved successfully"
        assert content_dict['token'] == token

    @patch('src.api.interro.load_test')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_save_interro_settings_empty_table(
            self,
            mock_get_user_name_from_token,
            mock_load_test,
        ):
        """
        Test save_interro_settings function
        """
        # ----- ARRANGE
        settings = {
            'databaseName': 'mock_db_name',
            'testType': 'mock_test_type',
            'numWords': '2',
        }
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_test = MagicMock()
        mock_test.words = 1
        mock_load_test.side_effect = ValueError()
        # ----- ACT
        result = interro_api.save_interro_settings(
            settings,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        assert content_dict['message'] == "Empty table"
        assert content_dict['token'] == token

    @patch('src.api.interro.load_interro_from_redis')
    @patch('src.api.authentication.get_user_name_from_token')
    def test_get_interro_question(
            self,
            mock_get_user_name_from_token,
            mock_load_interro_from_redis
        ):
        # ----- ARRANGE
        interro_category = 'mock_category'
        request = 'mock_request'
        total = 10
        count = 1
        score = 3
        token = 'mock_token'
        mock_get_user_name_from_token.return_value = 'mock_user_name'
        mock_interro_df = pd.DataFrame(
            {
                'english': ['Hi', 'Hello', 'Goodbye'],
            },
            index=[0, 1, 2]
        )
        mock_test = PremierTest(
            words_df_=pd.DataFrame(),
            words=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.interro_df = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_test
        # ----- ACT
        result = interro_api.get_interro_question(
            request,
            interro_category,
            total,
            count,
            score,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        self.assertEqual(
            result,
            {
                "request": request,
                'token': token,
                "numWords": total,
                "interroCategory": interro_category,
                "userName": 'mock_user_name',
                "count": count + 1,
                "score": score,
                "progressPercent": int(count / int(total) * 100),
                "content_box1": 'Hello'
            }
        )
        mock_load_interro_from_redis.assert_called_once_with(
            token=token,
            interro_category=interro_category
        )

    @patch('src.api.interro.load_interro_from_redis')
    def test_load_interro_answer(self, mock_load_interro_from_redis):
        # ----- ARRANGE
        request = 'mock_request'
        interro_category = 'mock_category'
        total = 10
        count = 1
        score = 3
        token = 'mock_token'
        mock_interro_df = pd.DataFrame(
            {
                'english': ['Hi', 'Hello', 'Goodbye'],
                'french': ['Salut', 'Bonjour', 'Au revoir']
            },
            index=[0, 1, 2]
        )
        mock_test = PremierTest(
            words_df_=pd.DataFrame(),
            words=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.interro_df = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_test
        # ----- ACT
        result = interro_api.load_interro_answer(
            request,
            interro_category,
            total,
            count,
            score,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        self.assertEqual(
            result,
            {
                "request": request,
                "token": token,
                "interroCategory": interro_category,
                "numWords": total,
                "count": count,
                "score": score,
                "progressPercent": int(count / int(total) * 100),
                "content_box1": 'Hi',
                "content_box2": 'Salut'
            }
        )
        mock_load_interro_from_redis.assert_called_once_with(
            token=token,
            interro_category=interro_category
        )

    @patch('src.api.interro.save_interro_in_redis')
    @patch('src.interro.PremierTest.update_voc_df')
    @patch('src.api.interro.load_interro_from_redis')
    def test_get_user_answer_test_yes(
            self,
            mock_load_interro_from_redis,
            mock_update_voc_df,
            mock_save_interro_in_redis
        ):
        # ----- ARRANGE
        token = 'mock_token'
        interro_category = 'test'
        data = {
            'score': '10',
            'answer': 'Yes',
            'interroCategory': interro_category,
        }
        mock_interro_df = pd.DataFrame(
            {
                'some_column': ['some_value'],
            }
        )
        mock_test = PremierTest(
            words_df_=pd.DataFrame(),
            words=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.interro_df = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_test
        mock_update_voc_df.return_value = True
        mock_save_interro_in_redis.return_value = True
        # ----- ACT
        result = interro_api.get_user_answer(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(
            content_dict,
            {
                'message': 'User response stored successfully',
                'token': 'mock_token',
                'interroCategory': interro_category,
                'score': 11,
            }
        )
        mock_load_interro_from_redis.assert_called_once_with(
            token=token,
            interro_category=interro_category
        )
        mock_update_voc_df.assert_called_once_with(True)
        mock_save_interro_in_redis.assert_called_once_with(
            interro=mock_test,
            token=token,
            interro_category=interro_category
        )

    @patch('src.api.interro.save_interro_in_redis')
    @patch('src.interro.PremierTest.update_faults_df')
    @patch('src.interro.PremierTest.update_voc_df')
    @patch('src.api.interro.load_interro_from_redis')
    def test_get_user_answer_test_no(
            self,
            mock_load_interro_from_redis,
            mock_update_voc_df,
            mock_update_faults_df,
            mock_save_interro_in_redis
        ):
        # ----- ARRANGE
        interro_category = 'test'
        data = {
            'score': '10',
            'answer': 'No',
            'english': 'Hello',
            'french': 'Bonjour',
            'interroCategory': interro_category
        }
        token = 'mock_token'
        mock_interro_df = pd.DataFrame(
            {
                'some_column': ['some_value'],
            }
        )
        mock_test = PremierTest(
            words_df_=pd.DataFrame(),
            words=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.interro_df = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_test
        mock_update_voc_df.return_value = True
        mock_update_faults_df.return_value = True
        mock_save_interro_in_redis.return_value = True
        # ----- ACT
        result = interro_api.get_user_answer(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(
            content_dict,
            {
                'message': 'User response stored successfully',
                'token': token,
                'interroCategory': interro_category,
                'score': 10,
            }
        )
        mock_load_interro_from_redis.assert_called_once_with(
            token=token,
            interro_category=interro_category
        )
        mock_update_faults_df.assert_called_once_with(False, ['Hello', 'Bonjour'])
        mock_update_voc_df.assert_called_once_with(False)
        mock_save_interro_in_redis.assert_called_once_with(
            interro=mock_test,
            token=token,
            interro_category=interro_category
        )

    @patch('src.api.interro.save_interro_in_redis')
    @patch('src.interro.PremierTest.update_voc_df')
    @patch('src.api.interro.load_interro_from_redis')
    def test_get_user_answer_rattraps_yes(
            self,
            mock_load_interro_from_redis,
            mock_update_voc_df,
            mock_save_interro_in_redis
        ):
        # ----- ARRANGE
        interro_category = 'rattrap'
        data = {
            'score': '10',
            'answer': 'Yes',
            'english': 'Hello',
            'french': 'Bonjour',
            'interroCategory': interro_category
        }
        token = 'mock_token'
        mock_interro_df = pd.DataFrame(
            {
                'some_column': ['some_value'],
            }
        )
        mock_rattrap = Rattrap(
            faults_df_=pd.DataFrame(),
            rattraps=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_rattrap.interro_df = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_rattrap
        mock_update_voc_df.return_value = True
        mock_save_interro_in_redis.return_value = True
        # ----- ACT
        result = interro_api.get_user_answer(
            data,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        self.assertEqual(
            content_dict,
            {
                'message': 'User response stored successfully',
                'token': token,
                'interroCategory': interro_category,
                'score': 11,
            }
        )
        mock_load_interro_from_redis.assert_called_once_with(
            token=token,
            interro_category=interro_category
        )
        assert not mock_update_voc_df.called
        mock_save_interro_in_redis.assert_called_once_with(
            interro=mock_rattrap,
            token=token,
            interro_category=interro_category
        )

    @patch('src.interro.logger')
    @patch('src.interro.Updater.update_data')
    @patch('src.api.interro.load_loader_from_redis')
    @patch('src.interro.PremierTest.compute_success_rate')
    @patch('src.api.interro.load_interro_from_redis')
    def test_propose_rattraps(
            self,
            mock_load_interro_from_redis,
            mock_compute_success_rate,
            mock_load_loader_from_redis,
            mock_update_data,
            mock_logger
        ):
        """
        Should propose a new rattraps test to the user.
        """
        # ----- ARRANGE
        request = 'mock_request'
        total = 10
        score = 3
        token = 'mock_token'
        interro_category = 'test'
        mock_interro_df = pd.DataFrame(
            {
                'some_column': ['some_value'],
            }
        )
        mock_faults_df = pd.DataFrame(
            {
                'some_column_1': ['some_value_1', 'some_value_3'],
                'some_column_2': ['some_value_2', 'some_value_4'],
            }
        )
        mock_test = PremierTest(
            words_df_=pd.DataFrame(),
            words=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.interro_df = mock_interro_df
        mock_test.faults_df = mock_faults_df
        mock_load_interro_from_redis.return_value = mock_test
        mock_compute_success_rate.return_value = True
        mock_db_interface = DbManipulator(
            'mock_user_name',
            'mock_db_name',
            'version'
        )
        mock_loader = Loader(mock_db_interface)
        mock_load_loader_from_redis.return_value = mock_loader
        mock_update_data.return_value = True
        # ----- ACT
        result = interro_api.propose_rattraps(
            request,
            interro_category,
            total,
            score,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            "request": request,
            "token": token,
            "interroCategory": interro_category,
            "newTotal": 2,
            "newScore": 0,
            "newCount": 0,
            "score": score,
            "numWords": total
        }
        self.assertEqual(result, expected_result)
        mock_load_interro_from_redis.assert_called_once_with(
            token=token,
            interro_category=interro_category
        )
        mock_compute_success_rate.assert_called_once()
        mock_load_loader_from_redis.assert_called_once_with(token=token)
        mock_update_data.assert_called_once()
        # mock_logger.info.assert_called_once_with("User data updated.")

    @patch('src.interro.PremierTest.compute_success_rate')
    @patch('src.api.interro.load_interro_from_redis')
    def test_propose_rattraps_rattraps(
            self,
            mock_load_interro_from_redis,
            mock_compute_success_rate
        ):
        """
        Should propose a new rattraps test to the user.
        """
        # ----- ARRANGE
        request = 'mock_request'
        total = 10
        score = 3
        token = 'mock_token'
        interro_category = 'mock_category'
        mock_faults_df_ = pd.DataFrame(
            {
                'some_column_1': ['some_value_1', 'some_value_3'],
                'some_column_2': ['some_value_2', 'some_value_4'],
            }
        )
        mock_rattrap = Rattrap(
            faults_df_=mock_faults_df_,
            rattraps=2,
            guesser=api_view.FastapiGuesser(),
        )
        mock_load_interro_from_redis.return_value = mock_rattrap
        mock_compute_success_rate.return_value = True
        # ----- ACT
        result = interro_api.propose_rattraps(
            request,
            interro_category,
            total,
            score,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            "request": request,
            "token": token,
            "interroCategory": interro_category,
            "newTotal": 0,
            "newScore": 0,
            "newCount": 0,
            "score": score,
            "numWords": total
        }
        self.assertEqual(result, expected_result)
        mock_load_interro_from_redis.assert_called_once_with(
            token=token,
            interro_category=interro_category
        )
        assert mock_compute_success_rate.called is False

    @patch('src.api.interro.save_interro_in_redis')
    @patch('src.api.interro.load_interro_from_redis')
    def test_load_rattraps(
            self,
            mock_load_interro_from_redis,
            mock_save_interro_in_redis,
        ):
        """
        Should load the rattraps.
        """
        # ----- ARRANGE
        token = 'mock_token'
        new_interro_category = 'mock_category'
        data = {
            'count': '2',
            'total': '10',
            'score': '3',
            'interroCategory': new_interro_category
        }
        mock_interro_df = pd.DataFrame(
            {
                'some_column': ['some_value'],
            }
        )
        mock_test = PremierTest(
            words_df_=pd.DataFrame(),
            words=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.interro_df = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_test
        mock_save_interro_in_redis.return_value = True
        # ----- ACT
        result = interro_api.load_rattraps(
            token,
            data
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        actual_dict = content.decode('utf-8')
        actual_dict = json.loads(actual_dict)
        expected_dict = {
            'message': "Rattraps created successfully",
            'token': token,
            'interroCategory': 'rattrap',
            'total': int(data['total']),
            'score': int(data['score']),
            'count': int(data['count'])
        }
        self.assertEqual(actual_dict, expected_dict)

    @patch('src.api.interro.save_interro_in_redis')
    @patch('src.api.interro.load_interro_from_redis')
    def test_load_rattraps_rattraps(
            self,
            mock_load_interro_from_redis,
            mock_save_interro_in_redis,
        ):
        """
        Should load the rattraps.
        """
        # ----- ARRANGE
        token = 'mock_token'
        interro_category = 'rattrap'
        data = {
            'count': '2',
            'total': '10',
            'score': '3',
            'interroCategory': interro_category
        }
        mock_interro_df = pd.DataFrame(
            {
                'some_column': ['some_value'],
            }
        )
        mock_test = Rattrap(
            faults_df_=pd.DataFrame(),
            rattraps=2,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.faults_df_ = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_test
        mock_save_interro_in_redis.return_value = True
        # ----- ACT
        result = interro_api.load_rattraps(
            token,
            data
        )
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        actual_dict = content.decode('utf-8')
        actual_dict = json.loads(actual_dict)
        expected_dict = {
            'message': "Rattraps created successfully",
            'token': token,
            'interroCategory': 'rattrap',
            'total': int(data['total']),
            'score': int(data['score']),
            'count': int(data['count'])
        }
        self.assertEqual(actual_dict, expected_dict)

    @patch('src.api.interro.turn_df_into_dict')
    @patch('src.interro.Updater.update_data')
    @patch('src.api.interro.load_loader_from_redis')
    @patch('src.api.interro.load_interro_from_redis')
    @patch('src.interro.logger')
    def test_end_interro(
            self,
            mock_logger,
            mock_load_interro_from_redis,
            mock_load_loader_from_redis,
            mock_update_data,
            mock_turn_df_into_dict,
        ):
        """
        Should end the interro.
        """
        # ----- ARRANGE
        interro_category = 'test'
        request = 'mock_request'
        total = '10'
        score = '2'
        token = 'mock_token'
        mock_interro_df = pd.DataFrame(
            {
                'some_column': ['some_value'],
            }
        )
        mock_test = PremierTest(
            words_df_=pd.DataFrame(),
            words=10,
            guesser=api_view.FastapiGuesser(),
        )
        mock_test.interro_df = mock_interro_df
        mock_load_interro_from_redis.return_value = mock_test
        mock_db_interface = DbManipulator(
            'mock_user_name',
            'mock_db_name',
            'version'
        )
        mock_loader = Loader(mock_db_interface)
        mock_load_loader_from_redis.return_value = mock_loader
        mock_update_data.return_value = True
        mock_turn_df_into_dict.return_value = (
            ['header_1', 'header_2'],
            ['row_1', 'row_2', 'row_3']
        )
        # ----- ACT
        result = interro_api.end_interro(
            request,
            interro_category,
            total,
            score,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            "request": request,
            "token": token,
            "headers": ['header_1', 'header_2'],
            "rows": ['row_1', 'row_2', 'row_3'],
            "score": score,
            "numWords": total,
        }
        self.assertEqual(result, expected_dict)
        assert mock_load_interro_from_redis.call_count == 2
        mock_load_interro_from_redis.any_call_with(
            token=token,
            interro_category=interro_category
        )
        mock_load_interro_from_redis.any_call_with(
            token=token,
            interro_category=interro_category
        )
        mock_load_loader_from_redis.assert_called_once_with(token=token)
        mock_update_data.assert_called_once()
        # mock_logger.info.assert_called_once_with("User data updated.")

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
