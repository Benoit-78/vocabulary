# -*- coding: utf-8 -*-
"""
Author: B.Delorme
Mail: delormebenoit211@gmail.com
Creation date: 2nd March 2023
Main purpose
"""

import pandas as pd

EXTENSION = '.csv'


def get_os_kind():
    """
    Get operating system kind: Windows or UNIX-based.
    """
    os_kind=None
    return os_kind


def get_os_sep(os_kind):
    """
    Get separator specific to operating system: / or \
    """
    if os_kind == 'windows':
        os_sep = '\\'
    elif os_kind == 'linux':
        os_sep = '/'
    else:
        raise Exception
    return os_sep


def check_test_kind(argv):
    """
    Check the kind of check, version or theme.
    """
    if argv not in ['version', 'theme']:
        raise Exception
    else:
        test_kind = argv
    return test_kind


def load_data(os_sep, test_kind):
    """
    Load different dataframes necessary for the app functionning properly.
    """
    voc_path = os_sep.join([r'.', 'data',
                         test_kind + '_voc' + EXTENSION])
    perf_path = os_sep.join([r'.', 'log',
                          test_kind + '_perf' + EXTENSION])
    word_cnt_path = os_sep.join([r'.', 'log',
                              test_kind + '_word_count' + EXTENSION])
    test_cnt_path = os_sep.join([r'.', 'conf',
                              test_kind + '_test_count' + EXTENSION])
    #
    voc_df = pd.read_csv(voc_path,
                         sep=';', encoding='latin1')
    perf_df = pd.read_csv(perf_path,
                          sep=';', encoding='latin1')
    word_cnt_df = pd.read_csv(word_cnt_path,
                              sep=';', encoding='latin1')
    test_cnt = pd.read_csv(test_cnt_path)
    #
    data = [voc_df, word_cnt_df, perf_df, test_cnt]
    return data


def get_random_step(voc_df):
    """
    Get random step, the jump from one word to another.
    """
    step = None
    return step


def get_row(copy_df, index):
    """
    Get the row of the word to be asked.
    The word must not have been asked already.
    """
    row = None
    return row

def get_next_index(current_index, copy_df):
    """
    Get the index of the wordd to be asked.
    The word must not have been asked already.
    """
    index = None
    return index
