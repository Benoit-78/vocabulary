"""
    Test module for 
"""

import os
import sys
import unittest
from unittest.mock import patch

REPO_DIR = os.getcwd().split('tests')[0]
sys.path.append(REPO_DIR)

from src.views import terminal as terminal_view



class TestCliUser(unittest.TestCase):
    """
    Tests on arguments parser.
    """
    def setUp(self):
        self.user = terminal_view.CliUser()

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments_default(self, mock_parse_args):
        """
        The method should store three arguments.
        """
        # ----- ARRANGE
        args = []
        # ----- ACT
        self.user.parse_arguments(args)
        # ----- ASSERT
        mock_parse_args.assert_called_with(
            [
                '-t', 'version',
                '-l', '10',
                '-r', '2'
            ]
        )

    @patch('argparse.ArgumentParser.parse_args')
    def test_arguments_all(self, mock_parse_args):
        """
        Test case 1: Valid arguments provided
        """
        # ----- ARRANGE
        args = [
            '--type', 'version',
            '--words', '100',
            '--rattrap', '1'
        ]
        # ----- ACT
        self.user.parse_arguments(args)
        # ----- ASSERT
        mock_parse_args.assert_called_with(
            [
                '--type', 'version',
                '--words', '100',
                '--rattrap', '1',
                '-t', 'version',
                '-l', '10',
                '-r', '2'
            ]
        )

    @patch('argparse.ArgumentParser.parse_args')
    def test_arguments_required_only(self, mock_parse_args):
        """
        Test case 2: Only required argument provided
        """
        # ----- ARRANGE
        args = ['-t', 'theme']
        # ----- ACT
        self.user.parse_arguments(args)
        # ----- ASSERT
        mock_parse_args.assert_called_with(
            [
                '-t', 'theme',
                '-l', '10',
                '-r', '2'
            ]
        )

    @patch('src.views.terminal.sys.argv', ['terminal.py', '-t', '', '-l', '100', '-r', '1'])
    @patch('src.views.terminal.logger')
    def test_get_settings_error_1(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        message = ' '.join([
            "Please give",
            "-t <test type>, ",
            "-l <test length> and ",
            "-r <number of rattrap>"
        ])
        mock_logger.error.assert_called_with(message)

    @patch('src.views.terminal.sys.argv', ['terminal.py', '-t', 'mock_type', '-l', '100', '-r', '1'])
    @patch('src.views.terminal.logger')
    def test_get_settings_error_2(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        mock_logger.error.assert_called_with("Test type must be either version or theme")

    @patch('src.views.terminal.sys.argv', ['terminal.py', '-t', 'version', '-l', '100', '-r', '-2'])
    @patch('src.views.terminal.logger')
    def test_get_settings_rattrap_negative(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        mock_logger.error.assert_called_with(
            "Number of rattrap must be greater than -1."
        )

    @patch('src.views.terminal.sys.argv', ['terminal.py', '-t', 'version', '-l', '-100', '-r', '1'])
    @patch('src.views.terminal.logger')
    def test_get_settings_words_negative(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        mock_logger.error.assert_called_with(
            "Test length must be greater than 0."
        )



class TestCliGuesser(unittest.TestCase):
    """
    Either on Windows or on Linux, this command line interface should enable the user
    to pass some interro, if he's not allergic to the black color of course.
    """
    @classmethod
    def setUpClass(cls):
        cls.guesser = terminal_view.CliGuesser()
        cls.row = [
            "How fast is an African swallow?",
            "A quelle vitesse vole une mouette africaine ?"
        ]

    @patch('src.views.terminal.messagebox.showinfo')
    def test_ask_word(self, mock_show_info):
        """
        Should ask the user a translation for the word proposed to him.
        """
        # ----- ARRANGE
        title = "Test Title"
        mock_show_info.return_value = True
        # ----- ACT
        self.guesser.ask_word(self.row, title)
        # ----- ASSERT
        mock_show_info.assert_called_with(
            title=title,
            message=f"Quelle traduction donnez-vous pour : {self.row[0]}?"
        )

    @patch('tkinter.messagebox.showinfo')
    @patch('src.views.terminal.logger')
    def test_ask_word_user_interrupt(self, mock_logger, mock_show_info):
        """
        User should be able to interrupt the test at anytime.
        """
        # ----- ARRANGE
        title = "Test Title"
        mock_show_info.return_value = False
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.guesser.ask_word(self.row, title)
        # ----- ASSERT
        mock_logger.error.assert_called_once_with("Interruption by user")

    @patch('src.views.terminal.messagebox.askyesnocancel')
    def test_get_user_answer(self, mock_ask_yes_no_cancel):
        # ----- ARRANGE
        title = "Test Title"
        message = f"Voici la traduction correcte : \'{self.row[1]}\'. \nAviez-vous la bonne réponse ?"
        mock_ask_yes_no_cancel.return_value = True
        # ----- ACT
        result = self.guesser.get_user_answer(self.row, title)
        # ----- ASSERT
        self.assertIsInstance(result, bool)
        mock_ask_yes_no_cancel.assert_called_once_with(
            title=title,
            message=message
        )

    @patch('src.views.terminal.messagebox.askyesnocancel')
    @patch('src.views.terminal.logger')
    def test_get_user_answer_interrupt(self, mock_logger, mock_ask_yes_no_cancel):
        # ----- ARRANGE
        title = "Test Title"
        message = f"Voici la traduction correcte : \'{self.row[1]}\'. \nAviez-vous la bonne réponse ?"
        mock_ask_yes_no_cancel.return_value = None
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.guesser.get_user_answer(self.row, title)
        # ----- ASSERT
        mock_logger.error.assert_called_with("Interruption by user")
        mock_ask_yes_no_cancel.assert_called_once_with(
            title=title,
            message=message
        )

    @patch('src.views.terminal.CliGuesser.get_user_answer')
    @patch('src.views.terminal.CliGuesser.ask_word')
    def test_guess_word(self, mock_ask_word, mock_get_user_answer):
        # ----- ARRANGE
        i = 1
        words = 2
        mock_ask_word.return_value = True
        mock_get_user_answer.return_value = True
        # ----- ACT
        result = self.guesser.guess_word(self.row, i, words)
        # ----- ASSERT
        self.assertEqual(result, True)
        mock_ask_word.assert_called_once()
        mock_get_user_answer.assert_called_once_with(
            row=self.row,
            title=f"Word {i}/{words}"
        )

    @patch('src.views.terminal.CliGuesser.get_user_answer')
    @patch('src.views.terminal.CliGuesser.ask_word')
    def test_guess_word_error(self, mock_ask_word, mock_get_user_answer):
        # ----- ARRANGE
        i = 1
        words = 2
        mock_ask_word.return_value = True
        mock_get_user_answer.return_value = False
        # ----- ACT
        result = self.guesser.guess_word(self.row, i, words)
        # ----- ASSERT
        self.assertEqual(result, False)
        mock_ask_word.assert_called_once()
        mock_get_user_answer.assert_called_once_with(
            row=self.row,
            title=f"Word {i}/{words}"
        )
