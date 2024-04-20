"""
    Main purpose:
        Sort of an Object-Relational Mapping tool.
        Focuses on Data Control, Data Definition & Data Manipulation.
"""

import json
import os
import socket
import sys
from abc import ABC
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List

import mysql.connector as mariadb
import pandas as pd
from loguru import logger
from sqlalchemy import create_engine

load_dotenv()

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

with open(REPO_DIR + '/conf/data.json', 'r', encoding='utf-8') as param_file:
    PARAMS = json.load(param_file)
HOSTS = PARAMS['host'].keys()



class DbInterface(ABC):
    """
    Abstract class that provides with a method to connect to a database.
    All methods invoked by the user should provide with a host name.
    """
    def __init__(self):
        self.host = PARAMS['host'][socket.gethostname()]

    def get_db_cursor(self):
        """
        Connect to vocabulary database if credentials are correct.
        # """
        user_name = 'root'
        password = os.getenv('VOC_DB_ROOT_PWD')
        db_name = 'mysql'
        # logger.debug(f"port: {PARAMS['port']}")
        connection_config = {
            'user': user_name,
            'password': password,
            'database': db_name,
            'port': PARAMS['port']
        }
        if self.host not in HOSTS:
            logger.warning(f"host: {self.host}")
            logger.error(f"host should be in {HOSTS}")
        else:
            connection_config['host'] = PARAMS['host'][self.host]
        # logger.debug(f"host: {PARAMS['host'][self.host]}")
        connection = mariadb.connect(**connection_config)
        cursor = connection.cursor()
        return connection, cursor



class DbController(DbInterface):
    """
    Manage access.
    """
    def create_user_in_mysql(self, user_name, user_password):
        """
        Create a user in the mysql.user table.
        """
        connection, cursor = self.get_db_cursor()
        result = None
        try:
            cursor.execute(
                f"CREATE USER '{user_name}'@'{self.host}' IDENTIFIED BY '{user_password}';"
            )
            connection.commit()
            result = True
        except Exception as err:
            if err.errno in [1396, 1973]:
                logger.error(f"User '{user_name}' already exists.")
                result = False
            elif err.errno == -1:
                logger.error(f"Mock error")
                result = False
            else:
                logger.error(f"Error number: {err.errno}")
                logger.error(err)
        finally:
            cursor.close()
            connection.close()
        return result

    def grant_privileges_on_common_database(self, user_name):
        """
        Grant the new user access to the common database.
        """
        connection, cursor = self.get_db_cursor()
        result = None
        try:
            cursor.execute(f"GRANT SELECT ON common.* TO '{user_name}'@'{self.host}';")
            connection.commit()
            logger.success(f"User '{user_name}' created on {self.host}.")
            result = True
        except mariadb.Error as err:
            logger.error(err)
            result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def grant_privileges(self, user_name, db_name):
        """
        Grant privileges to the user on the given database.
        """
        connection, cursor = self.get_db_cursor()
        result = None
        try:
            request_1 = "GRANT SELECT, INSERT, UPDATE, CREATE, DROP ON "
            request_2 = f"{user_name}_{db_name}.* TO '{user_name}'@'{self.host}';"
            cursor.execute(request_1 + request_2)
            connection.commit()
            logger.success(
                f"User '{user_name}' granted access to '{user_name}_{db_name}'."
            )
            result = True
        except mariadb.Error as err:
            logger.error(err)
            result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def get_users_list_from_mysql(self) -> List[str]:
        """
        For management purpose, not the usual app purpose.
        Get list of users registered in mysql table.
        Keep in mind that the user is first created on '%' and then on 'localhost'.
        """
        connection, cursor = self.get_db_cursor()
        users_list = []
        try:
            cursor.execute("SELECT User, Host FROM mysql.user;")
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            df = df[df['Host'] == self.host]
            users_list = df['User'].tolist()
        except mariadb.Error as err:
            logger.error(err)
        finally:
            cursor.close()
            connection.close()
        return users_list

    def add_user_to_users_table(
            self,
            user_name: str,
            hash_password: str,
            user_email: str=None
        ):
        """
        Add a user to the users MariaDB table in users Database.
        """
        connection, cursor = self.get_db_cursor()
        try:
            cursor.execute(
                f"INSERT INTO `users`.`voc_users` \
                (`username`, `password_hash`, `email`, `disabled`) \
                VALUES('{user_name}', '{hash_password}', '{user_email}', FALSE);"
            )
            connection.commit()
            logger.success(f"User '{user_name}' added to users table.")
        except mariadb.Error as err:
            logger.error(err)
        finally:
            cursor.close()
            connection.close()
        return True

    def get_users_list(self) -> List[Dict]:
        """
        Get list of users registered in users table.
        """
        connection, cursor = self.get_db_cursor()
        users_list = []
        try:
            cursor.execute(
                "SELECT username, password_hash, email, disabled FROM users.voc_users;"
            )
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            users_df = pd.DataFrame(result, columns=columns)
            users_str = users_df.to_json(orient='records')
            users_list = json.loads(users_str)
        except mariadb.Error as err:
            logger.error(err)
        finally:
            cursor.close()
            connection.close()
        return users_list

    def revoke_privileges(self, user_name, db_name):
        """
        Remove privileges from the user on the given database.
        """
        connection, cursor = self.get_db_cursor()
        result = None
        try:
            request_1 = "REVOKE SELECT, INSERT, UPDATE, CREATE, DROP ON "
            request_2 = f"{db_name}.* FROM '{user_name}'@'{self.host}';"
            cursor.execute(request_1 + request_2)
            connection.commit()
            logger.success(
                f"User '{user_name}' removed from '{user_name}_{db_name}'."
            )
            result = True
        except mariadb.Error as err:
            logger.error(err)
            result = False
        finally:
            cursor.close()
            connection.close()
        return result



class DbDefiner(DbInterface):
    """
    Define database structure.
    """
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.db_name = None

    def create_database(self, db_name):
        """
        Create a database with the given database name
        """
        connection, cursor = self.get_db_cursor()
        result = None
        try:
            cursor.execute(f"CREATE DATABASE {self.user_name}_{db_name};")
            connection.commit()
            result = True
        except mariadb.Error as err:
            logger.error(err)
            result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def get_user_databases(self):
        """
        Get the list of databases for the user.
        """
        connection, cursor = self.get_db_cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{self.user_name}_%';")
        databases = [db[0] for db in cursor.fetchall()]
        cursor.close()
        connection.close()
        return databases

    def create_seven_tables(self, db_name):
        """
        Create the seven tables necessary to the app.
        """
        sql_db_name = f"{self.user_name}_{db_name}"
        connection, cursor = self.get_db_cursor()
        try:
            cursor.execute(f"USE {sql_db_name};")
            cursor.execute(
                "CREATE TABLE version_voc (id INT AUTO_INCREMENT PRIMARY KEY, english VARCHAR(50), français VARCHAR(50), creation_date DATE, nb INT, score INT, taux INT);"
            )
            cursor.execute(
                "CREATE TABLE version_perf (test_date DATE, score INT, taux INT);"
            )
            cursor.execute(
                "CREATE TABLE version_words_count (test_date DATE, nb INT);"
            )
            cursor.execute(
                "CREATE TABLE theme_voc (id INT AUTO_INCREMENT PRIMARY KEY, english VARCHAR(50), français VARCHAR(50), creation_date DATE, nb INT, score INT, taux INT);"
            )
            cursor.execute(
                "CREATE TABLE theme_perf (test_date DATE, score INT, taux INT);"
            )
            cursor.execute(
                "CREATE TABLE theme_words_count (test_date DATE, nb INT);"
            )
            cursor.execute(
                "CREATE TABLE archives (id INT AUTO_INCREMENT PRIMARY KEY, english VARCHAR(50), français VARCHAR(50), creation_date DATE, nb INT, score INT, taux INT);"
            )
            connection.commit()
            result = True
        except mariadb.Error as err:
            logger.error(err)
            result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def get_database_cols(self, db_name):
        """
        Get table columns.
        """
        connection, cursor = self.get_db_cursor()
        try:
            cursor.execute(f"USE {db_name};")
            cursor.execute("SHOW TABLES;")
            tables = list(cursor.fetchall())
            cols_dict = {}
            for table_name in tables:
                if isinstance(table_name, tuple):
                    true_table_name = table_name[0]
                elif isinstance(table_name, str):
                    true_table_name = table_name
                cursor.execute(f"SHOW COLUMNS FROM {true_table_name};")
                columns = list(cursor.fetchall())
                # logger.debug(f"columns: {columns}")
                columns = self.rectify_this_strange_result(columns)
                # logger.debug(f"columns: {columns}")
                cols_dict[true_table_name] = columns
            # logger.debug(f"cols_dict: {cols_dict}")
        except mariadb.Error as err:
            logger.error(err)
        finally:
            cursor.close()
            connection.close()
        return cols_dict

    def rectify_this_strange_result(self, result):
        """
        Correct the result of the 'SHOW COLUMNS FROM table_name' request.
        """
        if isinstance(result[0], tuple):
            result = [col[0] for col in result]
        elif isinstance(result[0], str):
            pass
        return result

    def get_tables_names(self, test_type) -> List[str]:
        """
        Get version or theme table according to the test type.
        """
        test_types = ['version', 'theme']
        if test_type in test_types:
            voc_table = test_type + '_voc'
            perf_table = test_type + '_perf'
            word_cnt_table = test_type + '_words_count'
            test_types.remove(test_type)
            output_table = test_types[0] + '_voc'
        else:
            logger.error(f"Wrong test_type argument: {test_type}")
            raise ValueError
        return [voc_table, perf_table, word_cnt_table, output_table]

    def drop_database(self, db_name):
        """
        Drop the given database.
        """
        connection, cursor = self.get_db_cursor()
        try:
            cursor.execute(f"DROP DATABASE {db_name};")
            connection.commit()
            result = True
        except mariadb.Error as err:
            logger.error(err)
            result = False
        finally:
            cursor.close()
            connection.close()
        return result



class DbManipulator(DbInterface):
    """
    Working with data.
    """
    def __init__(self, user_name, db_name, test_type):
        super().__init__()
        self.user_name = user_name
        if self.user_name not in db_name:
            self.db_name = f"{user_name}_{db_name}"
        else:
            self.db_name = db_name
        self.db_definer = DbDefiner(self.user_name)
        self.test_type = ''
        self.check_test_type(test_type)

    def check_test_type(self, test_type):
        """
        Check the test type attribute.
        """
        if test_type not in ['version', 'theme']:
            logger.error(
                f"Test type {test_type} incorrect, should be either version or theme."
            )
        self.test_type = test_type

    def get_tables(self):
        """
        Load the different tables necessary to the app.
        """
        connection, cursor = self.get_db_cursor()
        cursor.execute(f"USE {self.db_name};")
        cols = self.db_definer.get_database_cols(self.db_name)
        tables_names = list(cols.keys())
        tables = {}
        for table_name in tables_names:
            sql_request = f"SELECT * FROM {table_name}"
            cursor.execute(sql_request)
            tables[table_name] = pd.DataFrame(
                columns=cols[table_name],
                data=cursor.fetchall()
            )
            index_col = tables[table_name].columns[0]
            tables[table_name] = tables[table_name].set_index(index_col)
        # Special case of output table
        output_table = self.get_output_table()
        tables['output'] = tables[output_table]
        tables.pop(output_table)
        cursor.close()
        connection.close()
        return tables

    def get_output_table(self):
        """
        Rename the output name according to the test type.
        """
        if self.test_type == 'version':
            output_table = 'theme_voc'
        elif self.test_type == 'theme':
            output_table = 'archives'
        else:
            logger.error(f"Wrong test_type argument: {self.test_type}")
            raise SystemExit
        return output_table

    def insert_word(self, row: list):
        """
        Add a word to the table.
        """
        connection, cursor = self.get_db_cursor()
        # Create request string
        today_str = str(datetime.today().date())
        words_table_name, _, _, _ = self.db_definer.get_tables_names(self.test_type)
        english = row[0]
        logger.debug(f"english: {english}")
        if self.read_word(english) is not None:
            result = 'Word already exists'
            logger.error(result)
            return result
        native = row[1]
        try:
            request_1 = f"INSERT INTO {self.db_name}.{words_table_name}"
            request_2 = "(english, français, creation_date, nb, score, taux)"
            request_3 = f"VALUES (\'{english}\', \'{native}\', \'{today_str}\', 0, 0, 0);"
            cursor.execute(' '.join([request_1, request_2, request_3]))
            connection.commit()
            result = True
        except:
            result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def read_word(self, english: str):
        """
        Read the given word
        """
        connection, cursor = self.get_db_cursor()
        # Create request string
        words_table_name, _, _, _ = self.db_definer.get_tables_names(self.test_type)
        request_1 = "SELECT english, français, score"
        request_2 = f"FROM {self.db_name}.{words_table_name}"
        request_3 = f"WHERE english = '{english}';"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        try:
            request_result = cursor.execute(sql_request)
            request_result = cursor.fetchall()
            english, native, score = request_result[0]
            result = (english, native, score)
        except IndexError:
            result = None
        except ValueError:
            result = None
        cursor.close()
        connection.close()
        return result

    def update_word(self, english: str, new_nb, new_score):
        """
        Update statistics on the given word
        """
        # Create request string
        words_table_name, _, _, _ = self.db_definer.get_tables_names(self.test_type)
        request_1 = f"UPDATE {self.db_name }.{words_table_name}"
        request_2 = f"SET nb = {new_nb}, score = {new_score}"
        request_3 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        connection, cursor = self.get_db_cursor()
        cursor.execute(sql_request)
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def delete_word(self, english):
        """
        Delete a word from the words table of the instance database.
        """
        # Create request string
        words_table_name, _, _, _ = self.db_definer.get_tables_names(self.test_type)
        request_1 = f"DELETE FROM {self.db_name}.{words_table_name}"
        request_2 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2])
        # Execute request
        connection, cursor = self.get_db_cursor()
        cursor.execute(sql_request)
        connection.commit()
        cursor.close()
        connection.close()
        return True

    def save_table(self, table_name: str, table: pd.DataFrame):
        """
        Save given table.
        """
        connection, cursor = self.get_db_cursor()
        cols = self.db_definer.get_database_cols(self.db_name)
        if table_name == 'output':
            if self.test_type == 'version':
                table_name = 'theme_voc'
            elif self.test_type == 'theme':
                table_name = 'archives'
        # logger.debug(f"table_name: {table_name}")
        # logger.debug(f"table columns: {table.columns}")
        # logger.debug(f"cols[table_name]: {cols[table_name]}")
        table = table[cols[table_name]]
        engine = create_engine(
            ''.join([
                "mysql+pymysql",
                "://", 'root',
                ':', os.getenv('VOC_DB_ROOT_PWD'),
                '@', self.host,
                '/', self.db_name.lower()
            ])
        )
        table.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            method='multi',
            index=False
        )
        cursor.close()
        connection.close()
