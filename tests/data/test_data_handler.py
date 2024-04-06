"""
    Main purpose:
        Tests for data_handler module.
"""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import mysql.connector as mariadb
import pandas as pd
# from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.data import data_handler



class TestDbInterface(unittest.TestCase):
    """
    Abstract class, embodied by divers daughter classes that serve as 
    interfaces for different data operations.
    As of today (2024-03-30), the daughter classes are:
    - DbController, for Data Control Language operations,
    - DbDefiner, for Data Definition Language operations,
    - DbManipulator, for Data Manipulation Language operations.
    """
    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.data_handler.logger')
    @patch('src.data.data_handler.mariadb.connect')
    def test_get_db_cursor_host_ok(self, mock_connect, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock(spec=mariadb.connection.MySQLConnection)
        mock_cursor = MagicMock(spec=mariadb.connection.MySQLCursor)
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        db_interface = data_handler.DbInterface()
        # ----- ACT
        result = db_interface.get_db_cursor()
        # ----- ASSERT
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

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.data_handler.logger')
    @patch('src.data.data_handler.mariadb.connect')
    def test_get_db_cursor_host_nok(self, mock_connect, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock(spec=mariadb.connection.MySQLConnection)
        mock_cursor = MagicMock(spec=mariadb.connection.MySQLCursor)
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        db_interface = data_handler.DbInterface()
        db_interface.host = 'nimportequoi'
        # ----- ACT
        result = db_interface.get_db_cursor()
        # ----- ASSERT
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
        mock_logger.warning.assert_called_once_with("host: nimportequoi")
        mock_logger.error.assert_called_once_with(f"host should be in {data_handler.HOSTS}")



class TestDbController(unittest.TestCase):
    """
    Should provide all necessary methods to define:
    - database access,
    - authorization methods.
    """
    @classmethod
    def setUp(cls):
        cls.mock_host = 'localhost'
        with patch('socket.gethostname', return_value=cls.mock_host):
            cls.db_controller = data_handler.DbController()
        cls.user_name = 'test_user'

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.data_handler.DbController.get_db_cursor')
    def test_create_user_in_mysql_ok(self, mock_get_db_cursor):
        """
        Should create a user in the mysql database.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        user_password = 'test_user_password'
        # ----- ACT
        result = self.db_controller.create_user_in_mysql(self.user_name, user_password)
        # ----- ASSERT
        self.assertEqual(result, True)
        mock_get_db_cursor.assert_called_once()
        request_1 = f"CREATE USER '{self.user_name}'@'{self.mock_host}'"
        request_2 = f"IDENTIFIED BY '{user_password}';"
        sql_request_1 = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_with(sql_request_1)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    # @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    # @patch('src.data.data_handler.DbController.get_db_cursor')
    # def test_create_user_in_mysql_nok(self, mock_get_db_cursor):
    #     # ----- ARRANGE
    #     mock_connection = MagicMock()
    #     mock_cursor = MagicMock()
    #     mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
    #     user_password = 'test_user_password'
    #     # ----- ACT
    #     result = self.db_controller.create_user_in_mysql(self.user_name, user_password)
    #     # ----- ASSERT
    #     self.assertEqual(result, True)
    #     mock_get_db_cursor.assert_called_once()
    #     request_1 = f"CREATE USER '{self.user_name}'@'{self.mock_host}'"
    #     request_2 = f"IDENTIFIED BY '{user_password}';"
    #     sql_request_1 = " ".join([request_1, request_2])
    #     mock_cursor.execute.assert_called_with(sql_request_1)
    #     mock_cursor.close.assert_called_once()
    #     mock_connection.close.assert_called_once()

    @patch('src.data.data_handler.mariadb')
    def test_create_user_failure(self, mock_mariadb):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_mariadb.connect.return_value = (mock_connection, mock_cursor)
        mock_cursor.execute.side_effect = mariadb.Error("Mock error")
        user_name = 'test_user'
        user_password = 'test_password'
        # Act
        result = self.db_controller.create_user_in_mysql(user_name, user_password)
        # Assert
        self.assertFalse(result)
        mock_cursor.execute.assert_called_once()
        mock_connection.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.data_handler.DbController.get_db_cursor')
    def test_grant_privileges(self, mock_get_db_cursor):
        """
        Should grant all necessary privileges to a user on a database.
        """
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'test_database_name'
        # Act
        result = self.db_controller.grant_privileges(self.user_name, db_name)
        # Assert
        self.assertEqual(result, True)
        mock_get_db_cursor.assert_called_once_with()
        request_1 = f"GRANT SELECT, INSERT, UPDATE, CREATE, DROP ON {self.user_name}_{db_name}.*"
        request_2 = f"TO '{self.user_name}'@'{self.mock_host}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()



class TestDbDefiner(unittest.TestCase):
    """
    Should provide all necessary methods to define data structure.
    """
    @classmethod
    def setUpClass(cls):
        cls.user_name = 'benoit'
        cls.db_definer = data_handler.DbDefiner(cls.user_name)

    @patch('src.data.data_handler.DbDefiner.get_db_cursor')
    def test_create_database(self, mock_get_db_cursor):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'test_db'
        # Act
        result = self.db_definer.create_database(db_name)
        # Assert
        mock_get_db_cursor.assert_called_once()
        sql_request = f"CREATE DATABASE {self.user_name}_{db_name};"
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.data_handler.DbDefiner.get_db_cursor')
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
        result = self.db_definer.get_database_cols(db_name)
        # Assertions
        mock_get_db_cursor.assert_called_once()
        mock_cursor.execute.assert_any_call(f"USE {db_name};")
        mock_cursor.execute.assert_any_call("SHOW TABLES;")
        mock_cursor.execute.assert_any_call("SHOW COLUMNS FROM table1;")
        mock_cursor.execute.assert_any_call("SHOW COLUMNS FROM table2;")
        # self.assertEqual(
        #     result,
        #     {
        #         'table1': [('col1', 'type1'), ('col2', 'type2')],
        #         'table2': [('col3', 'type3'), ('col4', 'type4')]
        #     }
        # )
        self.assertEqual(
            result,
            {
                'table1': ['col1', 'col2'],
                'table2': ['col3', 'col4']
            }
        )

    def test_get_tables_names(self):
        """Should return a list containing the tables names."""
        # Arrange
        test_type = 'version'
        # Act
        result = self.db_definer.get_tables_names(test_type)
        # Assert
        expected_result = ['version_voc', 'version_perf', 'version_words_count', 'theme_voc']
        self.assertEqual(result, expected_result)
        for table_name in result[:-1]:
            self.assertIn(test_type, table_name)
        test_types = ['version', 'theme']
        test_types.remove(test_type)
        self.assertIn(test_types[0], result[-1])



class TestDbManipulator(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls):
        # Data definition
        cls.user_name = 'benoit'
        cls.db_definer = data_handler.DbDefiner(cls.user_name)
        # Data manipulation
        cls.table_name = 'version_voc'
        cls.db_name = 'english'
        cls.test_type = 'version'
        cls.password = 'test_password'
        cls.db_manipulator = data_handler.DbManipulator(
            cls.user_name,
            cls.db_name,
            cls.test_type
        )
        cls.words_df = pd.DataFrame({
            'english': ['test_english'],
            'french': ['test_french'],
            'score': [42]
        })

    def test_check_test_type(self):
        """"""
        # Arrange
        # Act
        self.db_manipulator.check_test_type(('version'))
        # Assert
        self.assertIsInstance(self.db_manipulator.test_type, str)
        self.assertIn(self.db_manipulator.test_type, ['version', 'theme'])
        self.assertEqual(self.db_manipulator.test_type, 'version')

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.data_handler.DbDefiner.get_database_cols')
    @patch('src.data.data_handler.DbManipulator.get_db_cursor')
    def test_get_tables(self, mock_get_db_cursor, mock_get_database_cols):
        """"""
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_get_database_cols.return_value = {
            'version_voc':
            [
                'col_1', 'col_2'
            ],
            'version_perf':
            [
                'col_3', 'col_4'
            ],
            'version_words_count':
            [
                'col_5', 'col_6'
            ],
            'theme_voc':
            [
                'col_7', 'col_8'
            ],
            'theme_perf':
            [
                'col_9', 'col_10'
            ],
            'theme_words_count':
            [
                'col_11', 'col_12'
            ],
            'archives':
            [
                'col_13', 'col_14'
            ]
        }
        # Act
        result = self.db_manipulator.get_tables()
        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 7)
        self.assertIn('output', list(result.keys()))
        mock_get_db_cursor.assert_called_once_with()

    @patch('src.data.data_handler.DbManipulator.get_db_cursor')
    def test_insert_word(self, mock_get_db_cursor):
        """
        Should add a word to the table.
        """
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        test_row = ['Bugger off', 'Fous moi le camp']
        today_date = datetime.today().date()
        # Act
        result = self.db_manipulator.insert_word(test_row)
        # Assert
        self.assertIsInstance(result, int)
        self.assertEqual(result, True)
        sql_db_name = f'{self.db_manipulator.user_name}_{self.db_manipulator.db_name}'
        mock_get_db_cursor.assert_called_once()
        english = test_row[0]
        native = test_row[1]
        request_1 = f"INSERT INTO {sql_db_name}.{self.table_name}"
        request_2 = "(english, français, creation_date, nb, score, taux)"
        request_3 = f"VALUES (\'{english}\', \'{native}\', \'{today_date}\', 0, 0, 0);"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.data_handler.DbManipulator.get_db_cursor')
    def test_read_word(self, mock_get_db_cursor):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_cursor.execute.return_value = [('test_english', 'test_french', 42)]
        english = self.words_df['english'][0]
        # Act
        result = self.db_manipulator.read_word(english)
        # Assert
        mock_get_db_cursor.assert_called_once_with()
        request_1 = f"SELECT english, français, score FROM {self.table_name}"
        request_2 = f"WHERE english = '{english}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertEqual(result, ('test_english', 'test_french', 42))

    @patch('src.data.data_handler.DbManipulator.get_db_cursor')
    def test_update_word(self, mock_get_db_cursor):
        """"""
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        english = 'test_word'
        new_nb = 4
        new_score = 67
        # Act
        self.db_manipulator.update_word(english, new_nb, new_score)
        # Assert
        request_1 = f"UPDATE {self.table_name}"
        request_2 = f"SET nb = {new_nb}, score = {new_score}"
        request_3 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.data_handler.DbManipulator.get_db_cursor')
    def test_delete_word(self, mock_get_db_cursor):
        """"""
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        english = 'test_word'
        # Act
        self.db_manipulator.delete_word(english)
        # Assert
        request_1 = f"DELETE FROM {self.table_name}"
        request_2 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.data_handler.DbManipulator.get_db_cursor')
    @patch('src.data.data_handler.DbDefiner.get_database_cols')
    @patch('src.data.data_handler.create_engine')
    def test_save_table(self, mock_create_engine, mock_get_database_cols, mock_get_db_cursor):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        #
        mock_get_database_cols.return_value = {
            'version_voc': ['col_1', 'col_2'],
            'version_perf': ['col_3', 'col_4'],
            'version_words_count': ['col_5', 'col_6'],
            'theme_voc': ['col_7', 'col_8'],
            'theme_perf': ['col_9', 'col_10'],
            'theme_words_count': ['col_11', 'col_12'],
            'archives': ['col_13', 'col_14']
        }
        #
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        password = 'root_password'
        table_name = 'version_voc'
        table = pd.DataFrame({'col_1': [1, 2], 'col_2': ['a', 'b']})
        # Act
        self.db_manipulator.save_table(table_name, table)
        # Assert
        mock_get_db_cursor.assert_called_once()
        mock_create_engine.assert_called_once_with(
            f"mysql+pymysql://root:{password}@{self.db_manipulator.host}/{self.db_manipulator.db_name.lower()}"
        )
        # mock_engine.to_sql.assert_called_once_with(
        #     name=table_name,
        #     con=mock_engine,
        #     if_exists='replace',
        #     method='multi',
        #     index=False
        # )
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
