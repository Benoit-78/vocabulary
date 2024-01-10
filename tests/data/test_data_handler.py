"""
    Tests for data_handler module.
"""

import json
import logging
import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import mysql.connector as mariadb
import pandas as pd
from loguru import logger

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



class TestGetDBCursor(unittest.TestCase):
    @patch('src.data.data_handler.logger')
    @patch('src.data.data_handler.mariadb.connect')
    def test_get_db_cursor(self, mock_connect, mock_logger):
        # Prepare
        user_name = 'test_user'
        host = 'test_host'
        db_name = 'test_db'
        password = 'test_password'
        mock_connection = MagicMock(spec=mariadb.connection.MySQLConnection)
        mock_cursor = MagicMock(spec=mariadb.connection.MySQLCursor)
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        # Act
        result = data_handler.get_db_cursor(user_name, host, db_name, password)
        # Assert
        # mock_connect.assert_called_once_with(
        #     user=user_name,
        #     password=password,
        #     database=db_name,
        #     port=data_handler.PARAMS['MariaDB']['port'],
        #     host=host
        # )
        mock_connection.cursor.assert_called_once()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], mariadb.connection.MySQLConnection)
        self.assertIsInstance(result[1], mariadb.connection.MySQLCursor)
        self.assertEqual(result[0], mock_connection)
        self.assertEqual(result[1], mock_cursor)
        mock_logger.assert_not_called()



class TestDbController(unittest.TestCase):
    """"""
    @classmethod
    def setUp(cls):
        cls.host = 'web_local'
        cls.db_controller = data_handler.DbController(cls.host)

    @patch('src.data.data_handler.get_db_cursor')
    def test_create_user(self, mock_get_db_cursor):
        """Should create a user."""
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        root_password = 'test_root_password'
        user_name = 'test_user'
        user_password = 'test_user_password'
        # Act
        result = self.db_controller.create_user(root_password, user_name, user_password)
        # Assert
        self.assertEqual(result, True)
        mock_get_db_cursor.assert_called_once_with(
            'root',
            self.db_controller.host,
            'root',
            root_password
        )
        request_1 = f"CREATE USER '{user_name}'@'%'"
        request_2 = f"IDENTIFIED BY '{user_password}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.data_handler.get_db_cursor')
    def test_grant_privileges(self, mock_get_db_cursor):
        """
        Should grant all necessary privileges to a user on a database.
        """
        self.assertEqual(True, False)
        # Arrange
        # Act
        # Assert



class TestDbDefiner(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls):
        cls.user_name = 'benoit'
        cls.host = 'web_local'
        cls.password = 'test_password'
        cls.db_definer = data_handler.DbDefiner(cls.user_name, cls.host)

    def test_create_database(self):
        """"""
        self.assertEqual(True, False)

    def test_set_test_type(self):
        """"""
        self.assertEqual(True, False)

    @patch('src.data.data_handler.get_db_cursor')
    def test_get_database_cols(self, mock_get_db_cursor):
        """
        Should return the columns that will be used in the tables.
        """
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'test_db'
        mock_cursor.fetchall.return_value = [[(db_name,)]]  # Mock the USE statement result
        mock_cursor.fetchall.side_effect = [
            ['table1', 'table2'],  # Mock SHOW TABLES result
            [('col1', 'type1'), ('col2', 'type2')],
            [('col3', 'type3'), ('col4', 'type4')]  # Mock SHOW COLUMNS result
        ]
        # Act
        result = self.db_definer.get_database_cols(db_name, self.password)
        # Assertions
        mock_get_db_cursor.assert_called_once_with(
            self.db_definer.user_name,
            self.db_definer.host,
            db_name,
            self.password
        )
        mock_cursor.execute.assert_any_call(f"USE {db_name};")
        mock_cursor.execute.assert_any_call("SHOW TABLES;")
        mock_cursor.execute.assert_any_call("SHOW COLUMNS FROM table1;")
        mock_cursor.execute.assert_any_call("SHOW COLUMNS FROM table2;")
        self.assertEqual(
            result,
            {
                'table1': [('col1', 'type1'), ('col2', 'type2')],
                'table2': [('col3', 'type3'), ('col4', 'type4')]
            }
        )

    def test_get_tables_names(self):
        """Should return a list containing the tables names."""
        # Arrange
        self.db_definer.test_type = 'version'
        # Act
        result = self.db_definer.get_tables_names()
        # Assert
        expected_result = ['version_voc', 'version_perf', 'version_words_count', 'theme_voc']
        self.assertEqual(result, expected_result)
        for table_name in result[:-1]:
            self.assertIn(self.db_definer.test_type, table_name)
        test_types = ['version', 'theme']
        test_types.remove(self.db_definer.test_type)
        self.assertIn(test_types[0], result[-1])



class TestDbManipulator(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls):
        # DDL
        cls.user_name = 'benoit'
        cls.host = 'web_local'
        cls.db_definer = data_handler.DbDefiner(
            cls.user_name,
            cls.host
        )
        # DML
        cls.table_name = 'version_voc'
        cls.db_name = 'english'
        cls.test_type = 'version'
        cls.password = 'test_password'
        cls.db_manipulator = data_handler.DbManipulator(
            cls.user_name,
            cls.db_name,
            cls.host,
            cls.test_type
        )
        cls.words_df = pd.DataFrame({
            'english': ['test_english'],
            'french': ['test_french'],
            'score': [42]
        })

    def test_get_tables(self):
        """"""
        self.assertEqual(True, False)

    @patch('src.data.data_handler.get_db_cursor')
    def test_insert_word(self, mock_get_db_cursor):
        """"""
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        test_row = ['Bugger off', 'Fous moi le camp']
        today_date = datetime.today().date()
        # Act
        result = self.db_manipulator.insert_word(test_row, self.password)
        # Assert
        self.assertIsInstance(result, bool)
        self.assertEqual(result, True)
        mock_get_db_cursor.assert_called_once_with(
            self.db_manipulator.user_name,
            self.db_manipulator.host,
            self.db_manipulator.db_name,
            self.password
        )
        english = test_row[0]
        native = test_row[1]
        short_name = self.db_name + '.' + self.table_name
        request_1 = f"INSERT INTO {short_name} (english, français, creation_date, nb, score, taux)"
        request_2 = f"VALUES (\'{english}\', \'{native}\', \'{today_date}\', 0, 0, 0);"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.data_handler.get_db_cursor')
    def test_read(self, mock_get_db_cursor):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_cursor.execute.return_value = [('test_english', 'test_french', 42)]
        # Act
        result = self.db_manipulator.read(self.words_df, self.password)
        # Assert
        mock_get_db_cursor.assert_called_once_with(
            self.db_manipulator.user_name,
            self.db_manipulator.host,
            self.db_manipulator.db_name,
            self.password
        )
        mock_cursor.execute.assert_called_once_with(f"SELECT english, français, score FROM {self.table_name} WHERE english = 'test_english';")
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertEqual(result, ('test_english', 'test_french', 42))

    def test_update(self):
        """"""
        self.assertEqual(True, False)

    def test_delete(self):
        """"""
        self.assertEqual(True, False)

    def test_get_words_from_df(self):
        """Strange method that surely should be changed."""
        # Arrange   
        mock_df = pd.DataFrame(columns=['lang_1', 'lang_2'])
        mock_df.loc[mock_df.shape[0]] = ['African swallow', 'Mouette africaine']
        # Act
        result = self.db_manipulator.get_words_from_df(mock_df)
        # Assert
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], object)  # str, in reality

    def test_save_table(self):
        """"""
        self.assertEqual(True, False)
