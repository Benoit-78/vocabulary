
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



# -------------
#  CSV to SQL
# -------------

# Read the CSV file into a DataFrame
df = pd.read_csv('data/csv/version_voc.csv', sep=';')

logger.debug(f"Table: \n{df.head()}")

# Define the name of the table in the SQL database
table_name = 'version_voc'

# Generate SQL INSERT statements
# sql_inserts = []
# for _, row in df.iterrows():
#     columns = ', '.join(row.index)
#     values = ', '.join(
#         f"'{value}'"
#         if isinstance(value, str)
#         else str(value)
#         for value in row
#     )
#     sql_inserts.append(f"INSERT INTO `{table_name}` ({columns}) VALUES ({values});")

# # Write SQL statements to a .sql file
# with open('data/arabic.sql', 'w') as f:
#     f.write('\n'.join(sql_inserts))

with open('data/english_voc.sql', 'w') as sql_file:
    # Write the SQL insert statement for each row in the DataFrame
    for _, row in df.iterrows():
        values = ", ".join([
            f"'{value}'"
            if isinstance(value, str)
            else str(value)
            for value in row
        ])
        insert_statement = f"INSERT INTO `version_voc` (`latina`, `français`, `creation_date`, `nb`, `score`, `taux`) VALUES ({values});\n"
        sql_file.write(insert_statement)
