# -*- coding: utf-8 -*-
"""
Author: B.Delorme
Mail: delormebenoit211@gmail.com
Creation date: 2nd March 2023
Main purpose: main script of vocabulary application
"""

import platform
import random
from tkinter import messagebox
import pandas as pd
import seaborn as sns
import argparse
from datetime import date


EXTENSION = '.csv'


def check_test_type(test_type):
    """Check the kind of check, version or theme"""
    if not isinstance(test_type, str):
        print('# ERROR please give a string as a test type')
        raise TypeError
    if len(test_type) == 0:
        print('# ERROR please give a test type: either version or theme')
        raise ValueError
    if test_type not in ['version', 'theme']:
        print('# ERROR test kind must be \'version\' or \'theme\'')
        raise NameError
    return test_type


def get_os_type():
    """Get operating system kind: Windows or Linux"""
    operating_system = platform.platform()
    operating_system = operating_system.split('-')[0]
    if operating_system.lower() not in ['windows', 'linux', 'mac', 'android']:
        print('# ERROR operating system cannot be identified')
        raise OSError
    return operating_system


def get_os_separator(os_type):
    """Get separator specific to operating system: / or \\ """
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
    return data


def data_preprocessing(voc_df):
    voc_df['Query'] = [0] * voc_df.shape[0]
    voc_df = voc_df.sort_values(by='Date', ascending=True)
    voc_df = voc_df.replace(r',', r'.', regex=True)
    voc_df['Taux'] = voc_df['Taux'].astype(float)
    return voc_df


def create_random_step(voc_df):
    """Get random step, the jump from one word to another"""
    step = random.randint(1, voc_df.shape[0])
    return step


def get_next_index(current_index, step, voc_df):
    """Get the next index. The word must not have been asked already."""
    next_index = (current_index + step) % voc_df.shape[0]
    already_asked = (voc_df['Query'].loc[next_index] == 1)
    title_row = (next_index == 0) 
    while already_asked or title_row:
        next_index = (next_index + step) % voc_df.shape[0]
    return next_index


def get_row(voc_df, index):
    """Get the row of the word to be asked"""
    mot_etranger = voc_df[voc_df.columns[0]].loc[index]
    mot_natal = voc_df[voc_df.columns[1]].loc[index]
    row = [mot_etranger, mot_natal]
    return row


def guess_word(row, i, total):
    """Given an index, ask a word to the user, and return a boolean."""
    mot_etranger = row[0]
    msgbox_title = f'Word {i}/{total}'
    msgbox_text = f'{mot_etranger} \nDo you get it?'
    user_answer = messagebox.showinfo(title=msgbox_title,
                                      message=msgbox_text)
    if user_answer is False:
        print("# ERROR interruption by user")
        raise Exception
    mot_natal = row[1]
    msgbox_title = f'Word {i}/{total}'
    msgbox_text = f'Translation is \'{mot_natal}\'. \nWere you right?'
    word_guessed = messagebox.askyesnocancel(title=msgbox_title,
                                             message=msgbox_text)
    if word_guessed is None:
        print("# ERROR interruption by user")
        raise Exception
    return word_guessed


def update_fault_df(fault_df, word_guessed, row):
    """Save the faulty answers for the second test."""
    if word_guessed is False:
        fault_df.loc[fault_df.shape[0]] = [row[0], row[1]]
    return fault_df


def update_voc_df(voc_df, index, word_guessed):
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
    # Update Query
    voc_df['Query'].loc[index] += 1
    return voc_df


def save_performances(data, total, faults_total, double_faults_total, paths):
    """Save performances for further analysis."""
    perf_df = data['perf']
    today_date = date.today()
    if total != 0:
        test_perf = int(100 * (1 - (faults_total / total)))
    elif total ==0:
        test_perf = 100
    if faults_total != 0:
        rattrap_perf = int(100 * (1 - (double_faults_total / faults_total)))
    elif faults_total == 0:
        rattrap_perf = 100
    row = [today_date, test_perf, rattrap_perf]
    perf_df.loc[perf_df.shape[0]] = row
    perf_df.to_csv(paths['perf'], index=False, sep=';')
    return None


def remove_known_words(voc_df):
    """Remove words that have been guessed sufficiently enough.
    This \'sufficiently\' criteria is totally arbitrary, and can be changed only
    under the author's dictatorial will.
    """
    steep = -1.25
    ordinate = 112.5
    voc_df['image'] = ordinate + steep * voc_df['Nb']
    print(voc_df['image'])
    outliers_df = voc_df[100 * voc_df['Taux'] > voc_df['image']]
    print("# DEBUG number of points to be removed:", outliers_df.shape[0])
    voc_df = voc_df[voc_df['Taux'] < voc_df['image']]
    return voc_df


def save_nuage_de_point(voc_df):
    """Scatterplot of words, abscisses number of guesses, ordinates rate of
    success """
    sns.scatterplot(voc_df[['Nb', 'Taux']])
    return None


if __name__ == '__main__':
    # Load data
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str)
    args = parser.parse_args()
    test_type = check_test_type(args.type)
    os_type = get_os_type()
    os_sep = get_os_separator(os_type)
    paths = get_data_paths(os_sep, test_type)
    data = get_data(paths)
    print('# INFO data loaded.')
    # Prepare interro
    voc_df = data_preprocessing(data['voc'])
    step = create_random_step(voc_df)
    index = step
    print('# INFO interro prepared.')
    # WeuuuuAaaaaInterrooo !!!
    faults = list()
    total = 100
    for i in range(1, total + 1):
        index = get_next_index(index, step, voc_df)
        row = get_row(voc_df, index)
        word_guessed = guess_word(row, i, total)
        voc_df = update_voc_df(voc_df, index, word_guessed)
        if not word_guessed:
            faults.append([row[0], row[1]])
    # Eeeeencore une Interrrooooo !!!!
    double_faults = []
    faults_total = len(faults)
    for j in range(0, faults_total):
        row = faults[j]
        word_guessed = guess_word(row, j+1, faults_total)
        if not word_guessed:
            double_faults.append([row[0], row[1]])
    # Eeeet eeeeeencore une Interrroooo !!!!
    double_faults_total = len(double_faults)
    for k in range(0, double_faults_total):
        row = double_faults[k]
        word_guessed = guess_word(row, k+1, double_faults_total)
    print('# INFO interro finished.')
    # Save results
    save_performances(data, total, faults_total, double_faults_total, paths)
    remove_known_words(voc_df)
    save_word_counts()
    save_nuage_de_point(voc_df)
    # plot_nuage_de_point(voc_df)
    voc_df = voc_df.drop('Query', axis=1)
    voc_df.to_csv('voc_df.csv', index=False, sep=';')
