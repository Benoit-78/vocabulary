"""
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



class MariaDBHandler():
    """
    Provide with all methods necessary to interact with MariaDB database.
    """
    def __init__(self, test_type: str, mode: str, language_1: str):
        if test_type not in ['version', 'theme']:
            logger.error(f"Test type {test_type} incorrect, \
            should be either version or theme.")
        self.test_type = test_type
        self.os_sep = utils.get_os_separator()
        self.mode = mode
        self.language_1 = language_1
        self.config = {}
        self.connection = None
        self.cursor = None

    # Common operations
    def get_database_cred(self):
        """
        Get credentials necessary for connection with vocabulary database.
        """
        cred_path = self.os_sep.join([REPO_DIR, 'conf', 'cred.json'])
        with open(cred_path, 'rb') as cred_file:
            cred = json.load(cred_file)
        return cred

    def get_database_cols(self):
        """Get table columns."""
        if os.getcwd().endswith('tests'):
            os.chdir('..')
        col_path = self.os_sep.join([os.getcwd(), 'conf', 'columns.json'])
        with open(col_path, 'rb') as col_file:
            cols = json.load(col_file)
        return cols

    def set_db_cursor(self):
        """Connect to vocabulary database if credentials are correct."""
        cred = self.get_database_cred()
        self.config = {
            'user': cred['users']['user_1']['name'],
            'password': cred['users']['user_1']['password'],
            'database': self.language_1.lower(),
            'port': cred['port']
        }
        if self.mode not in HOSTS:
            logger.warning(f"Mode: {self.mode}")
            logger.error(f"Mode should be in {HOSTS}")
        else:
            self.config['host'] = cred['host'][self.mode]
        self.connection = mariadb.connect(**self.config)
        self.cursor = self.connection.cursor()

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
            print("ERROR: Wrong test_type argument:", self.test_type)
            raise ValueError
        return [voc_table, perf_table, word_cnt_table, output_table]

    # Table-level operations
    def get_tables(self):
        """Load the different tables necessary to the app."""
        self.set_db_cursor()
        cols = self.get_database_cols()
        tables_names = self.get_tables_names()
        tables = {}
        for table_name in tables_names:
            logger.debug(table_name)
            sql_request = f"SELECT * FROM {table_name}"
            self.cursor.execute(sql_request)
            tables[table_name] = pd.DataFrame(
                columns=cols[self.language_1][table_name]["Columns"],
                data=self.cursor.fetchall()
            )
            index_col = tables[table_name].columns[0]
            tables[table_name] = tables[table_name].set_index(index_col)
        # Special case of output table
        tables['output'] = tables[tables_names[-1]]
        tables.pop(tables_names[-1])
        self.cursor.close()
        self.connection.close()
        return tables

    def save_table(self, table_name: str, table: pd.DataFrame):
        """Save given table."""
        self.set_db_cursor()
        cols = self.get_database_cols()
        if table_name == 'output':
            if self.test_type == 'version':
                table_name = 'theme_voc'
            elif self.test_type == 'theme':
                table_name = 'archives'
        logger.debug(f"Table name: {table_name}")
        logger.debug(f"Table columns: {table.columns}")
        table = table[cols[self.language_1][table_name]["Columns"]]
        engine = create_engine(
            ''.join([
                "mysql+pymysql",
                "://", self.config['user'],
                ':', self.config['password'],
                '@', self.config['host'],
                '/', self.language_1.lower()
            ])
        )
        table.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            method='multi',
            index=False
        )
        self.cursor.close()
        self.connection.close()

    # Row-level operations
    def create(self, row: list, test_mode=False):
        """Add a word to the table"""
        # Create request string
        today_date = datetime.today().date()
        if test_mode:
            table_name = 'test_table'
        else:
            table_name = self.language_1 + '.' + 'version_voc'
        english = row[0]
        native = row[1]
        request_1 = f"INSERT INTO {table_name} \
            (english, français, creation_date, nb, score, taux)"
        request_2 = f"VALUES (\'{english}\', \'{native}\', \'{today_date}\', 0, 0, 0);"
        sql_request = " ".join([request_1, request_2])
        # Execute request
        self.set_db_cursor()
        self.cursor.execute(sql_request)
        self.connection.close()
        return True

    def read(self, word_series: pd.DataFrame):
        """Read the given word"""
        # Create request string
        table_name, _, _, _ = self.get_tables_names()
        english, native = self.get_words_from_df(word_series)
        request_1 = "SELECT english, français, score"
        request_2 = f"FROM {table_name}"
        request_3 = f"WHERE english = '{english}';"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        self.set_db_cursor()
        english, native, score = self.cursor.execute(sql_request)
        # self.cursor.execute(sql_request)
        # result = self.cursor.fetchone()
        # if result:
        #     english, native, score = result
        # else:
        #     english, native, score = None, None, None
        self.connection.close()
        return english, native, score

    def update(self, word_series: pd.DataFrame, new_nb, new_score):
        """Update statistics on the given word"""
        # Create request string
        table_name, _, _, _ = self.get_tables_names()
        english, _ = self.get_words_from_df(word_series)
        request_1 = f"UPDATE {table_name}"
        request_2 = f"SET nb = {new_nb}, score = {new_score}"
        request_3 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        self.set_db_cursor()
        self.cursor.execute(sql_request)
        self.connection.close()
        return True

    def delete(self, word_series: pd.DataFrame):
        """Delete a word from table."""
        # Create request string
        table_name, _, _, _ = self.get_tables_names()
        english, _ = self.get_words_from_df(word_series)
        request_1 = f"DELETE FROM {table_name}"
        request_2 = f"WHERE english = {english}"
        sql_request = " ".join([request_1, request_2])
        # Execute request
        self.set_db_cursor()
        self.cursor.execute(sql_request)
        self.connection.close()
        return True

    def get_words_from_df(self, word_series: pd.DataFrame):
        """Common method used by all 4 CRUD operations"""
        english = word_series[word_series.columns[0]]
        native = word_series[word_series.columns[1]]
        return english, native
