"""
    Main purpose: provides with methods for CRUD operations with database.
"""

import json
from datetime import datetime
from typing import List
import mysql.connector as mariadb
import pandas as pd


# Table-level operations
def get_tables(test_type: str):
    """Load the different tables necessary to the app."""
    tables_names = get_tables_names(test_type)
    cred = get_database_cred()
    connection, cursor = get_db_cursor(cred)
    tables = []
    for table_name in tables_names:
        sql_request = "SELECT * FROM {table_name}"
        tables[table_name] = cursor.execute(sql_request)
    connection.close()
    return tables


def save_table(table: pd.DataFrame):
    """Save given table."""
    pass


# Row operations
def create(test_type, row):
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


def read(test_type, row):
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


def update(test_type, row, new_nb, new_score):
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


def delete(test_type, row):
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


def copy(test_type, row):
    """Copy a word from a table to another."""
    pass



# Common operations
def get_database_cred():
    """Get credentials necessary for connection with vocabulary database."""
    credentials = None
    with open(".\\conf\\cred.json", 'rb') as cred_file:
        credentials = json.load(cred_file)
    return credentials


def get_db_cursor(cred):
    """Connect to vocabulary database if credentials are correct."""
    if cred:
        connection = mariadb.connect(
            user=cred.get('usr'),
            password=cred.get('pwd'),
            database=cred.get('database'),
            host=cred.get('host')
        )
        cursor = connection.cursor()
    return connection, cursor


def get_tables_names(test_type: str) -> List[str]:
    """Get version or theme table according to the test type."""
    test_types = ['version', 'theme']
    if test_type in ['version', 'theme']:
        voc_table = test_type + '_voc'
        perf_table = test_type + '_perf'
        word_cnt_table = test_type + '_words_count'
        test_types.pop(test_type)
        output_table = test_types[0] + '_voc'
    else:
        print("ERROR: Wrong test_type argument:", test_type)
        raise ValueError
    return [voc_table, perf_table, word_cnt_table, output_table]


def get_words_from_test_type(test_type: str, row: list):
    """Common method used by all 4 CRUD operations"""
    [words_table_name, _, _, _] = get_words_table_from_test_type(test_type)
    english = row[row.columns[0]]
    native = row[row.columns[1]]
    return [words_table_name, english, native]
