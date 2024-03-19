"""
    Main purpose:
        Background functions for vocabulary program.
"""

import pandas as pd


def complete_columns(df_1: pd.DataFrame, df_2: pd.DataFrame):
    """
    Guarantee that the well_known_words dataframe contains exactly
    the columns of the output dataframe
    """
    missing_columns = set(df_1.columns).difference(set(df_2.columns))
    for column in missing_columns:
        df_2[column] = [0] * df_2.shape[0]
    return df_2
