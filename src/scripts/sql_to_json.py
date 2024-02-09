"""
    Extract column names from vocabulary.sql and report them in cred.json
"""

import json
import os
import sys

from loguru import logger

SQL_FILE = "vocabulary.sql"
JSON_FILE = "cred_copy.json"

# Get the absolute path of the 'app' directory
app_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(app_dir))


from src import utils

OS_SEP = utils.get_os_separator()


def get_columns(table_name, sql_path='data' + OS_SEP + SQL_FILE):
    """Extract column names from the sql instructions file."""
    with open(sql_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pre_result = content.split(f"CREATE TABLE IF NOT EXISTS {table_name} (")[1]
    columns_types = pre_result.split(');')[0]
    columns_types = columns_types.split(',')
    for char in ['\n', '\t', '    ']:
        columns_types = [element.replace(char, '') for element in columns_types]
    columns = [element.split(' ')[0] for element in columns_types]
    return columns


def update_columns(columns, json_path='conf' + OS_SEP + JSON_FILE):
    """Re-write the column names in the json file."""
    with open(json_path, 'r', encoding='utf-8') as file:
        content_as_str = file.read()
        content_as_dict = json.loads(content_as_str)
        content_as_dict['Tables']['version_voc']['Columns'] = columns
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(content_as_dict, file)


if __name__ == '__main__':
    columns = get_columns('version_voc')
    update_columns(columns)
    with open('conf' + OS_SEP + JSON_FILE, 'r', encoding='utf-8') as file:
        new_json = file.read()
    logger.debug(new_json)
