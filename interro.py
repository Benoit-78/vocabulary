# -*- coding: utf-8 -*-
"""
Author: B.Delorme
Mail: delormebenoit211@gmail.com
Creation date: 2nd March 2023
Main purpose: main script of vocabulary application
"""

import platform
import random
import sys
from tkinter import messagebox
import pandas as pd
import seaborn as sns


EXTENSION = '.csv'


def check_test_type(argv):
    """Check the kind of check, version or theme"""
    if len(argv) == 1:
        print('# ERROR please give a test type: either version or theme')
        raise ValueError
    if not isinstance(argv[1], str):
        print('# ERROR please give a string as a test type')
        raise TypeError
    if len(argv[1]) == 0:
        print('# ERROR please give a test type: either version or theme')
        raise ValueError
    if argv[1] not in ['version', 'theme']:
        print('# ERROR test kind must be \'version\' or \'theme\'')
        raise NameError
    return argv[1]


def get_os_type():
    """Get operating system kind: Windows or Linux"""
    operating_system = platform.platform()
    operating_system = operating_system.split('-')[0]
    # if operating_system.lower() not in ['windows', 'linux', 'mac', 'android']:
    #     print('# ERROR operating system cannot be identified')
    #     raise OSError
    return operating_system


def get_os_separator(os_type):
    """Get separator specific to operating system: / or \ """
    if not isinstance(os_type, str):
        raise TypeError
    if os_type == 'Windows':
        os_sep = '\\'
    elif os_type in ['Linux', 'Mac', 'Android']:
        os_sep = '/'
    else:
        print('# ERROR wrong input for operating system')
        raise NameError
    return os_sep


def get_data_paths(os_sep, test_kind):
    """List paths to differente dataframes"""
    paths = {}
    paths['voc'] = os_sep.join([r'.', 'data',
                                test_kind + '_voc' + EXTENSION])
    paths['perf'] = os_sep.join([r'.', 'log',
                                 test_kind + '_perf' + EXTENSION])
    paths['word_cnt'] = os_sep.join([r'.', 'log',
                                     test_kind + '_word_count' + EXTENSION])
    paths['test_cnt'] = os_sep.join([r'.', 'conf',
                                     test_kind + '_test_count' + EXTENSION])
    return paths


def get_data(paths):
    """Load different dataframes necessary to the app"""
    data = {}
    data['voc'] = pd.read_csv(paths['voc'],
                              sep=';', encoding='latin1')
    data['perf'] = pd.read_csv(paths['perf'],
                               sep=';', encoding='latin1')
    data['word_cnt'] = pd.read_csv(paths['word_cnt'],
                                   sep=';', encoding='latin1')
    data['test_cnt'] = pd.read_csv(paths['test_cnt'],
                                   sep=';', encoding='latin1')
    print('# INFO data loaded')
    return data


def data_processing(voc_df):
    voc_df['Query'] = [0] * voc_df.shape[0]
    voc_df = voc_df.sort_values(by='Date', ascending=True)
    voc_df = voc_df.replace(r',', r'.', regex=True)
    voc_df['Taux'] = voc_df['Taux'].astype(float)
    return voc_df


def create_random_step(voc_df):
    """Get random step, the jump from one word to another"""
    step = random.randint(1, voc_df.shape[0])
    return step


def get_next_index(index, step, voc_df):
    """Get the next index. The word must not have been asked already."""
    # 
    if voc_df['Query'].loc[index] == 0:
        index = (index + step) % voc_df.shape[0]
    # 
    elif voc_df['Query'].loc[index] == 1:
        index = (index + step) % voc_df.shape[0] + 1
    return index


def get_row(voc_df, index):
    """Get the row of the word to be asked"""
    foreign = voc_df.columns[0]
    native = voc_df.columns[1]
    row = [voc_df[foreign].loc[index],
           voc_df[native].loc[index],
           voc_df['Taux'].loc[index]]
    return row


def guess_word(voc_df, index, i):
    """Given an index, ask a word to the user, and return a boolean."""
    etrangere, natale, taux = get_row(voc_df, index)
    msgbox_title = 'Word {}/100, n.{}'.format(i, index)
    msgbox_text = '{} \n Get it?'.format(etrangere)
    word_guessed = messagebox.askyesno(title=msgbox_title,
                                       message=msgbox_text)
    return word_guessed


def update_voc_df(voc_df, word_guessed):
    """Update the vocabulary dataframe"""
    # Update Nb
    voc_df['Nb'].loc[index] += 1
    # Update Score
    if word_guessed:
        voc_df['Score'].loc[index] += 1
    else:
        voc_df['Score'].loc[index] -= 1
    # Update Taux
    nombre = voc_df['Nb'].loc[index]
    score = voc_df['Score'].loc[index]
    taux = round(score / nombre, 2)
    voc_df['Taux'].loc[index] = taux
    return voc_df


def plot_nuage_de_point(voc_df):
    """Scatterplot of words, abscisses number of guesses, ordinates rate of
    success """
    sns.scatterplot(voc_df[['Nb', 'Taux']])
    return None


if __name__ == '__main__':
    # Load data
    test_type = check_test_type(sys.argv)
    os_type = get_os_type()
    os_sep = get_os_separator(os_type)
    paths = get_data_paths(os_sep, test_type)
    data = get_data(paths)
    # Prepare interro
    voc_df = data['voc']
    voc_df = data_processing(voc_df)
    print("# DEBUG voc_df['Taux'].dtype:", voc_df['Taux'].dtype)
    print("# DEBUG voc_df.columns:", voc_df.columns)
    step = create_random_step(voc_df)
    index = step
    # WeuuuuAaaaaInterrooo !!!
    for i in range(1, 101):
        index = get_next_index(index, step, voc_df)
        word_guessed = guess_word(voc_df, index, i)
        voc_df = update_voc_df(voc_df, word_guessed)
    voc_df = voc_df.drop('Query', axis=1)
    # plot_nuage_de_point(voc_df)
    voc_df.to_csv('voc_df.csv')
