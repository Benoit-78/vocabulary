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
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
from fastapi.responses import JSONResponse
# from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import guest as guest_api
from src.interro import PremierTest
from src.views import api as api_view



class TestGuest(unittest.TestCase):
    """
    Test the functions in the module guest.py
    """
    def test_get_flags_dict(self):
        """
        Test the function get_flags_dict
        """
        # ----- ARRANGE
        mock_json = {
            "en": {"flag": "1"},
            "fr": {"flag": "2"},
            "es": {"flag": "3"}
        }
        # ----- ACT
        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_json)
            ):
            result = guest_api.get_flags_dict()
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        self.assertIn('fr', result)
        self.assertIn('en', result)
        self.assertIn('es', result)
        self.assertNotIn('it', result)

    @patch('src.api.guest.get_flags_dict')
    def test_load_guest_settings(self, mock_get_flags_dict):
        # ----- ARRANGE
        request = 'mock_request'
        token = 'mock_token'
        mock_get_flags_dict.return_value = {
            'en': '1',
            'fr': '2',
            'es': '3'
        }
        # ----- ACT
        result = guest_api.load_guest_settings(request, token)
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            'en': '1',
            'fr': '2',
            'es': '3',
            'request': request,
            'token': token
        }
        self.assertEqual(result, expected_dict)
        mock_get_flags_dict.assert_called_once()

    @patch.dict(os.environ, {'VOC_GUEST_NAME': 'some_name'})
    @patch('src.api.guest.save_test_in_redis')
    @patch('src.api.guest.load_test')
    def test_save_interro_settings_guest(
            self,
            mock_load_test,
            mock_save_test_in_redis
        ):
        # ----- ARRANGE
        language = {
            'language': 'klingon'
        }
        token = 'mock_token'
        mock_load_test.return_value = 'mock_loader', 'mock_test'
        mock_save_test_in_redis.return_value = True
        # ----- ACT
        result = guest_api.save_interro_settings_guest(language, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'message': "Guest user settings stored successfully",
            'token': token
        }
        self.assertEqual(content_dict, expected_result)
        mock_load_test.assert_called_once_with(
            user_name='some_name',
            db_name='klingon',
            test_type='version',
            test_length=10
        )
        mock_save_test_in_redis.assert_called_once_with('mock_test', token)

    @patch('src.api.guest.get_flags_dict')
    @patch('src.api.guest.load_test_from_redis')
    def test_load_interro_question_guest(
            self,
            mock_load_test_from_redis,
            mock_get_flags_dict
        ):
        # ----- ARRANGE
        request = 'mock_request'
        words = 10
        count = 2
        score = 1
        language = 'klingon'
        token = 'mock_token'
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
        mock_load_test_from_redis.return_value = mock_test
        mock_get_flags_dict.return_value = {
            'en': '1',
            'fr': '2',
            'es': '3',
            'klingon': '4'
        }
        # ----- ACT
        result = guest_api.load_interro_question_guest(
            request,
            words,
            count,
            score,
            language,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            'request': request,
            'numWords': words,
            'count': count+1,
            'score': score,
            'progressPercent': 20,
            'content_box1': 'Goodbye',
            'token': token,
            'language': language,
            'flag': '4'
        }
        self.assertEqual(result, expected_result)
        mock_get_flags_dict.assert_called_once()
        mock_load_test_from_redis.assert_called_once_with(token)

    @patch('src.api.guest.get_flags_dict')
    @patch('src.api.guest.load_test_from_redis')
    def test_load_interro_answer_guest(
            self,
            mock_load_test_from_redis,
            mock_get_flags_dict
        ):
        # ----- ARRANGE
        request = 'mock_request'
        words = 10
        count = 1
        score = 1
        language = 'english'
        token = 'mock_token'
        mock_test = MagicMock()
        mock_test.interro_df = pd.DataFrame(
            {
                'english': ['Hi', 'Hello', 'Goodbye'],
                'french': ['Salut', 'Bonjour', 'Au revoir']
            },
            index=[0, 1, 2]
        )
        mock_load_test_from_redis.return_value = mock_test
        mock_get_flags_dict.return_value = {
            'fr': '2',
            'es': '3',
            'english': 'flag_id'
        }
        # ----- ACT
        result = guest_api.load_interro_answer_guest(
            request,
            words,
            count,
            score,
            token,
            language
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            'request': request,
            'numWords': words,
            'count': int(count),
            'score': int(score),
            'progressPercent': int(count / int(words) * 100),
            'content_box1': 'Hi',
            'content_box2': 'Salut',
            'token': 'mock_token',
            'language': 'english',
            'flag': 'flag_id'
        }
        self.assertEqual(result, expected_result)
        mock_load_test_from_redis.assert_called_once_with(token)
        mock_get_flags_dict.assert_called_once()

    @patch('src.api.guest.save_test_in_redis')
    @patch('src.interro.PremierTest.update_voc_df')
    @patch('src.api.guest.load_test_from_redis')
    def test_get_user_response_guest_yes(
            self,
            mock_load_test_from_redis,
            mock_update_voc_df,
            mock_save_test_in_redis
        ):
        # ----- ARRANGE
        data = {
            'score': 1,
            'answer': 'Yes',
            'english': 'Hi',
            'french': 'Salut'
        }
        token = 'mock_token'
        mock_load_test_from_redis.return_value = MagicMock()
        mock_update_voc_df.return_value = True
        mock_save_test_in_redis.return_value = True
        # ----- ACT
        result = guest_api.get_user_response_guest(data, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'score': 2,
            'message': "User response stored successfully.",
            'token': 'mock_token'
        }
        self.assertEqual(content_dict, expected_result)
        mock_load_test_from_redis.assert_called_once_with(token)
        # mock_update_voc_df.assert_called_once_with(True)
        mock_save_test_in_redis.assert_called_once_with(
            mock_load_test_from_redis.return_value,
            token
        )

    @patch('src.api.guest.save_test_in_redis')
    @patch('src.interro.PremierTest.update_faults_df')
    @patch('src.interro.PremierTest.update_voc_df')
    @patch('src.api.guest.load_test_from_redis')
    def test_get_user_response_guest_no(
            self,
            mock_load_test_from_redis,
            mock_update_voc_df,
            mock_update_faults_df,
            mock_save_test_in_redis
        ):
        # ----- ARRANGE
        data = {
            'score': 1,
            'answer': 'No',
            'english': 'Hi',
            'french': 'Salut'
        }
        token = 'mock_token'
        mock_test = MagicMock()
        mock_load_test_from_redis.return_value = mock_test
        mock_update_voc_df.return_value = True
        mock_update_faults_df.return_value = True
        mock_save_test_in_redis.return_value = True
        # ----- ACT
        result = guest_api.get_user_response_guest(data, token)
        # ----- ASSERT
        self.assertIsInstance(result, JSONResponse)
        content = result.body
        content_dict = content.decode('utf-8')
        content_dict = json.loads(content_dict)
        expected_result = {
            'score': 1,
            'message': "User response stored successfully.",
            'token': 'mock_token'
        }
        self.assertEqual(content_dict, expected_result)
        mock_load_test_from_redis.assert_called_once_with(token)
        # mock_update_voc_df.assert_called_once_with(False)
        # mock_update_faults_df.assert_called_once_with(
        #     False,
        #     'Hi',
        #     'Salut'
        # )
        mock_save_test_in_redis.assert_called_once_with(
            mock_load_test_from_redis.return_value,
            token
        )

    @patch('src.api.guest.save_test_in_redis')
    @patch('src.api.guest.load_test_from_redis')
    def test_propose_rattraps_guest(
            self,
            mock_load_test_from_redis,
            mock_save_test_in_redis
        ):
        # ----- ARRANGE
        request = 'mock_request'
        words = 10
        count = 1
        score = 1
        token = 'mock_token'
        language = 'klingon'
        mock_test = MagicMock()
        mock_test.faults_df = pd.DataFrame(
            {
                'english': ['Hi', 'Hello', 'Goodbye'],
                'french': ['Salut', 'Bonjour', 'Au revoir']
            },
            index=[0, 1, 2]
        )
        mock_test.interro_df = pd.DataFrame()
        mock_load_test_from_redis.return_value = mock_test
        mock_save_test_in_redis.return_value = True
        # ----- ACT
        result = guest_api.propose_rattraps_guest(
            request,
            words,
            count,
            score,
            token,
            language
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            'request': request,
            'score': score,
            'numWords': words,
            'count': count,
            'newScore': 0,
            'newWords': 3,
            'newCount': 0,
            'token': token,
            'language': language
        }
        self.assertEqual(result, expected_result)
        mock_load_test_from_redis.assert_called_once_with(token)
        mock_save_test_in_redis.assert_called_once_with(
            mock_test,
            token
        )

    def test_end_interro_guest(self):
        # ----- ARRANGE
        request = 'mock_request'
        score = 1
        words = 10
        token = 'mock_token'
        # ----- ACT
        result = guest_api.end_interro_guest(
            request,
            score,
            words,
            token
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_result = {
            'request': request,
            'score': score,
            'numWords': words,
            'token': token
        }
        self.assertEqual(result, expected_result)
