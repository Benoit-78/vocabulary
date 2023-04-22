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



class Chargeur():
    """Controller (in the MVC pattern). Should be used by the user"""
    def __init__(self, args):
        """Must be done in the same session than the interroooo is launched"""
        self.test_type = args.type
        self.os_type = None
        self.os_sep = None
        self.paths = {}
        self.data = {}

    def check_test_type(self):
        """Check the kind of check, version or theme"""
        if not isinstance(self.test_type, str):
            print('# ERROR please give a string as a test type')
            raise TypeError
        if len(self.test_type) == 0:
            print('# ERROR please give a test type: either version or theme')
            raise ValueError
        if self.test_type not in ['version', 'theme']:
            print('# ERROR test kind must be \'version\' or \'theme\'')
            raise NameError

    def set_os_type(self):
        """Get operating system kind: Windows or Linux"""
        operating_system = platform.platform()
        operating_system = operating_system.split('-')[0]
        if operating_system.lower() not in ['windows', 'linux', 'mac', 'android']:
            print('# ERROR operating system cannot be identified')
            raise OSError
        self.os_type = operating_system

    def set_os_separator(self):
        """Get separator specific to operating system: / or \\ """
        if not isinstance(self.os_type, str):
            raise TypeError
        if self.os_type == 'Windows':
            self.os_sep = '\\'
        elif self.os_type in ['Linux', 'Mac', 'Android']:
            self.os_sep = '/'
        else:
            print('# ERROR wrong input for operating system')
            raise NameError

    def set_data_paths(self):
        """List paths to differente dataframes"""
        self.paths['voc'] = self.os_sep.join([r'.', 'data',
                                              self.test_type + '_voc' + EXTENSION])
        self.paths['perf'] = self.os_sep.join([r'.', 'log',
                                               self.test_type + '_perf' + EXTENSION])
        self.paths['word_cnt'] = self.os_sep.join([r'.', 'log',
                                                   self.test_type + '_word_count' + EXTENSION])

    def set_data(self):
        """Load different dataframes necessary to the app"""
        self.data['voc'] = pd.read_csv(self.paths['voc'],
                                       sep=';', encoding='latin1')
        self.data['perf'] = pd.read_csv(self.paths['perf'],
                                        sep=';', encoding='latin1')
        self.data['word_cnt'] = pd.read_csv(self.paths['word_cnt'],
                                            sep=';', encoding='latin1')



class Interro():
    """Model (in the MVC pattern). Should be launched by the user"""
    def __init__(self, data):
        self.data = data
        self.voc_df = self.data['voc']
        self.step = 0

    def data_preprocessing(self):
        self.voc_df['Query'] = [0] * self.voc_df.shape[0]
        self.voc_df = self.voc_df.sort_values(by='Date', ascending=True)
        self.voc_df = self.voc_df.replace(r',', r'.', regex=True)
        self.voc_df['Taux'] = self.voc_df['Taux'].astype(float)

    def create_random_step(self):
        """Get random step, the jump from one word to another"""
        self.step = random.randint(1, self.voc_df.shape[0])

    def guess_word(row, i, total):
        """Given an index, ask a word to the user, and return a boolean."""
        mot_etranger = row[0]
        title = f'Word {i}/{total}'
        text = f'{mot_etranger} \nDo you get it?'
        user_answer = messagebox.showinfo(title=title, message=text)
        if user_answer is False:
            print("# ERROR interruption by user")
            raise Exception
        mot_natal = row[1]
        title = f'Word {i}/{total}'
        text = f'Translation is \'{mot_natal}\'. \nWere you right?'
        word_guessed = messagebox.askyesnocancel(title=title, message=text)
        if word_guessed is None:
            print("# ERROR interruption by user")
            raise Exception
        return word_guessed

    def update_fault_df(fault_df, word_guessed, row):
        """Save the faulty answers for the second test."""
        if word_guessed is False:
            fault_df.loc[fault_df.shape[0]] = [row[0], row[1]]
        return fault_df

    def save_performances(self, total, faults_total, double_faults_total, paths):
        """Save performances for further analysis."""
        self.perf_df = self.data['perf']
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

    def save_words_count(voc_df, test_type, os_sep):
        """Save the length of vocabulary list in a file"""
        word_counts = voc_df.shape[0]
        # log_file_name = test_type + '_words_count.csv'
        # log_file_path = os_sep.join(['.', 'log', log_file_name])
        count_df = pd.read_csv(log_file_path, sep=';', encoding='latin1')
        count_before = count_df.shape[0]
        today_date = date.today()
        count_df.loc[count_before] = [today_date, word_counts]
        count_after = count_df.shape[0]
        count_df.to_csv(log_file_path, index=False, sep=';')
        if count_after == count_before + 1:
            message = "# INFO    | Words count saved successfully."
        else:
            message = "# ERROR   | Words count not saved."
        print(message)






class Test(Interro):
    """First round"""
    def get_next_index(current_index, step, voc_df):
        """Get the next index. The word must not have been asked already."""
        next_index = (current_index + step) % voc_df.shape[0]
        already_asked = (voc_df['Query'].loc[next_index] == 1)
        title_row = (next_index == 0)
        while already_asked or title_row:
            next_index = (next_index + step) % voc_df.shape[0]
            already_asked = (voc_df['Query'].loc[next_index] == 1)
            title_row = (next_index == 0)
        return next_index
    
    def get_row(voc_df, index):
        """Get the row of the word to be asked"""
        mot_etranger = voc_df[voc_df.columns[0]].loc[index]
        mot_natal = voc_df[voc_df.columns[1]].loc[index]
        row = [mot_etranger, mot_natal]
        return row
    
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



class Rattrap(Interro):
    """Second round"""



class RattrapRattrap(Interro):
    """Third round"""



class Graphiques():
    """Viewer (in the MVC pattern). Should be used by the user."""
    def save_nuage_de_point(voc_df):
        """Scatterplot of words, abscisses number of guesses, ordinates rate of
        success """
        sns.scatterplot(voc_df[['Nb', 'Taux']])
        return None



def save_results(voc_df):
    """Update the vocabulary list with the """
    


if __name__ == '__main__':
    # Load data
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str)
    args = parser.parse_args()
    loader = Chargeur(args)
    loader.check_test_type()
    loader.set_os_type()
    loader.set_os_separator()
    loader.set_data_paths()
    loader.set_data()
    print('# INFO data loaded.')
    # Prepare interro
    interro = Interro(loader.data)
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
# =============================================================================
#     # Eeeeencore une Interrrooooo !!!!
# =============================================================================
    double_faults = []
    faults_total = len(faults)
    for j in range(0, faults_total):
        row = faults[j]
        word_guessed = guess_word(row, j+1, faults_total)
        if not word_guessed:
            double_faults.append([row[0], row[1]])
# =============================================================================
#     # Eeeet eeeeeencore une Interrroooo !!!!
# =============================================================================
    double_faults_total = len(double_faults)
    for k in range(0, double_faults_total):
        row = double_faults[k]
        word_guessed = guess_word(row, k+1, double_faults_total)
    print('# INFO interro finished.')
    # Save results
    save_performances(data, total, faults_total, double_faults_total, paths)
    remove_known_words(voc_df)
    save_words_count(voc_df, test_type)
    save_nuage_de_point(voc_df)
    # plot_nuage_de_point(voc_df)
    voc_df = voc_df.drop('Query', axis=1)
    voc_df.to_csv('voc_df.csv', index=False, sep=';')
