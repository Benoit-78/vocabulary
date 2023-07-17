from .event import subscribe
import json
from datetime import datetime
import mariadb


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


def create_word(cred, table, english, french):
    """Add a word to the table"""
    connection, cursor = get_db_cursor(cred)
    today = datetime.now()
    requests_header = f"INSERT INTO {table} (english, francais, Date, Nb, Score, Taux)"
    request_content = f"VALUES ({english}, {french}, {today}, 0, 0, 0);"
    sql_request = " ".join([requests_header, request_content])
    cursor.execute(sql_request)
    # for first_name, last_name in cursor:
    #     print(f'First name: {first_name}, Last name: {last_name}')
    connection.close()


def read_word():
    """Read the given word"""
    pass


def update_word(user, word):
    """Update statistics on the given word"""
    pass


def copy_word(user):
    pass


def delete_word(user):
    pass


def setup_database_event_handlers():
    subscribe("add_word", create_word)
    subscribe("ask_word", read_word)
    subscribe("update_word", update_word)
    subscribe("copy_word", copy_word)
    subscribe("delete_word", delete_word)
