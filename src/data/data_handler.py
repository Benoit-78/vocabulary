"""
    Methods for CRUD operations.
"""

import json
from datetime import datetime
from typing import List
import mysql.connector as mariadb
import pandas as pd
from sqlalchemy import create_engine
from loguru import logger

from typing import Dict

import utils



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
        self.paths['voc'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_voc.csv']
        )
        self.paths['perf'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_perf.csv']
        )
        self.paths['word_cnt'] = self.os_sep.join(
            [r'.', 'data', self.test_type + '_words_count.csv']
        )
        if self.test_type == 'version':
            self.paths['output'] = self.os_sep.join(['.', 'data', 'theme_voc.csv'])
        elif self.test_type == 'theme':
            self.paths['output'] = self.os_sep.join(['.', 'data', 'archives.csv'])
        else:
            print("# ERROR: Wrong test_type argument:", self.test_type)
            raise SystemExit

    def set_tables(self):
        """Load the different tables necessary to the app."""
        self.set_paths()
        self.tables['voc'] = pd.read_csv(self.paths['voc'], sep=';', encoding='utf-8')
        self.tables['perf'] = pd.read_csv(self.paths['perf'], sep=';', encoding='utf-8')
        self.tables['word_cnt'] = pd.read_csv(self.paths['word_cnt'], sep=';', encoding='utf-8')
        self.tables['output'] = pd.read_csv(self.paths['output'], sep=';', encoding='utf-8')

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
        pass

    def read(self, word, table):
        """Read the given word."""
        pass

    def update(self, word, table):
        """Update statistics on the given word."""
        pass

    def delete(self, word, table):
        """Delete the given word in the given table."""
        pass

    def transfer(self, word, table):
        """Copy a word from its original table to the output table (theme or archive)."""
        pass



class MariaDBHandler():
    """Provide with all methods necessary to interact with MariaDB database."""
    def __init__(self, test_type: str, mode: str):
        self.test_type = test_type
        self.mode = mode
        self.params = {}
        self.config = {}
        self.connection = None
        self.cursor = None
        self.hosts = ['cli', 'web_local', 'container']

    # Common operations
    def set_database_cred(self):
        """Get credentials necessary for connection with vocabulary database."""
        os_sep = utils.get_os_separator()
        cred_path = os_sep.join(['..', 'conf', 'cred.json'])
        with open(cred_path, 'rb') as cred_file:
            self.params = json.load(cred_file)

    def set_db_cursor(self):
        """Connect to vocabulary database if credentials are correct."""
        self.config = {
            'user': self.params['Database']['user']['user_1']['name'],
            'password': self.params['Database']['user']['user_1']['password'],
            'database': self.params['Database']['database'],
            'port': self.params['Database']['port']
        }
        if self.mode not in self.hosts:
            logger.warning(f"Mode: {self.mode}")
            logger.error(f"Mode should be in {self.hosts}")
        else:
            self.config['host'] = self.params['Database']['host'][self.mode]
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

    def get_words_from_test_type(self, test_type: str, row: list):
        """Common method used by all 4 CRUD operations"""
        [words_table_name, _, _, _] = get_words_table_from_test_type(test_type)
        english = row[row.columns[0]]
        native = row[row.columns[1]]
        return [words_table_name, english, native]

    # Table-level operations
    def get_tables(self):
        """Load the different tables necessary to the app."""
        self.set_database_cred()
        self.set_db_cursor()
        tables_names = self.get_tables_names()
        tables = {}
        for table_name in tables_names:
            sql_request = f"SELECT * FROM {table_name}"
            self.cursor.execute(sql_request)
            tables[table_name] = pd.DataFrame(
                columns=self.params["Tables"][table_name]["Columns"],
                data=self.cursor.fetchall()
            )
            index_col = tables[table_name].columns[0]
            tables[table_name] = tables[table_name].set_index(index_col)
        self.cursor.close()
        self.connection.close()
        return tables

    def save_table(self, table_name: str, table: pd.DataFrame):
        """Save given table."""
        self.set_database_cred()
        self.set_db_cursor()
        table = table[self.params["Tables"][table_name]["Columns"]]
        engine = create_engine(
            ''.join([
                "mysql+pymysql",
                "://", self.config['user'],
                ':', self.config['password'],
                '@', self.config['host'],
                '/', self.config['database']
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
    def create(self, test_type, row):
        """Add a word to the table"""
        # Create request string
        today = datetime.now()
        table_name, english, native = get_words_from_test_type(test_type, row)
        request_1 = f"INSERT INTO {table_name} (english, francais, Date, Nb, Score, Taux)"
        request_2 = f"VALUES ({english}, {native}, {today}, 0, 0, 0);"
        sql_request = " ".join([request_1, request_2])
        # Execute request
        cred = get_database_cred()
        connection, cursor = get_db_cursor(cred)
        cursor.execute(sql_request)
        connection.close()
        return True

    def read(self, test_type, row):
        """Read the given word"""
        # Create request string
        table_name, english, native = get_words_from_test_type(test_type, row)
        request_1 = "SELECT english, native, Score"
        request_2 = f"FROM {table_name}"
        request_3 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        cred = get_database_cred()
        connection, cursor = get_db_cursor(cred)
        english, native, score = cursor.execute(sql_request)
        connection.close()
        return english, native, score

    def update(self, test_type, row, new_nb, new_score):
        """Update statistics on the given word"""
        # Create request string
        table_name, english, _ = get_words_from_test_type(test_type, row)
        request_1 = f"UPDATE {table_name}"
        request_2 = f"SET Nb = {new_nb}, Score = {new_score}"
        request_3 = f"WHERE english = {english};"
        sql_request = " ".join([request_1, request_2, request_3])
        # Execute request
        cred = get_database_cred()
        connection, cursor = get_db_cursor(cred)
        cursor.execute(sql_request)
        connection.close()
        return True

    def delete(self, test_type, row):
        """Delete a word from table."""
        # Create request string
        table_name, english, _ = get_words_from_test_type(test_type, row)
        request_1 = f"DELETE FROM {table_name}"
        request_2 = f"WHERE english = {english}"
        sql_request = " ".join([request_1, request_2])
        # Execute request
        cred = get_database_cred()
        connection, cursor = get_db_cursor(cred)
        cursor.execute(sql_request)
        connection.close()
        return True

    def transfer(self, test_type, row):
        """Transfer a word from a table to another."""
        pass
