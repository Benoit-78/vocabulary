"""
    Tests for data_handler module.
"""

import os
import pandas as pd
import numpy as np
import sys
import unittest
import logging
from unittest.mock import patch, MagicMock

sys.path.append('..\\..\\')
from src import interro
from src.data import data_handler

class TestCsvHandler(unittest.TestCase):
    """The CsvHandler class should serve as an interface with csv data."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.csv_handler_1 = data_handler.CsvHandler('version')
        cls.csv_handler_2 = data_handler.CsvHandler('theme')

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
        self.csv_handler = data_handler.CsvHandler(invalid_test_type)
        mock_logger = MagicMock()
        logging.basicConfig(level=logging.INFO)
        with self.assertRaises(SystemExit):
            # Act
            self.csv_handler.set_paths()
            # Assert
            mock_logger.error.assert_called_with(f"Wrong test_type argument: {invalid_test_type}")
            mock_logger.error.assert_called_once()

    def test_set_tables(self):
        """Data should be correctly loaded"""
        # Arrange
        os.chdir('..')
        # Act
        self.csv_handler_1.set_tables()
        self.csv_handler_2.set_tables()
        # Assert
        for csv_handler in [self.csv_handler_1, self.csv_handler_2]:
            self.assertGreater(len(csv_handler.paths), 1)
            self.assertIsInstance(csv_handler.tables, dict)
            self.assertEqual(len(csv_handler.tables), 4)
            for df_name, dataframe in csv_handler.tables.items():
                self.assertIn(df_name, ['voc', 'perf', 'word_cnt', 'output'])
                self.assertIsInstance(dataframe, type(pd.DataFrame()))
                self.assertGreater(dataframe.shape[1], 0)
        os.chdir('tests')
