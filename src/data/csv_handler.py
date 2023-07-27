"""
    Main purpose: provides with methods for CRUD operations with csv.
"""
import pandas as pd


# Table-level operations
def set_paths(os_sep: str, test_type: str):
    """List paths to data csv."""
    paths = {}
    paths['voc'] = os_sep.join(
        [r'.', 'data', test_type + '.csv']
    )
    paths['perf'] = os_sep.join(
        [r'.', 'logs', test_type + '_perf.csv']
    )
    paths['word_cnt'] = os_sep.join(
        [r'.', 'logs', test_type + '_words_count.csv']
    )
    if test_type == 'version':
        paths['output'] = os_sep.join(['.', 'data', 'theme.csv'])
    elif test_type == 'theme':
        paths['output'] = os_sep.join(['.', 'data', 'archives.csv'])
    else:
        print("# ERROR: Wrong test_type argument:", test_type)
        raise SystemExit
    return paths


def get_tables(os_sep: str, test_type: str):
    """Load the different tables necessary to the app."""
    paths = set_paths(os_sep, test_type)
    tables = {}
    tables['voc'] = pd.read_csv(paths['voc'], sep=';', encoding='utf-8')
    tables['perf'] = pd.read_csv(paths['perf'], sep=';', encoding='utf-8')
    tables['word_cnt'] = pd.read_csv(paths['word_cnt'], sep=';', encoding='utf-8')
    tables['output'] = pd.read_csv(paths['output'], sep=';', encoding='utf-8')
    return paths, tables


def save_table(test_type: str, os_sep: str, table_name: str, table: pd.DataFrame):
    """Save given table."""
    paths = set_paths(os_sep, test_type)
    table.to_csv(
        paths[table_name],
        index=False,
        sep=';',
        encoding='utf-8'
    )


# Row-level operations
def create(word, table):
    """Add a word to the table."""
    pass


def read(word, table):
    """Read the given word."""
    pass


def update(word, table):
    """Update statistics on the given word."""
    pass


def delete(word, table):
    """Delete the given word in the given table."""
    pass


def copy(word, table):
    """Copy a word from its original table to the output table (theme or archive)."""
    pass


