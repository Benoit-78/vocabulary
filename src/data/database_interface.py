"""
    Main purpose:
        Sort of an Object-Relational Mapping tool.
        Focuses on Data Control, Data Definition & Data Manipulation.
"""

import json
import os
import re
import socket
from abc import ABC
from datetime import datetime
from typing import Dict, List

import mysql.connector as mariadb
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine

load_dotenv()

HOSTS = {
    "localhost": "localhost",
    "%": "%",
    "web_local": "0.0.0.0",
    "container": "db",
    "fedora": "localhost",
    "ip-172-32-0-78": "localhost"
}



class DbInterface(ABC):
    """
    Abstract class that provides with a method to connect to a database.
    All methods invoked by the user should provide with a host name.
    """
    def __init__(self):
        self.host = HOSTS[socket.gethostname()]
        self.check_host()

    def check_host(self):
        """
        Check if the host is in the list of expected hosts.
        """
        hosts = HOSTS.keys()
        if self.host not in hosts:
            logger.warning(f"host: {self.host}")
            logger.error(f"host should be in {hosts}")
            raise ValueError

    def get_db_cursor(self):
        """
        Connect to vocabulary database if credentials are correct.
        """
        user_name = os.getenv('VOC_DB_ROOT_USR')
        password = os.getenv('VOC_DB_ROOT_PWD')
        db_name = 'mysql'
        connection_config = {
            'user': user_name,
            'password': password,
            'database': db_name,
            'port': os.getenv('VOC_DB_PORT')
        }
        connection_config['host'] = HOSTS[self.host]
        connection = mariadb.connect(**connection_config)
        cursor = connection.cursor()
        return connection, cursor



class DbController(DbInterface):
    """
    Manage access.
    """
    def __init__(self):
        super().__init__()
        self.sql_queries = self.load_sql_queries()

    @staticmethod
    def load_sql_queries() -> dict:
        """
        Load the SQL queries so that they stay in memory,
        and do not have to be read from disk.
        """
        queries = [
            'create_user',
            'grant_select',
            'grant_all',
            'get_users_mysql',
            'add_user',
            'get_users',
            'revoke_all'
        ]
        sql_queries = {}
        for query in queries:
            file_path = query.join(["data/queries/controller/", '.sql'])
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_queries[query] = file.read().strip()
        return sql_queries

    def create_user_in_mysql(self, user_name: str, user_password: str):
        """
        Create a user in the mysql.user table.
        """
        connection, cursor = self.get_db_cursor()
        result = None
        sql_query = self.sql_queries['create_user'].format(
            user_name=user_name,
            host=self.host,
            user_password=user_password
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def grant_privileges_on_common_database(self, user_name: str):
        """
        Grant the new user access to the common database.
        """
        connection, cursor = self.get_db_cursor()
        result = None
        sql_query = self.sql_queries['grant_select'].format(
            user_name=user_name,
            host=self.host
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            logger.success(f"User '{user_name}' created on {self.host}.")
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def grant_privileges(self, user_name: str, db_name: str):
        """
        Grant privileges to the user on the given database.
        """
        sql_db_name = f"{user_name}_{db_name}"
        connection, cursor = self.get_db_cursor()
        result = None
        sql_query = self.sql_queries['grant_all'].format(
            sql_db_name=sql_db_name,
            user_name=user_name,
            host=self.host
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            logger.success(
                f"User '{user_name}' granted access to '{user_name}_{db_name}'."
            )
            result = True
        except Exception as err:
            if err.errno == -1:
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
        sql_query = self.sql_queries['get_users_mysql']
        try:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            users_df = pd.DataFrame(result, columns=columns)
            users_df = users_df[users_df['Host'] == self.host]
            users_list = users_df['User'].tolist()
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
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
        sql_query = self.sql_queries['add_user'].format(
            user_name=user_name,
            hash_password=hash_password,
            user_email=user_email
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            logger.success(f"User '{user_name}' added to users table.")
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def get_users_list(self) -> List[Dict]:
        """
        Get list of users registered in users table.
        """
        connection, cursor = self.get_db_cursor()
        users_list = []
        sql_query = self.sql_queries['get_users']
        try:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            users_df = pd.DataFrame(result, columns=columns)
            users_str = users_df.to_json(orient='records')
            users_list = json.loads(users_str)
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return users_list

    def revoke_privileges(self, user_name: str, db_name: str):
        """
        Remove privileges from the user on the given database.
        """
        connection, cursor = self.get_db_cursor()
        result = None
        sql_query = self.sql_queries['revoke_all'].format(
            db_name=db_name,
            user_name=user_name,
            host=self.host
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            logger.success(
                f"User '{user_name}' removed from '{user_name}_{db_name}'."
            )
            result = True
        except Exception as err:
            if err.errno == -1:
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
        self.sql_queries = self.load_sql_queries()

    @staticmethod
    def load_sql_queries():
        """
        Load the SQL queries so that they stay in memory,
        and do not have to be read from disk.
        """
        queries = [
            'show_db',
            'use_db',
            'create_db',
            'create_version_voc',
            'create_version_perf',
            'create_version_count',
            'create_theme_voc',
            'create_theme_perf',
            'create_theme_count',
            'create_archives',
            'show_tables',
            'show_columns',
            'drop_db'
        ]
        sql_queries = {}
        for query in queries:
            file_path = query.join(["data/queries/definer/", '.sql'])
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_queries[query] = file.read().strip()
        return sql_queries

    def validate_db_name(self, db_name):
        """
        Regular expression to match a valid database name (alphanumeric and underscores)
        """
        result = re.match(
            pattern=r'^[A-Za-z0-9_]+$',
            string=db_name
        )
        return bool(result)

    def create_database(self, db_name):
        """
        Create a database with the given database name
        """
        sql_db_name = f"{self.user_name}_{db_name}"
        if not self.validate_db_name(sql_db_name):
            logger.error(f"Invalid database name: {sql_db_name}")
            return False
        connection, cursor = self.get_db_cursor()
        result = None
        sql_query = sql_db_name.join([
            self.sql_queries['create_db'] + ' ',
            ";"
        ])
        try:
            cursor.execute(sql_query)
            connection.commit()
            result = True
        except Exception as err:
            if err.errno == -1:
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
        sql_query = self.user_name.join([
            self.sql_queries['show_db'] + " '",
            "_%';"
        ])
        try:
            cursor.execute(sql_query)
            databases = [db[0] for db in cursor.fetchall()]
            result = databases
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def create_seven_tables(self, db_name):
        """
        Create the seven tables necessary to the app.
        """
        sql_db_name = f"{self.user_name}_{db_name}"
        if not self.validate_db_name(sql_db_name):
            logger.error(f"Invalid database name: {sql_db_name}")
            return False
        connection, cursor = self.get_db_cursor()
        sql_query = sql_db_name.join([self.sql_queries['use_db'] + ' ', ";"])
        create_tables = [
            'create_version_voc',
            'create_version_perf',
            'create_version_count',
            'create_theme_voc',
            'create_theme_perf',
            'create_theme_count',
            'create_archives'
        ]
        create_queries = [
            self.sql_queries[create_table]
            for create_table in create_tables]
        try:
            cursor.execute(sql_query)
            for sql_query in create_queries:
                cursor.execute(sql_query)
            connection.commit()
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
            else:
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
        sql_query = db_name.join([self.sql_queries['use_db'] + ' ', ";"])
        try:
            cursor.execute(sql_query)
            cursor.execute(self.sql_queries['show_tables'])
            tables = list(cursor.fetchall())
            tables = self.rectify_this_strange_result(columns=tables)
            cols_dict = {}
            for table_name in tables:
                sql_query = table_name.join([
                    self.sql_queries['show_columns'] + ' ',
                    ';'
                ])
                cursor.execute(sql_query)
                columns = list(cursor.fetchall())
                columns = self.rectify_this_strange_result(columns=columns)
                cols_dict[table_name] = columns
            result = cols_dict
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def rectify_this_strange_result(self, columns):
        """
        Correct the result of following requests:
        - 'SHOW TABLES'
        - 'SHOW COLUMNS FROM table_name'
        """
        if isinstance(columns[0], tuple):
            result = [col[0] for col in columns]
        elif isinstance(columns[0], str):
            result = columns
        else:
            logger.error(f"Strange result: {columns}")
            logger.error(f"Type of first element: {type(columns[0])}")
            raise ValueError
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
        sql_query = db_name.join([self.sql_queries['drop_db'] + ' ', ";"])
        try:
            cursor.execute(sql_query)
            connection.commit()
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result



class DbManipulator(DbInterface):
    """
    Modifying the data
    """
    def __init__(self, user_name, db_name, test_type):
        super().__init__()
        self.user_name = user_name
        if self.user_name not in db_name:
            self.db_name = f"{user_name}_{db_name}"
        else:
            self.db_name = db_name
        self.db_definer = DbDefiner(user_name=self.user_name)
        self.db_querier = DbQuerier(
            user_name=self.user_name,
            db_name=db_name,
            test_type=test_type
        )
        self.test_type = check_test_type(test_type=test_type)
        self.sql_queries = self.load_sql_queries()

    @staticmethod
    def load_sql_queries():
        """
        Load the SQL queries so that they stay in memory,
        and do not have to be read from disk.
        """
        queries = [
            'insert_word',
            'update_word',
            'delete_word'
        ]
        sql_queries = {}
        for query in queries:
            file_path = query.join(["data/queries/manipulator/", '.sql'])
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_queries[query] = file.read().strip()
        return sql_queries

    def insert_word(self, row: list):
        """
        Add a word to the table.
        """
        connection, cursor = self.get_db_cursor()
        today_str = str(datetime.today().date())
        words_table_name, _, _, _ = self.db_definer.get_tables_names(
            test_type=self.test_type
        )
        foreign_word = row[0]
        if self.db_querier.read_word(foreign_word) is not None:
            result = 'Word already exists'
            logger.error(result)
            return result
        native_word = row[1]
        sql_query = self.sql_queries['insert_word'].format(
            db_name=self.db_name,
            table_name=words_table_name,
            foreign=foreign_word,
            native=native_word,
            today_str=today_str
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
            else:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def update_word(self, foreign: str, new_nb, new_score):
        """
        Update statistics on the given word
        """
        connection, cursor = self.get_db_cursor()
        words_table_name, _, _, _ = self.db_definer.get_tables_names(
            test_type=self.test_type
        )
        sql_query = self.sql_queries['update_word'].format(
            db_name=self.db_name,
            table_name=words_table_name,
            new_nb=new_nb,
            new_score=new_score,
            foreign=foreign
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def delete_word(self, foreign_word):
        """
        Delete a word from the words table of the instance database.
        """
        connection, cursor = self.get_db_cursor()
        words_table_name, _, _, _ = self.db_definer.get_tables_names(
            test_type=self.test_type
        )
        sql_query = self.sql_queries['delete_word'].format(
            db_name=self.db_name,
            table_name=words_table_name,
            foreign=foreign_word
        )
        try:
            cursor.execute(sql_query)
            connection.commit()
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result

    def save_table(self, table_name: str, table: pd.DataFrame):
        """
        Save given table.
        """
        connection, cursor = self.get_db_cursor()
        cols = self.db_definer.get_database_cols(db_name=self.db_name)
        if table_name == 'output':
            table_name = self.db_querier.get_output_table()
        table = table[cols[table_name]]
        try:
            engine = create_engine(
                url=''.join([
                    "mysql+pymysql",
                    "://", os.getenv('VOC_DB_ROOT_USR'),
                    ':', os.getenv('VOC_DB_ROOT_PWD'),
                    '@', self.host,
                    '/', self.db_name
                ])
            )
            table.to_sql(
                name=table_name,
                con=engine,
                if_exists='replace',
                method='multi',
                index=False
            )
            result = True
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = False
        finally:
            cursor.close()
            connection.close()
        return result



class DbQuerier(DbInterface):
    """
    Querying the data
    """
    def __init__(
            self,
            user_name: str,
            db_name: str,
            test_type: str
        ):
        super().__init__()
        self.user_name = user_name
        if self.user_name not in db_name:
            self.db_name = f"{user_name}_{db_name}"
        else:
            self.db_name = db_name
        self.db_definer = DbDefiner(user_name=self.user_name)
        self.test_type = check_test_type(test_type=test_type)
        self.sql_queries = self.load_sql_queries()

    @staticmethod
    def load_sql_queries():
        """
        Load the SQL queries so that they stay in memory,
        and do not have to be read from disk.
        """
        queries = [
            'get_tables',
            'read_word'
        ]
        sql_queries = {}
        for query in queries:
            file_path = query.join(["data/queries/querier/", '.sql'])
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_queries[query] = file.read().strip()
        return sql_queries

    def get_tables(self):
        """
        Load the different tables necessary to the app.
        """
        connection, cursor = self.get_db_cursor()
        cursor.execute(f"USE {self.db_name};")
        cols = self.db_definer.get_database_cols(db_name=self.db_name)
        tables_names = list(cols.keys())
        tables = {}
        for table_name in tables_names:
            sql_query = self.sql_queries['get_tables'].format(
                table_name=table_name
            )
            cursor.execute(sql_query)
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

    def read_word(self, foreign_word: str):
        """
        Read the given word
        """
        connection, cursor = self.get_db_cursor()
        words_table_name, _, _, _ = self.db_definer.get_tables_names(
            test_type=self.test_type
        )
        sql_query = self.sql_queries['read_word'].format(
            db_name=self.db_name,
            table_name=words_table_name,
            foreign=foreign_word
        )
        request_result = None
        try:
            request_result = cursor.execute(sql_query)
            request_result = cursor.fetchall()
        except Exception as err:
            if err.errno == -1:
                logger.error(err)
                result = None
        finally:
            cursor.close()
            connection.close()
        if request_result:
            foreign_word, native, score = request_result[0]
            result = (foreign_word, native, score)
        else:
            result = None
        return result



def check_test_type(test_type):
    """
    Check the test type attribute.
    """
    if test_type not in ['version', 'theme']:
        logger.error(
            f"Test type {test_type} incorrect, should be either version or theme."
        )
        raise ValueError
    return test_type
