"""
    Test module for 
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from tkinter import messagebox
from loguru import logger

sys.path.append('..\\')
from src import views_local



class TestCliGuesser(unittest.TestCase):
    """
    Either on Windows or on Linux, this command line interface should enable the user
    to pass some interro, if he's not allergic to the black color of course.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.guesser = views_local.CliGuesser()
        cls.row = [
            "How fast is an African swallow?",
            "A quelle vitesse vole une mouette africaine ?"
        ]

    @patch('tkinter.messagebox.showinfo', return_value=True)
    def test_ask_word(self, mock_showinfo):
        """"""
        # Arrange
        title = "Test Title"
        # Act
        self.guesser.ask_word(self.row, title)
        # Assert
        mock_showinfo.assert_called_with(
            title=title,
            message=f"Quelle traduction donnez-vous pour : {self.row[0]}?"
        )

    @patch('tkinter.messagebox.showinfo', return_value=False)
    @patch('builtins.print')
    @patch('builtins.exit')
    def test_ask_word_user_interrupt(self, mock_print, mock_exit, mock_showinfo):
        # Arrange
        title = "Test Title"
        with self.assertRaises(SystemExit):
            # Act
            self.guesser.ask_word(self.row, title)
            # Assert that the appropriate messages are printed
            mock_print.assert_called_with("Interruption by user")
            mock_exit.assert_called_once()

    # @patch('tkinter.messagebox.showinfo', return_value=True)
    # def test_guess_word(self, mock_showinfo):
    #     # Arrange
    #     i = 1
    #     words = 2
    #     # Act
    #     result = self.guesser.guess_word(self.row, i, words)
    #     # Assert
    #     self.assertIsInstance(result, bool)
