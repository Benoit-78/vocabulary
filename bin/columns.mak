# Define variables
SQL_FILE = data/vocabulary.sql
JSON_FILE = conf/cred.json

# Define targets and sub-targets
# When you run 'make sync', it will execute both sub-targets.
sync: sql_to_json json_to_sql

sql_to_json:
    # Add the command to extract column names from SQL and update JSON
    python scripts/sql_to_json.py $(SQL_FILE) $(JSON_FILE)

json_to_sql:
    # Add the command to extract column names from JSON and update SQL
    python scripts/json_to_sql.py $(JSON_FILE) $(SQL_FILE)
