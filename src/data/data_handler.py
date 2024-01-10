"""
    Main purpose:
        Methods for CRUD operations.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List

import mysql.connector as mariadb
import pandas as pd
from loguru import logger
from sqlalchemy import create_engine

REPO_DIR = os.getcwd().split('src')[0]
sys.path.append(REPO_DIR)
from src import utils

HOSTS = ['cli', 'web_local', 'container']

with open(REPO_DIR + '/conf/data.json', 'r') as param_file:
    PARAMS = json.load(param_file)



class CsvHandler():
    """Provide with all methods necessary to interact with csv files."""
    def __init__(self, test_type: str):
        self.test_type = test_type
        self.os_sep = utils.get_os_separator()
        self.paths = {}
        self.tables = {}

    # Table-level operations
    def set_paths(self):
        """List paths to data csv."""
        self.paths[self.test_type + '_voc'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_voc.csv']
        )
        self.paths[self.test_type + '_perf'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_perf.csv']
        )
        self.paths[self.test_type + '_word_cnt'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_words_count.csv']
        )
        if self.test_type == 'version':
            self.paths['output'] = self.os_sep.join(['.', 'data', 'theme_voc.csv'])
        elif self.test_type == 'theme':
            self.paths['output'] = self.os_sep.join(['.', 'data', 'archives.csv'])
        else:
            logger.error(f"Wrong test_type argument: {self.test_type}")
            raise SystemExit

    def set_tables(self):
        """Load the different tables necessary to the app."""
        self.set_paths()
        self.tables[self.test_type + '_voc'] = pd.read_csv(
            self.paths[self.test_type + '_voc'],
            sep=';',
            encoding='utf-8'
        )
        self.tables[self.test_type + '_perf'] = pd.read_csv(
            self.paths[self.test_type + '_perf'],
            sep=';',
            encoding='utf-8'
        )
        self.tables[self.test_type + '_word_cnt'] = pd.read_csv(
            self.paths[self.test_type + '_word_cnt'],
            sep=';',
            encoding='utf-8'
        )
        self.tables['output'] = pd.read_csv(
            self.paths['output'],
            sep=';',
            encoding='utf-8'
        )

    def get_paths(self) -> Dict[str, str]:
        """Return the paths"""
        self.set_paths()
        return self.paths

    def get_tables(self) -> Dict[str, pd.DataFrame]:
        """Load the tables"""
        self.set_tables()
        return self.tables

    def save_table(self, table_name: str, table: pd.DataFrame):
        """Save given table."""
        self.set_paths()
        table.to_csv(
            self.paths[table_name],
            index=False,
            sep=';',
            encoding='utf-8'
        )

    # Row-level operations
    def create(self, word, table):
        """Add a word to the table."""

    def read(self, word, table):
        """Read the given word."""

    def update(self, word, table):
        """Update statistics on the given word."""

    def delete(self, word, table):
        """Delete the given word in the given table."""

    def transfer(self, word, table):
        """Copy a word from its original table to the output table (theme or archive)."""



def get_db_cursor(user_name, host, db_name, password):
    """Connect to vocabulary database if credentials are correct."""
    connection_config = {
        'user': user_name,
        'password': password,
        'database': db_name,
        'port': PARAMS['MariaDB']['port']
    }
    if host not in HOSTS:
        logger.warning(f"host: {host}")
        logger.error(f"host should be in {HOSTS}")
    else:
        connection_config['host'] = PARAMS['host'][host]
    connection = mariadb.connect(**connection_config)
    cursor = connection.cursor()
    return connection, cursor



class DbController():
    """Manage access and transactions"""
    def __init__(self, host):
        self.host = host

    def create_user(self, root_password, user_name, user_password):
        """Create user"""
        connection, cursor = get_db_cursor('root', self.host, 'root', root_password)
        try:
            cursor.execute(f"CREATE USER '{user_name}'@'%' IDENTIFIED BY '{user_password}';")
            connection.commit()
            logger.success(f"User '{user_name}' created successfully.")
        except mysql.connector.Error as err:
            logger.error(err)
        finally:
            cursor.close()
            connection.close()
        return True

    def grant_all_privileges(self, root_password, , user_name, db_name):
        """Grant privileges to the user on the given database"""
        connection, cursor = get_db_cursor('root', self.host, 'root', password)
        cursor.execute(f"GRANT ALL PRIVILEGES ON {user_name}_{db_name}.* TO '{user_name}'@'%'")
        connection.commit()
        cursor.close()
        connection.close()



class DbDefiner():
    """Define database structure"""
    def __init__(self, user_name, host):
        self.user_name = user_name
        self.host = host
        self.db_name = None
        self.test_type = ''

    def create_database(self, db_name):
        """Create a database with the given database name"""
        db_controller = DbController(self.host)
        connection, cursor = get_db_connection()
        try:
            self.cursor.execute(f"CREATE DATABASE {self.user_name}_{db_name}")
            connection.commit()
            logger.success(f"Database '{self.user_name}_{db_name}' created successfully.")
            db_controller.grant_all_privileges(db_name)
            logger.success(f"User '{self.user_name}' granted access to '{self.user_name}_{db_name}'.")
        except mysql.connector.Error as err:
            logger.error(err)
        finally:
            cursor.close()
            connection.close()

    def set_test_type(self, test_type):
        if test_type not in ['version', 'theme']:
            logger.error(f"Test type {test_type} incorrect, \
            should be either version or theme.")
        self.test_type = test_type

    def get_database_cols(self, db_name, password):
        """Get table columns."""
        connection, cursor = get_db_cursor(self.user_name, self.host, db_name, password)
        try:
            cursor.execute(f"USE {db_name};")
            # db_name = list(cursor.fetchall())
            logger.debug(f"Database: {db_name}")
            cursor.execute("SHOW TABLES;")
            tables = list(cursor.fetchall())
            # tables = [table[0] for table in cursor.fetchall()]
            logger.debug(f"Tables: {tables}")
            cols_dict = {}
            for table_name in tables:
                logger.debug(f"Table: {table_name}")
                cursor.execute(f"SHOW COLUMNS FROM {table_name};")
                columns = list(cursor.fetchall())
                logger.debug(f"Columns: {columns}")
                cols_dict[table_name] = columns
                logger.debug(f"Columns: {cols_dict}")
        except mariadb.Error as err:
            logger.error(err)
        finally:
            cursor.close()
            connection.close()
        return cols_dict

    def get_tables_names(self) -> List[str]:
        """Get version or theme table according to the test type."""
        test_types = ['version', 'theme']
        if self.test_type in test_types:
            voc_table = self.test_type + '_voc'
            perf_table = self.test_type + '_perf'
            word_cnt_table = self.test_type + '_words_count'
            test_types.remove(self.test_type)
            output_table = test_types[0] + '_voc'
        else:
            logger.error(f"Wrong test_type argument: {self.test_type}")
            raise ValueError
        return [voc_table, perf_table, word_cnt_table, output_table]



class DbManipulator():
    """Working with data"""
    def __init__(self, user_name, db_name, host, test_type):
        self.user_name = user_name
        self.db_name = db_name
        self.host = host
        self.test_type = test_type
        self.db_definer = DbDefiner(self.user_name, self.host)

    def get_tables(self, password):
        """Load the different tables necessary to the app."""
        connection, cursor = get_db_cursor(self.user_name, self.host, self.db_name, password)
        cols = self.db_definer.get_database_cols(self.db_name, password)
        tables_names = self.db_definer.get_tables_names()
        tables = {}
        for table_name in tables_names:
            sql_request = f"SELECT * FROM {table_name}"
            cursor.execute(sql_request)
            tables[table_name] = pd.DataFrame(
                columns=cols[self.db_name][table_name]["Columns"],
                data=cursor.fetchall()
            )
            index_col = tables[table_name].columns[0]
            tables[table_name] = tables[table_name].set_index(index_col)
        # Special case of output table
        tables['output'] = tables[tables_names[-1]]
        tables.pop(tables_names[-1])
        cursor.close()
        connection.close()
        return tables

    def insert_word(self, row: list, password):
        """Add a word to the table"""
        # Create request string
        today_date = datetime.today().date()
        table_name = self.db_name + '.' + 'version_voc'
        english = row[0]
        native = row[1]
        request_1 = f"INSERT INTO {table_name} (english, français, creation_date, nb, score, taux)"
        request_2 = f"VALUES (\'{english}\', \'{native}\', \'{today_date}\', 0, 0, 0);"
        sql_request = " ".join([request_1, request_2])
        # Execute request
        connection, cursor = get_db_cursor(
            self.user_name, self.host, self.db_name, password
        )
        cursor.execute(sql_request)
        cursor.close()
        connection.close()
        return True

    def read(self, word_series: pd.DataFrame, password):
        """Read the given word"""
        # Create request string
        self.db_definer.set_test_type(self.test_type)
        table_name, _, _, _ = self.db_definer.get_tables_names()
        english, native = self.get_words_from_df(word_series)
        request_1 = "SELECT english, français, score"
        request_2 = f"FROM {table_name}"
        request_3 = f"WHERE english = '{english}';"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        connection, cursor = get_db_cursor(self.user_name, self.host, self.db_name, password)
        english, native, score = cursor.execute(sql_request)[0]
        cursor.close()
        connection.close()
        return english, native, score

    def update(self, word_series: pd.DataFrame, new_nb, new_score, password):
        """Update statistics on the given word"""
        # Create request string
        table_name, _, _, _ = self.db_definer.get_tables_names()
        english, _ = self.get_words_from_df(word_series)
        request_1 = f"UPDATE {table_name}"
        request_2 = f"SET nb = {new_nb}, score = {new_score}"
        request_3 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        connection, cursor = get_db_cursor(self.user_name, self.host, self.db_name, password)
        cursor.execute(sql_request)
        cursor.close()
        connection.close()
        return True

    def delete(self, word_series: pd.DataFrame, password):
        """Delete a word from table."""
        # Create request string
        table_name, _, _, _ = self.db_definer.get_tables_names()
        english, _ = self.get_words_from_df(word_series)
        request_1 = f"DELETE FROM {table_name}"
        request_2 = f"WHERE english = {english}"
        sql_request = " ".join([request_1, request_2])
        # Execute request
        connection, cursor = get_db_cursor(self.user_name, self.host, self.db_name, password)
        cursor.execute(sql_request)
        cursor.close()
        connection.close()
        return True

    def get_words_from_df(self, word_series: pd.DataFrame):
        """Common method used by all 4 CRUD operations"""
        english = word_series[word_series.columns[0]][0]
        native = word_series[word_series.columns[1]][0]
        return english, native

    def save_table(self, table_name: str, table: pd.DataFrame, password):
        """Save given table."""
        connection, cursor = get_db_cursor(self.user_name, self.host, self.db_name, password)
        cols = self.get_database_cols()
        if table_name == 'output':
            if self.test_type == 'version':
                table_name = 'theme_voc'
            elif self.test_type == 'theme':
                table_name = 'archives'
        table = table[cols[self.db_name][table_name]["Columns"]]
        engine = create_engine(
            ''.join([
                "mysql+pymysql",
                "://", self.user_name,
                ':', password,
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
