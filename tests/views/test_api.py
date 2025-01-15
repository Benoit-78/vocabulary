"""
    Creator:
        B.Delorme
    Creation date:
        20th April 2024
    Main purpose:
        Test script for api_view.py
"""

import unittest
from unittest.mock import patch

from src.views import api as api_view



class TestFastapiGuesser(unittest.TestCase):
    def setUp(self):
        self.fastapi_guesser = api_view.FastapiGuesser()

    def test_ask_word(self):
        """
        Ask a word to the user
        """
        # ----- ARRANGE
        row = ['1', 'word', 'mot']
        # ----- ACT
        result = self.fastapi_guesser.ask_word(row)
        # ----- ASSERT
        self.assertEqual(result, 'word')

    def test_return_translation(self):
        """
        Return translation to the user
        """
        # ----- ARRANGE
        row = ['1', 'word', 'mot']
        # ----- ACT
        result = self.fastapi_guesser.return_translation(row)
        # ----- ASSERT
        self.assertEqual(result, 'mot')

    @patch('src.views.api.FastapiGuesser.return_translation')
    @patch('src.views.api.FastapiGuesser.ask_word')
    def test_guess_word(
            self,
            mock_ask_word,
            mock_return_translation,
        ):
        """
        Steps of the user's guessing process.
        """
        # ----- ARRANGE
        row = ['1', 'word', 'mot']
        words = 10
        mock_ask_word.return_value = True
        mock_return_translation.return_value = True
        # ----- ACT
        self.fastapi_guesser.guess_word(row, words)
        # ----- ASSERT
        mock_ask_word.assert_called_once_with(row)
        mock_return_translation.assert_called_once_with(row)
