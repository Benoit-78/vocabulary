"""
    Decoupling date:
        30th March 2024
    Main purpose:
        Interaction with csv database.
"""

import logging
import os
import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch, mock_open

import pandas as pd
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import csv_interface



class TestDataHandler(unittest.TestCase):
    """
    The DataHandler class should serve as an interface with csv data.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.csv_handler_1 = csv_interface.DataHandler('version')
        cls.csv_handler_2 = csv_interface.DataHandler('theme')
        cls.error_data_handler = None

    def test_set_paths(self):
        """Data paths should exist"""
        # Act
        self.csv_handler_1.set_paths()
        self.csv_handler_2.set_paths()
        # Assert
        for csv_handler in [self.csv_handler_1, self.csv_handler_2]:
            self.assertIsInstance(csv_handler.paths, dict)
            self.assertEqual(len(csv_handler.paths), 4)
            for _, path in csv_handler.paths.items():
                self.assertIsInstance(path, str)

    def test_set_paths_error(self):
        """Error should be raised in case of unknown OS."""
        # Arrange
        invalid_test_type = "blablabla"
        self.error_data_handler = csv_interface.DataHandler(invalid_test_type)
        mock_logger = MagicMock()
        logging.basicConfig(level=logging.INFO)
        with self.assertRaises(SystemExit):
            # Act
            self.error_data_handler.set_paths()
            # Assert
            mock_logger.error.assert_called_with(f"Wrong test_type argument: {invalid_test_type}")
            mock_logger.error.assert_called_once()

    @patch('src.data.csv_interface.DataHandler.set_paths')
    @patch('src.data.csv_interface.pd.read_csv')
    def test_set_tables(self, mock_read_csv, mock_set_paths):
        """
        Data should be correctly loaded.
        """
        # ----- ARRANGE
        self.csv_handler_1.tables = {}
        mock_set_paths.return_value = {
            'version_voc': 'data/version_voc.csv',
            'version_perf': 'data/version_perf.csv',
            'version_word_cnt': 'data/version_words_count.csv',
            'output': 'data/theme_voc.csv'
        }
        self.csv_handler_1.test_type = 'version'
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'words': ['word1', 'word2', 'word3'],
                'integers': [1, 2, 3],
                'floats': [1.0, 2.0, 3.0],
                'booleans': [True, False, True]
            }
        )
        # ----- ACT
        self.csv_handler_1.set_tables()
        # ----- ASSERT
        self.assertIsInstance(self.csv_handler_1.tables, dict)
        self.assertEqual(len(self.csv_handler_1.tables), 4)
        for df_name, dataframe in self.csv_handler_1.tables.items():
            self.assertIn(
                df_name,
                [
                    self.csv_handler_1.test_type + '_voc',
                    self.csv_handler_1.test_type + '_perf',
                    self.csv_handler_1.test_type + '_word_cnt',
                    'output'
                ]
            )
            self.assertIsInstance(dataframe, type(pd.DataFrame()))
            self.assertEqual(dataframe.shape, (3, 4))

    @patch('src.data.csv_interface.DataHandler.set_paths')
    def test_get_paths(self, mock_set_paths):
        """
        Should return the paths.
        """
        # ----- ARRANGE
        mock_set_paths.return_value = True
        # ----- ACT
        paths = self.csv_handler_1.get_paths()
        # ----- ASSERT
        self.assertIsInstance(paths, dict)
        mock_set_paths.assert_called_once()

    @patch('src.data.csv_interface.DataHandler.set_tables')
    def test_get_tables(self, mock_set_tables):
        """
        Should return the paths.
        """
        # ----- ARRANGE
        mock_set_tables.return_value = True
        # ----- ACT
        paths = self.csv_handler_1.get_tables()
        # ----- ASSERT
        self.assertIsInstance(paths, dict)
        mock_set_tables.assert_called_once()

    def test_save_table(self):
        """
        Should save the table as a csv file.
        """
        # Arrange
        csv_handler = csv_interface.DataHandler('version')
        csv_handler.set_paths()
        old_df = pd.DataFrame(columns=['words', 'integers', 'floats', 'booleans'])
        old_df.loc[old_df.shape[0]] = ['a', 0, 0.0, True]
        old_df.loc[old_df.shape[0]] = ['b', 1, 1.0, False]
        old_df.loc[old_df.shape[0]] = ['c', 2, 2.0, False]
        csv_handler.paths['for_test_only'] = csv_handler.os_sep.join(
            [r'.', 'data', 'for_test_only.csv']
        )
        # Act
        csv_handler.save_table(
            table_name='for_test_only',
            table=old_df
        )
        new_df = pd.read_csv(csv_handler.paths['for_test_only'], sep=';')
        # Assert
        self.assertEqual(old_df.shape, new_df.shape)
        for column in new_df.columns:
            self.assertEqual(
                list(old_df[column]),
                list(new_df[column])
            )
        os.remove(csv_handler.paths['for_test_only'])



class TestMenusReader(unittest.TestCase):
    """
    The MenuReader class should serve as an interface with csv data.
    """
    def setUp(self):
        """Run once before all tests."""
        self.menu_reader = csv_interface.MenuReader('user/user_space')

    def test_init(self):
        """
        MenuReader should be initialized correctly.
        """
        # ----- ARRANGE
        # ----- ACT
        # ----- ASSERT
        self.assertIsInstance(self.menu_reader, csv_interface.MenuReader)
        self.assertEqual(self.menu_reader.os_sep, os.sep)
        self.assertEqual(self.menu_reader.path, '')
        self.assertEqual(self.menu_reader.page, 'user_space.html')

    def test_set_path(self):
        """
        Path should be set correctly.
        """
        # ----- ARRANGE
        # ----- ACT
        self.menu_reader.set_path()
        # ----- ASSERT
        self.assertIsInstance(self.menu_reader.path, str)
        self.assertEqual(self.menu_reader.path, './data/menus.csv')

    @patch('src.data.csv_interface.pd.read_csv')
    def test_get_translations_dict(self, mock_read_csv):
        """
        Should return the translations dictionary.
        """
        # ----- ARRANGE
        mock_df = pd.DataFrame({
            'page': ['user_space.html', 'user_space.html', 'welcome.html'],
            'standard': ['pomme', 'banane', 'some_strange_value'],
            'english': ['apple', 'banana', 'some_value'],
            'french': ['pomme', 'banane', 'some_strange_value']
        })
        mock_read_csv.return_value = mock_df
        # ----- ACT
        result = self.menu_reader.get_translations_dict()
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        expected_dict = {
            'pomme': {
                'en': 'apple',
                'fr': 'pomme',
            },
            'banane': {
                'en': 'banana',
                'fr': 'banane'
            }
        }
        self.assertEqual(result, expected_dict)
