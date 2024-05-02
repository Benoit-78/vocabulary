
import os
import sys
from typing import Dict

import pandas as pd
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src.utils.os import get_os_separator



class CsvHandler():
    """
    Provide with all methods necessary to interact with csv files.
    """
    def __init__(self, test_type: str):
        self.test_type = test_type
        self.os_sep = get_os_separator()
        self.paths = {}
        self.tables = {}

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
        """
        Load the different tables necessary to the app.
        """
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
        """
        Return the paths
        """
        self.set_paths()
        return self.paths

    def get_tables(self) -> Dict[str, pd.DataFrame]:
        """
        Load the tables
        """
        self.set_tables()
        return self.tables

    def save_table(self, table_name: str, table: pd.DataFrame):
        """
        Save given table.
        """
        self.set_paths()
        table.to_csv(
            self.paths[table_name],
            index=False,
            sep=';',
            encoding='utf-8'
        )



# def csv_to_sql(csv_path: str, table_name: str):
#     """
#     Read the CSV file into a DataFrame
#     and write the SQL insert statements to a .sql file.
#     """
#     data_df = pd.read_csv(csv_path, sep=';')
#     with open(f'data/{table_name}.sql', 'w', encoding='utf-8') as sql_file:
#         for _, row in data_df.iterrows():
#             values = ", ".join([
#                 f"'{value}'"
#                 if isinstance(value, str)
#                 else str(value)
#                 for value in row
#             ])
#             request_1 = "INSERT INTO `version_voc` (`foreign`, `native`, `creation_date`, `nb`, `score`, `taux`)"
#             request_2 = f"VALUES ({values});\n"
#             insert_statement = request_1 + request_2
#             logger.debug(f"Writing to SQL file: {insert_statement}")
#             sql_file.write(insert_statement)
