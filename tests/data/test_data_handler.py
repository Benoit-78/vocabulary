"""
    Tests for data_handler module.
"""

import logging
import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import pandas as pd

REPO_DIR = os.getcwd().split('tests')[0]
sys.path.append(REPO_DIR)
from src.data import data_handler



class TestCsvHandler(unittest.TestCase):
    """The CsvHandler class should serve as an interface with csv data."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.csv_handler_1 = data_handler.CsvHandler('version')
        cls.csv_handler_2 = data_handler.CsvHandler('theme')
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
        self.error_data_handler = data_handler.CsvHandler(invalid_test_type)
        mock_logger = MagicMock()
        logging.basicConfig(level=logging.INFO)
        with self.assertRaises(SystemExit):
            # Act
            self.error_data_handler.set_paths()
            # Assert
            mock_logger.error.assert_called_with(f"Wrong test_type argument: {invalid_test_type}")
            mock_logger.error.assert_called_once()

    def test_set_tables(self):
        """Data should be correctly loaded"""
        # Act
        self.csv_handler_1.set_tables()
        self.csv_handler_2.set_tables()
        # Assert
        for csv_handler in [self.csv_handler_1, self.csv_handler_2]:
            self.assertGreater(len(csv_handler.paths), 1)
            self.assertIsInstance(csv_handler.tables, dict)
            self.assertEqual(len(csv_handler.tables), 4)
            for df_name, dataframe in csv_handler.tables.items():
                self.assertIn(
                    df_name,
                    [
                        csv_handler.test_type + '_voc',
                        csv_handler.test_type + '_perf',
                        csv_handler.test_type + '_word_cnt',
                        'output'
                    ]
                )
                self.assertIsInstance(dataframe, type(pd.DataFrame()))
                self.assertGreater(dataframe.shape[1], 0)
        os.chdir('tests')

    def test_save_table(self):
        """Should save the table as a csv file."""
        # Arrange
        csv_handler = data_handler.CsvHandler('version')
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



class TestMariaDBHandler(unittest.TestCase):
    """
    The tested class should serve as an interface with MariaDB databases.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.db_handler_1 = data_handler.MariaDBHandler(
            'version',
            mode='cli',
            language_1='test'
        )
        cls.db_handler_2 = data_handler.MariaDBHandler(
            'theme',
            mode='cli',
            language_1='English'
        )
        cls.error_data_handler = None

    def test_get_database_cred(self):
        """Should return the credentials."""
        # Arrange
        # Act
        result = self.db_handler_1.get_database_cred()
        # Assert
        self.assertEqual(len(result), 3)
        self.assertIn('users', result.keys())
        self.assertGreater(len(result['users']), 0)
        self.assertIn('host', result.keys())
        self.assertGreater(len(result['host']), 2)
        self.assertIn('port', result.keys())
        self.assertGreater(len(result['port']), 3)

    def test_get_database_cols(self):
        """
        Should return the columns that will be used in the tables.
        """
        # Arrange
        # Act
        result = self.db_handler_1.get_database_cols()
        # Assert
        language = list(result.keys())[0]
        table_1 = list(result[language].keys())[0]
        key_1 = list(result[language][table_1].keys())[0]
        self.assertEqual(key_1, 'Columns')

    @patch('src.data.data_handler.mariadb.connect')
    def test_set_db_cursor(self, mock_connect):
        """
        Should set cursor and connection to mariadb database as attributes
        """
        # Arrange
        self.db_handler_1.get_database_cred = MagicMock(
            return_value={
                'users':
                {
                    'user_1':
                    {
                        'name': 'test_user',
                        'password': 'test_password'
                    }
                },
                'port': 3306,
                'host':
                {
                    'cli': 'localhost'
                }
            }
        )
        # Act
        self.db_handler_1.set_db_cursor()
        # Assert
        self.assertIsInstance(self.db_handler_1.config, dict)
        self.assertEqual(
            {'user', 'password', 'database', 'port', 'host'},
            set(self.db_handler_1.config.keys())
        )
        mock_connect.assert_called_once_with(
            user='test_user',
            password='test_password',
            database='test',
            port=3306,
            host='localhost',
        )

    def test_get_tables_names(self):
        """Should return a list containing the tables names."""
        # Arrange
        self.db_handler_1.test_type = 'version'
        # Act
        result = self.db_handler_1.get_tables_names()
        # Assert
        expected_result = ['version_voc', 'version_perf', 'version_words_count', 'theme_voc']
        self.assertEqual(result, expected_result)
        for table_name in result[:-1]:
            self.assertIn(self.db_handler_1.test_type, table_name)
        test_types = ['version', 'theme']
        test_types.remove(self.db_handler_1.test_type)
        self.assertIn(test_types[0], result[-1])

    def test_create(self):
        """Should add a word in the database"""
        # Arrange
        test_row = ['African swallow', 'Mouette africaine']
        today_date = datetime.today().date()
        table_name = 'test_table'
        english = test_row[0]
        native = test_row[1]
        sql_request_1 = f"INSERT INTO {table_name} \
            (english, français, creation_date, nb, score, taux)"
        sql_request_2 = f"VALUES (\'{english}\', \'{native}\', \'{today_date}\', 0, 0, 0);"
        test_sql_request = " ".join([sql_request_1, sql_request_2])
        # Act
        result = self.db_handler_1.create(test_row, test_mode=True)
        self.db_handler_1.set_db_cursor()
        self.db_handler_1.cursor.execute(test_sql_request)
        # Assert
        # request_1 = "SELECT english, français, score"
        # request_2 = f"FROM {table_name}"
        # request_3 = f"WHERE english = '{english}';"
        # sql_request = " ".join([request_1, request_2, request_3])
        # self.db_handler_1.set_db_cursor()
        # english_2, native_2, score_2 = self.db_handler_1.cursor.execute(sql_request)
        expected_result = True
        self.assertEqual(result, expected_result)
        # self.assertEqual(english_2, english)
        # self.assertEqual(native_2, native)
        # self.assertEqual(score_2, 0)
        self.db_handler_1.connection.close()

    @patch(
        'src.data.data_handler.MariaDBHandler.get_tables_names',
        return_value=['table_name', '', '', '']
    )
    def test_get_words_from_test_type(self, mock_get_table_names):
        """Strange method that surely should be changed."""
        # Arrange   
        mock_df = pd.DataFrame(columns=['lang_1', 'lang_2'])
        mock_df.loc[mock_df.shape[0]] = ['African swallow', 'Mouette africaine']
        # Act
        result = self.db_handler_1.get_words_from_test_type(mock_df)
        # Assert
        self.assertEqual(len(result), 3)
        mock_get_table_names.assert_called_once()
