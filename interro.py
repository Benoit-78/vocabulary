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
# import seaborn as sns
import argparse
from datetime import date
import pandas as pd


EXTENSION = '.csv'
TOTAL = 100



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

    def get_os_type(self):
        """Get operating system kind: Windows or Linux"""
        operating_system = platform.platform()
        operating_system = operating_system.split('-')[0]
        if operating_system.lower() not in ['windows', 'linux', 'mac', 'android']:
            print('# ERROR operating system cannot be identified')
            raise OSError
        self.os_type = operating_system

    def set_os_separator(self):
        """Get separator specific to operating system: / or \\ """
        self.get_os_type()
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
        self.set_os_separator()
        self.check_test_type()
        self.paths['voc'] = self.os_sep.join([r'.', 'data', self.test_type + '_voc' + EXTENSION])
        self.paths['perf'] = self.os_sep.join([r'.', 'log', self.test_type + '_perf' + EXTENSION])
        self.paths['word_cnt'] = self.os_sep.join([r'.', 'log',
                                                   self.test_type + '_words_count' + EXTENSION])

    def get_data(self):
        """Load different dataframes necessary to the app"""
        self.set_data_paths()
        self.data['voc'] = pd.read_csv(self.paths['voc'], sep=';', encoding='latin1')
        self.data['perf'] = pd.read_csv(self.paths['perf'], sep=';', encoding='latin1')
        self.data['word_cnt'] = pd.read_csv(self.paths['word_cnt'], sep=';', encoding='latin1')

    def data_extraction(self):
        """Return the data necessary for the interro to run"""
        self.get_data()
        self.data['voc']['Query'] = [0] * self.data['voc'].shape[0]
        self.data['voc'] = self.data['voc'].sort_values(by='Date', ascending=True)
        self.data['voc']= self.data['voc'].replace(r',', r'.', regex=True)
        self.data['voc']['Taux'] = self.data['voc']['Taux'].astype(float)



class Interro():
    """Model (in the MVC pattern). Should be launched by the user"""
    def __init__(self, words_df, perf_df=None, word_cnt_df=None):
        self.words_df = words_df
        self.perf_df = perf_df
        self.word_cnt_df = word_cnt_df
        self.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
        self.index = 1

    def get_row(self):
        """Get the row of the word to be asked"""
        mot_etranger = self.words_df[self.words_df.columns[0]].loc[self.index]
        mot_natal = self.words_df[self.words_df.columns[1]].loc[self.index]
        row = [mot_etranger, mot_natal]
        return row

    def guess_word(self, row, i, total):
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

    def save_performances(self, total, rattrap_1_faults):
        """Save performances for further analysis."""
        faults_total = self.faults_df.shape[0]
        today_date = date.today()
        # Test
        if total != 0:
            test_perf = int(100 * (1 - (faults_total / total)))
        elif total == 0:
            test_perf = 100
        # Rattrap n.1
        if faults_total != 0:
            rattrap_perf = int(100 * (1 - (rattrap_1_faults / faults_total)))
        elif faults_total == 0:
            rattrap_perf = 100
        row = [today_date, test_perf, rattrap_perf]
        self.perf_df.loc[self.perf_df.shape[0]] = row
        # self.perf_df.to_csv(self.paths['perf'], index=False, sep=';')



class Test(Interro):
    """First round"""
    def create_random_step(self):
        """Get random step, the jump from one word to another"""
        self.step = random.randint(1, self.words_df.shape[0])

    def run(self, total):
        """Launch the vocabulary interoooooo !!!!"""
        self.create_random_step()
        self.index = self.step
        for i in range(1, total + 1):
            self.index = self.get_next_index(self.index)
            row = self.get_row()
            word_guessed = self.guess_word(row, i, total)
            self.update_voc_df(word_guessed)
            if not word_guessed:
                faults = self.faults_df.shape[0]
                self.faults_df.loc[faults] = [row[0], row[1]]

    def get_next_index(self, current_index):
        """Get the next index. The word must not have been asked already."""
        next_index = (current_index + self.step) % self.words_df.shape[0]
        already_asked = self.words_df['Query'].loc[next_index] == 1
        title_row = next_index == 0
        while already_asked or title_row:
            next_index = (next_index + self.step) % self.words_df.shape[0]
            already_asked = self.words_df['Query'].loc[next_index] == 1
            title_row = next_index == 0
        return next_index

    def update_voc_df(self, word_guessed):
        """Update the vocabulary dataframe"""
        # Update Nb
        self.words_df['Nb'].loc[self.index] += 1
        # Update Score
        if word_guessed:
            self.words_df['Score'].loc[self.index] += 1
        else:
            self.words_df['Score'].loc[self.index] -= 1
        # Update Taux
        nombre = self.words_df['Nb'].loc[self.index]
        score = self.words_df['Score'].loc[self.index]
        taux = round(score / nombre, 2)
        self.words_df['Taux'].loc[self.index] = taux
        # Update Query
        self.words_df['Query'].loc[self.index] += 1

    def update_fault_df(self, word_guessed, row):
        """Save the faulty answers for the second test."""
        if word_guessed is False:
            self.faults_df.loc[self.faults_df.shape[0]] = [row[0], row[1]]

    def remove_known_words(self):
        """Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will."""
        steep = -1.25
        ordinate = 112.5
        self.words_df['image'] = ordinate + steep * self.words_df['Nb']
        outliers_df = self.words_df[100 * self.words_df['Taux'] > self.words_df['image']]
        print("# DEBUG number of points to be removed:", outliers_df.shape[0])
        self.words_df = self.words_df[self.words_df['Taux'] < self.words_df['image']]
        return self.words_df

    def save_words_count(self):
        """Save the length of vocabulary list in a file"""
        word_counts = self.words_df.shape[0]
        count_before = self.word_cnt_df.shape[0]
        today_date = date.today()
        self.word_cnt_df.loc[count_before] = [today_date, word_counts]
        count_after = self.word_cnt_df.shape[0]
        if count_after == count_before + 1:
            # Code ci-dessous à mettre dans Chargeur ?
            # log_file_name = test_type + '_words_count.csv'
            # log_file_path = os_sep.join(['.', 'log', log_file_name])
            # self.word_cnt_df.to_csv(log_file_path, index=False, sep=';')
            message = "# INFO    | Words count saved successfully."
        else:
            message = "# ERROR   | Words count not saved."
        print(message)



class Rattrap(Test):
    """Rattrapage !!!"""
    def run(self):
        """Launch the second test"""
        total = self.words_df.shape[0]
        for j in range(0, total):
            row = self.get_row()
            word_guessed = self.guess_word(row, j+1, total)
            if not word_guessed:
                faults = self.faults_df.shape[0]
                self.faults_df.loc[faults]([row[0], row[1]])



class Graphiques():
    """Viewer (in the MVC pattern). Should be used by the user."""
    def plot_nuage_de_point(self):
        """Scatterplot of words, abscisses number of guesses, ordinates rate of
        success """
        # sns.scatterplot(words_df[['Nb', 'Taux']])
        return None

    def save_nuage_de_points(self):
        """Save the graph, so that analysis can be made on series of graphs"""



if __name__ == '__main__':
    # Get user inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str)
    args = parser.parse_args()
    # Load data
    loader = Chargeur(args)
    loader.data_extraction()
    print('# INFO data loaded.')
    # WeuuuuAaaaaInterrooo !!!
    test = Test(loader.data['voc'], loader.data['perf'], loader.data['word_cnt'])
    test.run(TOTAL)
    # Eeeeencore une Interrrooooo !!!!
    rattrap_1 = Rattrap(test.faults_df)
    rattrap_1.run()
    # Eeeet eeeeeencore une Interrroooo !!!!
    rattrap_2 = Rattrap(rattrap_1.faults_df)
    rattrap_2.run()
    print('# INFO interro finished.')
    # Save results
    test.save_performances(TOTAL, rattrap_1.faults_df.shape[0])
    test.remove_known_words()
    test.save_words_count()
    test.words_df = test.words_df.drop('Query', axis=1)
    test.words_df.to_csv('voc_df.csv', index=False, sep=';')
