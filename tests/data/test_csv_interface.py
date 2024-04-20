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
from unittest.mock import MagicMock, patch

import pandas as pd

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import csv_interface



class TestCsvHandler(unittest.TestCase):
    """The CsvHandler class should serve as an interface with csv data."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.csv_handler_1 = csv_interface.CsvHandler('version')
        cls.csv_handler_2 = csv_interface.CsvHandler('theme')
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
        self.error_data_handler = csv_interface.CsvHandler(invalid_test_type)
        mock_logger = MagicMock()
        logging.basicConfig(level=logging.INFO)
        with self.assertRaises(SystemExit):
            # Act
            self.error_data_handler.set_paths()
            # Assert
            mock_logger.error.assert_called_with(f"Wrong test_type argument: {invalid_test_type}")
            mock_logger.error.assert_called_once()

    # @patch('src.data.csv_interface.pd.read_csv')
    # def test_set_tables(self, mock_read_csv):
    #     """
    #     Data should be correctly loaded.
    #     """
    #     # ----- ARRANGE
    #     self.tables = {}
    #     # ----- ACT
    #     self.csv_handler_1.set_tables()
    #     # ----- ASSERT
    #     self.assertGreater(len(self.csv_handler_1.paths), 1)
    #     self.assertIsInstance(self.csv_handler_1.tables, dict)
    #     self.assertEqual(len(self.csv_handler_1.tables), 4)
    #     for df_name, dataframe in self.csv_handler_1.tables.items():
    #         self.assertIn(
    #             df_name,
    #             [
    #                 self.csv_handler_1.test_type + '_voc',
    #                 self.csv_handler_1.test_type + '_perf',
    #                 self.csv_handler_1.test_type + '_word_cnt',
    #                 'output'
    #             ]
    #         )
    #         self.assertIsInstance(dataframe, type(pd.DataFrame()))
    #         self.assertGreater(dataframe.shape[1], 0)
    #     os.chdir('tests')

    def test_save_table(self):
        """Should save the table as a csv file."""
        # Arrange
        csv_handler = csv_interface.CsvHandler('version')
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
