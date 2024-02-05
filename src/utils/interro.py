"""
    Creation date:
        4th February 2024
    Main purpose:
        Gather some utils functions.
"""

import os
import sys

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src import interro, views
from src.data import data_handler


def load_test(user_name, db_name, test_type, test_length, password):
    """Load the interroooo!"""
    db_handler = data_handler.DbManipulator(
        host='localhost',
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
    )
    db_handler.check_test_type(test_type)
    loader_ = interro.Loader(0, db_handler)
    loader_.load_tables(password)
    guesser = views.FastapiGuesser()
    logger.debug(f"Table names: {loader_.tables.keys()}")
    test_ = interro.Test(
        loader_.tables[loader_.test_type + '_voc'],
        test_length,
        guesser,
        loader_.tables[loader_.test_type + '_perf'],
        loader_.tables[loader_.test_type + '_words_count']
    )
    logger.debug(f"Test created: {test_}")
    test_.set_interro_df()
    return loader_, test_
