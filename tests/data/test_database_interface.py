"""
    Main purpose:
        Tests for database_interface module.
"""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import mysql.connector as mariadb
import pandas as pd

from src.data import database_interface



class TestDbInterface(unittest.TestCase):
    """
    Abstract class, embodied by divers daughter classes that serve as 
    interfaces for different data operations.
    As of today (2024-06-01), the daughter classes are:
    - DbController, for Data Control Language operations,
    - DbDefiner, for Data Definition Language operations,
    - DbManipulator, for Data Manipulation Language operations,
    - DbQuerier, for Data Querying Language operations.
    """
    @patch('src.data.database_interface.logger')
    def test_check_host(self, mock_logger):
        # ----- ARRANGE
        db_interface = database_interface.DbInterface()
        db_interface.host = 'mock_host'
        # ----- ACT
        # ----- ASSERT
        with self.assertRaises(ValueError):
            db_interface.check_host()
            mock_logger.warning.assert_called_once_with(
                "host: mock_host"
            )
            mock_logger.error.assert_called_once_with(
                f"host should be in {database_interface.HOSTS.keys()}"
            )


    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb.connect')
    def test_get_db_cursor_host_ok(self, mock_connect, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock(spec=mariadb.connection.MySQLConnection)
        mock_cursor = MagicMock(spec=mariadb.connection.MySQLCursor)
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        db_interface = database_interface.DbInterface()
        # ----- ACT
        result = db_interface.get_db_cursor()
        # ----- ASSERT
        # mock_connect.assert_called_once_with(
        #     user=user_name,
        #     password=password,
        #     database=db_name,
        #     port=database_interface.PARAMS['MariaDB']['port'],
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
    """
    Should provide all necessary methods to define:
    - database access,
    - authorization methods.
    """
    @classmethod
    def setUp(cls):
        cls.mock_host = 'localhost'
        with patch('socket.gethostname', return_value=cls.mock_host):
            cls.db_controller = database_interface.DbController()
        cls.user_name = 'test_user'

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.database_interface.DbController.get_db_cursor')
    def test_create_user_in_mysql(self, mock_get_db_cursor):
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
        mock_get_db_cursor.assert_called_once()
        request_1 = f"CREATE USER '{self.user_name}'@'{self.mock_host}'"
        request_2 = f"IDENTIFIED BY '{user_password}';"
        sql_request_1 = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_with(sql_request_1)
        self.assertEqual(result, True)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_create_user_error(self, mock_mariadb, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.commit.side_effect = mariadb.Error("ER_CANNOT_USER")
        user_password = 'test_password'
        # ----- ACT
        result = self.db_controller.create_user_in_mysql("test_user", "test_password")
        # ----- ASSERT
        request_1 = f"CREATE USER '{self.user_name}'@'{self.mock_host}'"
        request_2 = f"IDENTIFIED BY '{user_password}';"
        sql_request_1 = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_with(sql_request_1)
        mock_connection.commit.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertEqual(result, False)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_grant_privileges_on_common_database(
            self,
            mock_mariadb,
            mock_logger
        ):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        # ----- ACT
        result = self.db_controller.grant_privileges_on_common_database('test_user')
        # ----- ASSERT
        mock_cursor.execute.assert_called_once_with(
            "GRANT SELECT ON common.* TO 'test_user'@'localhost';"
        )
        mock_connection.commit.assert_called_once()
        mock_logger.success.assert_called_once_with(
            f"User '{self.user_name}' created on {self.db_controller.host}."
        )
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertTrue(result)

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_grant_privileges_on_common_database_error(
            self,
            mock_mariadb,
            mock_logger
        ):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.commit.side_effect = mariadb.Error("ER_CANNOT_USER")
        # ----- ACT
        result = self.db_controller.grant_privileges_on_common_database('test_user')
        # ----- ASSERT
        mock_cursor.execute.assert_called_once_with(
            "GRANT SELECT ON common.* TO 'test_user'@'localhost';"
        )
        mock_connection.commit.assert_called_once()
        # mock_logger.error.assert_called_once_with(mariadb.Error(-1, 'ER_CANNOT_USER', None)²)
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.mariadb')
    def test_grant_privileges(self, mock_mariadb):
        """
        Should grant all necessary privileges to a user on a database.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        db_name = 'test_database_name'
        # ----- ACT
        result = self.db_controller.grant_privileges(self.user_name, db_name)
        # ----- ASSERT
        self.assertEqual(result, True)
        request_1 = f"GRANT SELECT, INSERT, UPDATE, CREATE, DROP ON {self.user_name}_{db_name}.*"
        request_2 = f"TO '{self.user_name}'@'{self.mock_host}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_grant_privileges_error(self, mock_mariadb, mock_logger):
        """
        Should grant all necessary privileges to a user on a database.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.commit.side_effect = mariadb.Error("ER_CANNOT_USER")
        db_name = 'test_database_name'
        # ----- ACT
        result = self.db_controller.grant_privileges(self.user_name, db_name)
        # ----- ASSERT
        request_1 = f"GRANT SELECT, INSERT, UPDATE, CREATE, DROP ON {self.user_name}_{db_name}.*"
        request_2 = f"TO '{self.user_name}'@'{self.mock_host}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_connection.commit.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertEqual(result, False)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.mariadb')
    def test_get_users_list_from_mysql(self, mock_mariadb):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('user1', 'localhost'),
            ('user2', 'localhost')
        ]
        mock_cursor.description = [
            ['User', 'some_value'],
            ['Host', 'some_value']
        ]
        # ----- ACT
        result = self.db_controller.get_users_list_from_mysql()
        # ----- ASSERT
        self.assertIsInstance(result, list)
        self.assertEqual(result, ['user1', 'user2'])
        mock_cursor.execute.assert_called_once_with("SELECT User, Host FROM mysql.user;")
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_get_users_list_from_mysql_error(self, mock_mariadb, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = mariadb.Error("ER_CANNOT_USER")
        # ----- ACT
        result = self.db_controller.get_users_list_from_mysql()
        # ----- ASSERT
        mock_cursor.execute.assert_called_once_with("SELECT User, Host FROM mysql.user;")
        mock_cursor.fetchall.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.mariadb')
    def test_add_user_to_users_table(self, mock_mariadb):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        hash_password = 'mock_pwd'
        user_email = 'mock_email'
        # ----- ACT
        result = self.db_controller.add_user_to_users_table(
            self.user_name,
            hash_password,
            user_email
        )
        # ----- ASSERT
        self.assertEqual(result, True)
        request_1 = "INSERT INTO `users`.`voc_users`"
        request_2 = "(`username`, `password_hash`, `email`, `disabled`)"
        request_3 = f"VALUES('{self.user_name}', '{hash_password}', '{user_email}', FALSE);"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_add_user_to_users_table_error(self, mock_mariadb, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.commit.side_effect = mariadb.Error("ER_CANNOT_USER")
        hash_password = 'mock_pwd'
        user_email = 'mock_email'
        # ----- ACT
        result = self.db_controller.add_user_to_users_table(
            self.user_name,
            hash_password,
            user_email
        )
        # ----- ASSERT
        request_1 = "INSERT INTO `users`.`voc_users`"
        request_2 = "(`username`, `password_hash`, `email`, `disabled`)"
        request_3 = f"VALUES('{self.user_name}', '{hash_password}', '{user_email}', FALSE);"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_connection.commit.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertEqual(result, False)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.mariadb')
    def test_get_users_list(self, mock_mariadb):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('user1', 'pwd_hash_1', 'mail_1', True),
            ('user2', 'pwd_hash_2', 'mail_2', False)
        ]
        mock_cursor.description = [
            ['User', 'some_value'],
            ['Password_hash', 'some_value'],
            ['Email', 'some_value'],
            ['Disabled', 'some_value'],
        ]
        # ----- ACT
        result = self.db_controller.get_users_list()
        # ----- ASSERT
        self.assertIsInstance(result, list)
        request_1 = "SELECT username, password_hash, email, disabled"
        request_2 = "FROM users.voc_users;"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_get_users_list_error(self, mock_mariadb, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = mariadb.Error("ER_CANNOT_USER")
        # ----- ACT
        result = self.db_controller.get_users_list()
        # ----- ASSERT
        request_1 = "SELECT username, password_hash, email, disabled"
        request_2 = "FROM users.voc_users;"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.fetchall.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_revoke_privileges(self, mock_mariadb, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        db_name = 'mock_db_name'
        # ----- ACT
        result = self.db_controller.revoke_privileges(
            self.user_name,
            db_name
        )
        # ----- ASSERT
        self.assertEqual(result, True)
        request_1 = "REVOKE SELECT, INSERT, UPDATE, CREATE, DROP ON"
        request_2 = f"{db_name}.* FROM '{self.user_name}'@'{self.db_controller.host}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_connection.commit.assert_called_once()
        mock_logger.success.assert_called_once_with(
            f"User '{self.user_name}' removed from '{self.user_name}_{db_name}'."
        )
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.mariadb')
    def test_revoke_privileges_error(self, mock_mariadb, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_mariadb.connect.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.commit.side_effect = mariadb.Error("ER_CANNOT_USER")
        db_name = 'mock_db_name'
        # ----- ACT
        result = self.db_controller.revoke_privileges(
            self.user_name,
            db_name
        )
        # ----- ASSERT
        request_1 = "REVOKE SELECT, INSERT, UPDATE, CREATE, DROP ON"
        request_2 = f"{db_name}.* FROM '{self.user_name}'@'{self.db_controller.host}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_connection.commit.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertEqual(result, False)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()



class TestDbDefiner(unittest.TestCase):
    """
    Should provide all necessary methods to define data structure.
    """
    @classmethod
    def setUpClass(cls):
        cls.user_name = 'username'
        cls.db_definer = database_interface.DbDefiner(cls.user_name)

    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_create_database(self, mock_get_db_cursor):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'test_db'
        # Act
        result = self.db_definer.create_database(db_name)
        # Assert
        self.assertEqual(result, True)
        mock_get_db_cursor.assert_called_once()
        sql_request = f"CREATE DATABASE {self.user_name}_{db_name};"
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbDefiner.validate_db_name')
    def test_create_database_invalid_name(
            self,
            mock_validate_db_name,
            mock_logger
        ):
        # ----- ARRANGE
        db_name = 'testdb'
        mock_validate_db_name.return_value = False
        # ----- ACT
        result = self.db_definer.create_database(db_name)
        # ----- ASSERT
        self.assertEqual(result, False)
        mock_logger.error.assert_called_once_with(
            f"Invalid database name: username_testdb"
        )

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_create_database_error(self, mock_get_db_cursor, mock_logger):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_connection.commit.side_effect = mariadb.Error("ER_CANNOT_USER")
        db_name = 'test_db'
        # Act
        result = self.db_definer.create_database(db_name)
        # Assert
        mock_get_db_cursor.assert_called_once()
        sql_request = f"CREATE DATABASE {self.user_name}_{db_name};"
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_connection.commit.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_get_user_databases(self, mock_get_db_cursor):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_cursor.fetchall.return_value = [
            [self.db_definer.user_name + '_' + 'english'],
            [self.db_definer.user_name + '_' + 'french']
        ]
        # ----- ACT
        result = self.db_definer.get_user_databases()
        # ----- ASSERT
        self.assertIsInstance(result, list)
        self.assertEqual(result, ['username_english', 'username_french'])
        mock_cursor.execute.assert_called_once_with(
            f"SHOW DATABASES LIKE '{self.db_definer.user_name}_%';"
        )
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_get_user_databases_error(self, mock_get_db_cursor, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_cursor.fetchall.side_effect = mariadb.Error("ER_CANNOT_USER")
        # ----- ACT
        result = self.db_definer.get_user_databases()
        # ----- ASSERT
        mock_cursor.execute.assert_called_once_with(
            f"SHOW DATABASES LIKE '{self.db_definer.user_name}_%';"
        )
        mock_cursor.fetchall.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_create_seven_tables(self, mock_get_db_cursor):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'mock_db_name'
        sql_db_name = f"{self.user_name}_{db_name}"
        # ----- ACT
        result = self.db_definer.create_seven_tables(db_name)
        # ----- ASSERT
        self.assertTrue(result)
        mock_cursor.execute.assert_any_call(f"USE {sql_db_name};")
        assert mock_cursor.execute.call_count == 8
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbDefiner.validate_db_name')
    def test_create_seven_tables_invalid_name(
            self,
            mock_validate_db_name,
            mock_logger
        ):
        # ----- ARRANGE
        db_name = 'testdb'
        mock_validate_db_name.return_value = False
        # ----- ACT
        result = self.db_definer.create_seven_tables(db_name)
        # ----- ASSERT
        self.assertEqual(result, False)
        mock_logger.error.assert_called_once_with(
            f"Invalid database name: username_testdb"
        )

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_create_seven_tables_error(self, mock_get_db_cursor, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_cursor.execute.side_effect = mariadb.Error("ER_CANNOT_USER")
        db_name = 'mock_db_name'
        sql_db_name = f"{self.user_name}_{db_name}"
        # ----- ACT
        result = self.db_definer.create_seven_tables(db_name)
        # ----- ASSERT
        mock_cursor.execute.assert_called_once_with(f"USE {sql_db_name};")
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.DbDefiner.rectify_this_strange_result')
    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_get_database_cols(
            self,
            mock_get_db_cursor,
            mock_rectify
        ):
        """
        Should return the columns that will be used in the tables.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'test_db'
        mock_cursor.fetchall.return_value = [[(db_name,)]]  # Mock the USE statement result
        mock_cursor.fetchall.side_effect = [
            ['table1', 'table2'],  # Mock SHOW TABLES result
            [('col1', 'type1'), ('col2', 'type2')],
            [('col3', 'type3'), ('col4', 'type4')]  # Mock SHOW COLUMNS result
        ]
        mock_rectify.side_effect = lambda **kwargs: kwargs['columns']
        # ----- ACT
        result = self.db_definer.get_database_cols(db_name)
        # ----- ASSERT
        mock_get_db_cursor.assert_called_once()
        self.assertEqual(
            result,
            {
                'table1': [('col1', 'type1'), ('col2', 'type2')],
                'table2': [('col3', 'type3'), ('col4', 'type4')]
            }
        )
        assert mock_cursor.execute.call_count == 4
        mock_cursor.execute.assert_any_call(f"USE {db_name};")
        mock_cursor.execute.assert_any_call("SHOW TABLES;")
        mock_cursor.execute.assert_any_call("SHOW COLUMNS FROM table1;")
        mock_cursor.execute.assert_any_call("SHOW COLUMNS FROM table2;")
        assert mock_cursor.fetchall.call_count == 3
        assert mock_rectify.call_count == 3
        mock_rectify.assert_any_call(
            columns=[('col1', 'type1'), ('col2', 'type2')]
        )
        mock_rectify.assert_any_call(
            columns=[('col3', 'type3'), ('col4', 'type4')]
        )

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_get_database_cols_error(
            self,
            mock_get_db_cursor,
            mock_logger
        ):
        """
        Should return the columns that will be used in the tables.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mariadb.Error("ER_CANNOT_USER")
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'test_db'
        # ----- ACT
        result = self.db_definer.get_database_cols(db_name)
        # ----- ASSERT
        mock_get_db_cursor.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.execute.assert_called_once_with(f"USE {db_name};")

    def test_rectify_this_strange_result(self):
        # ----- ARRANGE
        columns = [
            ('col1', 'type1'),
            ('col2', 'type2')
        ]
        # ----- ACT
        result = self.db_definer.rectify_this_strange_result(columns=columns)
        # ----- ASSERT
        self.assertIsInstance(result, list)
        self.assertEqual(result, ['col1', 'col2'])

    def test_rectify_this_strange_result_str(self):
        # ----- ARRANGE
        columns = [
            'col1', 'col2'
        ]
        # ----- ACT
        result = self.db_definer.rectify_this_strange_result(columns=columns)
        # ----- ASSERT
        self.assertIsInstance(result, list)
        self.assertEqual(result, ['col1', 'col2'])

    def test_get_tables_names(self):
        """
        Should return a list containing the tables names.
        """
        # ----- ARRANGE
        test_type = 'version'
        # ----- ACT
        result = self.db_definer.get_tables_names(test_type)
        # ----- ASSERT
        expected_result = ['version_voc', 'version_perf', 'version_words_count', 'theme_voc']
        self.assertEqual(result, expected_result)
        for table_name in result[:-1]:
            self.assertIn(test_type, table_name)
        test_types = ['version', 'theme']
        test_types.remove(test_type)
        self.assertIn(test_types[0], result[-1])

    @patch('src.data.database_interface.logger')
    def test_get_tables_names_error(self, mock_logger):
        """
        Should return a list containing the tables names.
        """
        # ----- ARRANGE
        test_type = 'gnagnagna'
        # ----- ACT
        with self.assertRaises(ValueError):
            self.db_definer.get_tables_names(test_type)
        # ----- ASSERT
        mock_logger.error.assert_called_once_with(
            f"Wrong test_type argument: {test_type}"
        )

    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_drop_database(self, mock_get_db_cursor):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'mock_db_name'
        # ----- ACT
        result = self.db_definer.drop_database(db_name)
        # ----- ASSERT
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with(
            f"DROP DATABASE {db_name};"
        )
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbDefiner.get_db_cursor')
    def test_drop_database_error(self, mock_get_db_cursor, mock_logger):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mariadb.Error("ER_CANNOT_USER")
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        db_name = 'mock_db_name'
        # ----- ACT
        result = self.db_definer.drop_database(db_name)
        # ----- ASSERT
        mock_cursor.execute.assert_called_once_with(
            f"DROP DATABASE {db_name};"
        )
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()



class TestDbManipulator(unittest.TestCase):
    """
    Should provide all necessary methods to modify data.
    """
    def setUp(self):
        # Data definition
        self.user_name = 'benoit'
        self.db_definer = database_interface.DbDefiner(self.user_name)
        # Data manipulation
        self.db_name = 'English'
        self.table_name = self.user_name + '_' + self.db_name + '.' + 'version_voc'
        self.test_type = 'version'
        self.password = 'test_password'
        self.db_manipulator = database_interface.DbManipulator(
            self.user_name,
            self.db_name,
            self.test_type
        )
        self.words_df = pd.DataFrame({
            'foreign': ['test_english'],
            'native': ['test_french'],
            'score': [42]
        })

    def test_init(self):
        # ----- ARRANGE
        # ----- ACT
        # ----- ASSERT
        self.assertEqual(self.db_manipulator.user_name, self.user_name)
        self.assertEqual(self.db_manipulator.db_name, f"{self.user_name}_{self.db_name}")
        self.assertEqual(self.db_manipulator.test_type, self.test_type)

    def test_init_complete_name(self):
        # ----- ARRANGE
        self.db_name = f"{self.user_name}_{self.db_name}"
        # ----- ACT
        self.db_manipulator = database_interface.DbManipulator(
            self.user_name,
            self.db_name,
            self.test_type
        )
        # ----- ASSERT
        self.assertEqual(self.db_manipulator.user_name, self.user_name)
        self.assertEqual(self.db_manipulator.db_name, self.db_name)
        self.assertEqual(self.db_manipulator.test_type, self.test_type)

    @patch('src.data.database_interface.DbQuerier.read_word')
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_insert_word(self, mock_get_db_cursor, mock_read_word):
        """
        Should add a word to the table.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_read_word.return_value = None
        test_row = ['Bugger off', 'Fous moi le camp']
        today_date = datetime.today().date()
        # ----- ACT
        result = self.db_manipulator.insert_word(test_row)
        # ----- ASSERT
        mock_get_db_cursor.assert_called_once()
        foreign_word = test_row[0]
        native_word = test_row[1]
        request_1 = f"INSERT INTO {self.table_name}"
        request_2 = "(`foreign`, `native`, creation_date, nb, score, taux)"
        request_3 = f"VALUES (\'{foreign_word}\', \'{native_word}\', \'{today_date}\', 0, 0, 0);"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_with(sql_request)
        self.assertTrue(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbQuerier.read_word')
    @patch('src.data.database_interface.DbDefiner.get_tables_names')
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_insert_word_already_exists(
            self,
            mock_get_db_cursor,
            mock_get_tables_names,
            mock_read_word,
            mock_logger
        ):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_get_tables_names.return_value = [
            'version_voc',
            'version_perf',
            'version_count_words',
            'theme_voc'
        ]
        mock_read_word.return_value = ('test_english', 'test_french', 42)
        row = ['Hello', 'Bonjour']
        # ----- ACT
        result = self.db_manipulator.insert_word(row)
        # ----- ASSERT
        self.assertEqual(result, False)
        mock_logger.error.assert_called_once_with(
            'Word already exists'
        )

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbQuerier.read_word')
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_insert_word_error(
            self,
            mock_get_db_cursor,
            mock_read_word,
            mock_logger
        ):
        """
        Should add a word to the table.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mariadb.Error("ER_CANNOT_USER")
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_read_word.return_value = None
        test_row = ['Bugger off', 'Fous moi le camp']
        today_date = datetime.today().date()
        # ----- ACT
        result = self.db_manipulator.insert_word(test_row)
        # ----- ASSERT
        mock_get_db_cursor.assert_called_once()
        english_word = test_row[0]
        native_word = test_row[1]
        request_1 = f"INSERT INTO {self.table_name}"
        request_2 = "(`foreign`, `native`, creation_date, nb, score, taux)"
        request_3 = f"VALUES (\'{english_word}\', \'{native_word}\', \'{today_date}\', 0, 0, 0);"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_with(sql_request)
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_update_word(self, mock_get_db_cursor):
        """
        Should update the word stats after a test.
        """
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        foreign_word = 'test_word'
        new_nb = 4
        new_score = 67
        # Act
        result = self.db_manipulator.update_word(foreign_word, new_nb, new_score)
        # Assert
        request_1 = f"UPDATE {self.table_name}"
        request_2 = f"SET nb = {new_nb}, score = {new_score}"
        request_3 = f"WHERE `foreign` = {foreign_word};"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_once_with(sql_request)
        self.assertTrue(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_update_word_error(self, mock_get_db_cursor, mock_logger):
        """
        Should update the word stats after a test.
        """
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mariadb.Error("ER_CANNOT_USER")
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        foreign_word = 'test_word'
        new_nb = 4
        new_score = 67
        # Act
        result = self.db_manipulator.update_word(foreign_word, new_nb, new_score)
        # Assert
        request_1 = f"UPDATE {self.table_name}"
        request_2 = f"SET nb = {new_nb}, score = {new_score}"
        request_3 = f"WHERE `foreign` = {foreign_word};"
        sql_request = " ".join([request_1, request_2, request_3])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_delete_word(self, mock_get_db_cursor):
        """
        Should delete a word from the table.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        foreign_word = 'test_word'
        # ----- ACT
        result = self.db_manipulator.delete_word(foreign_word)
        # ----- ASSERT
        request_1 = f"DELETE FROM {self.table_name}"
        request_2 = f"WHERE `foreign` = {foreign_word};"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        self.assertTrue(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_delete_word_error(self, mock_get_db_cursor, mock_logger):
        """
        Should delete a word from the table.
        """
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mariadb.Error("ER_CANNOT_USER")
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        foreign_word = 'test_word'
        # ----- ACT
        result = self.db_manipulator.delete_word(foreign_word)
        # ----- ASSERT
        request_1 = f"DELETE FROM {self.table_name}"
        request_2 = f"WHERE `foreign` = {foreign_word};"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_logger.error.assert_called_once()
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    @patch('src.data.database_interface.DbDefiner.get_database_cols')
    @patch('src.data.database_interface.create_engine')
    def test_save_table(
            self,
            mock_create_engine,
            mock_get_database_cols,
            mock_get_db_cursor
        ):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_get_database_cols.return_value = {
            'version_voc': ['col_1', 'col_2'],
            'version_perf': ['col_3', 'col_4'],
            'version_words_count': ['col_5', 'col_6'],
            'theme_voc': ['col_7', 'col_8'],
            'theme_perf': ['col_9', 'col_10'],
            'theme_words_count': ['col_11', 'col_12'],
            'archives': ['col_13', 'col_14']
        }
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        password = 'root_password'
        table_name = 'version_voc'
        table = pd.DataFrame({'col_1': [1, 2], 'col_2': ['a', 'b']})
        # ----- ACT
        result = self.db_manipulator.save_table(table_name, table)
        # ----- ASSERT
        mock_get_db_cursor.assert_called_once()
        mock_create_engine.assert_called_once_with(
            url=f"mysql+pymysql://root:{password}@{self.db_manipulator.host}/{self.db_manipulator.db_name}"
        )
        self.assertTrue(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.database_interface.DbQuerier.get_output_table')
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    @patch('src.data.database_interface.DbDefiner.get_database_cols')
    @patch('src.data.database_interface.create_engine')
    def test_save_table_output(
            self,
            mock_create_engine,
            mock_get_database_cols,
            mock_get_db_cursor,
            mock_get_output_table
        ):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_get_database_cols.return_value = {
            'version_voc': ['foreign', 'native'],
            'version_perf': ['test_date', 'score'],
            'version_words_count': ['test_date', 'words_count'],
            'theme_voc': ['foreign', 'native'],
            'theme_perf': ['test_date', 'score'],
            'theme_words_count': ['test_date', 'words_count'],
            'archives': ['foreign', 'native']
        }
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_get_output_table.return_value = 'theme_voc'
        self.db_manipulator.test_type = 'version'
        password = 'root_password'
        table_name = 'output'
        table = pd.DataFrame({
            'foreign': [1, 2],
            'native': ['a', 'b']
        })
        # ----- ACT
        self.db_manipulator.save_table(table_name, table)
        # ----- ASSERT
        mock_get_db_cursor.assert_called_once()
        mock_create_engine.assert_called_once_with(
            url=f"mysql+pymysql://root:{password}@{self.db_manipulator.host}/{self.db_manipulator.db_name}"
        )
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.database_interface.logger')
    @patch('src.data.database_interface.create_engine')
    @patch('src.data.database_interface.DbDefiner.get_database_cols')
    @patch('src.data.database_interface.DbManipulator.get_db_cursor')
    def test_save_table_error(
            self,
            mock_get_db_cursor,
            mock_get_database_cols,
            mock_create_engine,
            mock_logger
        ):
        # ----- ARRANGE
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        mock_get_database_cols.return_value = {
            'version_voc': ['col_1', 'col_2'],
            'version_perf': ['col_3', 'col_4'],
            'version_words_count': ['col_5', 'col_6'],
            'theme_voc': ['col_7', 'col_8'],
            'theme_perf': ['col_9', 'col_10'],
            'theme_words_count': ['col_11', 'col_12'],
            'archives': ['col_13', 'col_14']
        }
        mock_create_engine.side_effect = mariadb.Error("ER_CANNOT_USER")
        password = 'root_password'
        table_name = 'version_voc'
        table = pd.DataFrame({
            'col_1': [1, 2],
            'col_2': ['a', 'b']
        })
        # ----- ACT
        self.db_manipulator.save_table(table_name, table)
        # ----- ASSERT
        mock_get_db_cursor.assert_called_once()
        mock_create_engine.assert_called_once_with(
            url=f"mysql+pymysql://root:{password}@{self.db_manipulator.host}/{self.db_manipulator.db_name}"
        )
        mock_logger.error.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()



class TestDbQuerier(unittest.TestCase):
    def setUp(self):
        # Data definition
        self.user_name = 'benoit'
        self.db_definer = database_interface.DbDefiner(self.user_name)
        # Data manipulation
        self.db_name = 'English'
        self.table_name = self.user_name + '_' + self.db_name + '.' + 'version_voc'
        self.test_type = 'version'
        self.password = 'test_password'
        self.db_querier = database_interface.DbQuerier(
            self.user_name,
            self.db_name,
            self.test_type
        )
        self.words_df = pd.DataFrame({
            'foreign': ['test_english'],
            'native': ['test_french'],
            'score': [42]
        })

    @patch.dict('os.environ', {'VOC_DB_ROOT_PWD': 'root_password'})
    @patch('src.data.database_interface.DbDefiner.get_database_cols')
    @patch('src.data.database_interface.DbQuerier.get_db_cursor')
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
        result = self.db_querier.get_tables()
        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 7)
        self.assertIn('output', list(result.keys()))
        mock_get_db_cursor.assert_called_once_with()

    def test_get_output_table(self):
        """
        Should go from version to theme
        """
        # ----- ARRANGE
        self.db_querier.test_type = 'version'
        # ----- ACT
        result = self.db_querier.get_output_table()
        # ----- ASSERT
        self.assertEqual(result, 'theme_voc')

    def test_get_output_table_theme(self):
        """
        Should go from theme to theme archives
        """
        # ----- ARRANGE
        self.db_querier.test_type = 'theme'
        # ----- ACT
        result = self.db_querier.get_output_table()
        # ----- ASSERT
        self.assertEqual(result, 'archives')

    @patch('src.data.database_interface.logger')
    def test_get_output_table_error(self, mock_logger):
        """
        Should raise error if test_type is not 'version' or 'theme'.
        """
        # ----- ARRANGE
        self.db_querier.test_type = 'vladivostok'
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.db_querier.get_output_table()
        # ----- ASSERT
        mock_logger.error.assert_called_once_with(
            f"Wrong test_type argument: {self.db_querier.test_type}"
        )

    @patch('src.data.database_interface.DbQuerier.get_db_cursor')
    def test_read_word(self, mock_get_db_cursor):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.return_value = [('test_english', 'test_french', 42)]
        mock_cursor.fetchall.return_value = [('test_english', 'test_french', 42)]
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        foreign_word = self.words_df['foreign'][0]
        # Act
        result = self.db_querier.read_word(foreign_word)
        # Assert
        mock_get_db_cursor.assert_called_once()
        request_1 = f"SELECT `foreign`, `native`, score FROM {self.table_name}"
        request_2 = f"WHERE `foreign` = '{foreign_word}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertEqual(result, ('test_english', 'test_french', 42))

    @patch('src.data.database_interface.DbQuerier.get_db_cursor')
    def test_read_word_error(self, mock_get_db_cursor):
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mariadb.Error("ER_CANNOT_USER")
        mock_get_db_cursor.return_value = (mock_connection, mock_cursor)
        foreign_word = self.words_df['foreign'][0]
        # Act
        result = self.db_querier.read_word(foreign_word)
        # Assert
        mock_get_db_cursor.assert_called_once()
        request_1 = f"SELECT `foreign`, `native`, score FROM {self.table_name}"
        request_2 = f"WHERE `foreign` = '{foreign_word}';"
        sql_request = " ".join([request_1, request_2])
        mock_cursor.execute.assert_called_once_with(sql_request)
        self.assertFalse(result)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()



class TestDbInterfaceFunctions(unittest.TestCase):
    """
    Should provide all necessary methods to query the database
    """
    def test_check_test_type(self):
        """
        Should return the test type if valid
        """
        # ----- ARRANGE
        test_type = 'version'
        # ----- ACT
        result = database_interface.check_test_type(test_type)
        # ----- ASSERT
        self.assertEqual(result, 'version')

    @patch('src.data.database_interface.logger')
    def test_check_test_type_error(self, mock_logger):
        """
        Should raise an error if test type is invalid
        """
        # ----- ARRANGE
        test_type = 'mock_test_type'
        # ----- ACT
        with self.assertRaises(ValueError):
            database_interface.check_test_type(test_type)
        # ----- ASSERT
        mock_logger.error.assert_called_once_with(
            f"Test type {test_type} incorrect, should be either version or theme."
        )
