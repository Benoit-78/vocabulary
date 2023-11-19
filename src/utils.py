"""
    Background functions for vocabulary program.
"""

import platform

import pandas as pd
from loguru import logger


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


def complete_columns(df_1: pd.DataFrame, df_2: pd.DataFrame):
    """
    Guarantee that the well_known_words dataframe contains exactly
    the columns of the output dataframe
    """
    missing_columns = set(df_1.columns).difference(set(df_2.columns))
    for column in missing_columns:
        df_2[column] = [0] * df_2.shape[0]
    return df_2
