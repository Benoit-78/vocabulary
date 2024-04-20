import pandas as pd

from loguru import logger


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
