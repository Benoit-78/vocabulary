"""
    Background functions for vocabulary program.
"""

import platform
from loguru import logger
from typing import List
import pandas as pd


def get_os_type():
    """Get operating system kind: Windows or Linux"""
    os_type = platform.platform()
    os_type = os_type.split('-')[0]
    if os_type.lower() not in ['windows', 'linux', 'mac', 'android']:
        logger.error("Operating system cannot be identified.")
        logger.warning("Operating system was arbitrarily set to 'linux'.")
    return os_type


def get_os_separator():
    """Get separator specific to operating system: / or \\ """
    os_type = get_os_type()
    if os_type == 'Windows':
        os_sep = '\\'
    elif os_type in ['Linux', 'Mac', 'Android']:
        os_sep = '/'
    else:
        print("# ERROR: Wrong input for operating system.")
        raise NameError
    return os_sep


def complete_columns(df_2: pd.DataFrame, df_1: pd.DataFrame):
    """
    Guarantee that the well_known_words dataframe contains exactly
    the columns of the output dataframe
    """
    known_words_cols = df_1.columns
    output_columns = df_2.columns
    missing_columns = set(output_columns).difference(set(known_words_cols))
    for column in missing_columns:
        df_1[column] = [0] * df_1.shape[0]
    return df_1
