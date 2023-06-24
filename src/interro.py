# -*- coding: utf-8 -*-
"""
    Author: B.Delorme
    Mail: delormebenoit211@gmail.com
    Creation date: 2nd March 2023
    Main purpose: main script of vocabulary application.
"""

import platform
import random
from tkinter import messagebox
import argparse
from datetime import date
from abc import ABC, abstractmethod
import sys
import pandas as pd

EXT = '.csv'


def parse_arguments(args):
    """Parse command line argument"""
    another_parser = argparse.ArgumentParser()
    another_parser.add_argument("-t", "--type", type=str)
    another_parser.add_argument("-w", "--words", type=int)
    another_parser.add_argument("-r", "--rattraps", type=int)
    if args == []:
        args = ['-t', 'version', '-w', '10', '-r', '2']
    args = another_parser.parse_args(args)
    return args


def check_args(args):
    """Check the kind of interro, version or theme"""
    if not args.type or not args.words or not args.rattraps :
        print("# ERROR   | Please give a -t <test type>, -w <number of words> and -r <number of rattraps>")
        raise SystemExit
    if args.type == '':
        print("# ERROR   | Please give a test type: either version or theme")
        raise SystemExit
    if args.type not in ['version', 'theme']:
        print("# ERROR   | Test type must be either version or theme")
        raise SystemExit
    if args.rattraps < 1:
        print("# ERROR   | Number of rattraps must be greater than 0.")
        raise SystemExit
    if args.words < 1:
        print("# ERROR   | Number of words must be greater than 0.")
        raise SystemExit
    return args



class Loader():
    """Data loader"""
    def __init__(self, type, rattraps):
        """Must be done in the same session than the interroooo is launched"""
        self.test_type = type
        self.number_of_rattraps = rattraps
        self.os_type = None
        self.os_sep = None
        self.paths = {}
        self.data = {}

    def get_os_type(self):
        """Get operating system kind: Windows or Linux"""
        operating_system = platform.platform()
        operating_system = operating_system.split('-')[0]
        if operating_system.lower() not in ['windows', 'linux', 'mac', 'android']:
            print("# ERROR operating system cannot be identified")
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
            print("# ERROR wrong input for operating system")
            raise NameError

    def set_data_paths(self):
        """List paths to differente dataframes"""
        self.set_os_separator()
        self.paths['voc'] = self.os_sep.join([r'.', 'data', self.test_type + '_voc' + EXT])
        self.paths['perf'] = self.os_sep.join([r'.', 'log', self.test_type + '_perf' + EXT])
        self.paths['word_cnt'] = self.os_sep.join([r'.', 'log', self.test_type + '_words_count' + EXT])

    def get_data(self):
        """Load different dataframes necessary to the app"""
        self.set_data_paths()
        self.data['voc'] = pd.read_csv(self.paths['voc'], sep=';', encoding='utf-8')
        self.data['perf'] = pd.read_csv(self.paths['perf'], sep=';', encoding='utf-8')
        self.data['word_cnt'] = pd.read_csv(self.paths['word_cnt'], sep=';', encoding='utf-8')

    def data_extraction(self):
        """Return the data necessary for the interro to run"""
        self.get_data()
        self.data['voc']['Query'] = [0] * self.data['voc'].shape[0]
        self.data['voc'] = self.data['voc'].sort_values(by='Date', ascending=True)
        self.data['voc']= self.data['voc'].replace(r',', r'.', regex=True)
        self.data['voc']['Taux'] = self.data['voc']['Taux'].astype(float)



class Interro(ABC):
    """Model (in the MVC pattern). Should be launched by the user"""
    def __init__(self, words_df, args=None, perf_df=None, words_cnt_df=None):
        self.words_df = words_df
        if args:
            self.total = args.words
        else:
            self.total = None
        self.perf_df = perf_df
        self.word_cnt_df = words_cnt_df
        self.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
        self.index = 1
        self.perf = []

    @abstractmethod
    def run(self):
        pass

    def get_row(self):
        """Get the row of the word to be asked"""
        mot_etranger = self.words_df[self.words_df.columns[0]].loc[self.index]
        mot_natal = self.words_df[self.words_df.columns[1]].loc[self.index]
        row = [mot_etranger, mot_natal]
        return row

    def guess_word(self, row, i):
        """Given an index, ask a word to the user, and return a boolean."""
        title = f"Word {i}/{self.total}"
        question = ViewQuestion()
        question.ask_word(title, row)
        word_guessed = question.check_word(title, row)
        return word_guessed

    def update_faults_df(self, word_guessed, row):
        """Save the faulty answers for the second test."""
        if word_guessed is False:
            self.faults_df.loc[self.faults_df.shape[0]] = [row[0], row[1]]

    def compute_success_rate(self):
        """Compute success rate."""
        faults_total = self.faults_df.shape[0]
        if self.total != 0:
            success_rate = int(100 * (1 - (faults_total / self.total)))
        elif self.total == 0:
            success_rate = 100
        self.perf = success_rate



class Test(Interro):
    """First round"""
    def run(self):
        """Launch the vocabulary interoooooo !!!!"""
        self.create_random_step()
        self.index = self.step
        for i in range(1, self.total + 1):
            self.index = self.get_next_index()
            row = self.get_row()
            word_guessed = self.guess_word(row, i)
            self.update_voc_df(word_guessed)
            self.update_faults_df(word_guessed, row)

    def create_random_step(self):
        """Get random step, the jump from one word to another"""
        self.step = random.randint(1, self.words_df.shape[0])

    def get_next_index(self):
        """Get the next index. The word must not have been already asked."""
        next_index = (self.index + self.step) % self.words_df.shape[0]
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
        self.words_df.loc[self.index, 'Nb'] += 1
        # Update Score
        if word_guessed:
            self.words_df.loc[self.index, 'Score'] += 1
        else:
            self.words_df.loc[self.index, 'Score'] -= 1
        # Update Taux
        nombre = self.words_df['Nb'].loc[self.index]
        score = self.words_df['Score'].loc[self.index]
        taux = round(score / nombre, 2)
        self.words_df.loc[self.index, 'Taux'] = taux
        # Update Query
        self.words_df.loc[self.index, 'Query'] += 1

    def remove_known_words(self):
        """Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will."""
        steep = -1.25
        ordinate = 112.5
        self.words_df['image'] = ordinate + steep * self.words_df['Nb']
        self.words_df = self.words_df[self.words_df['Taux'] < self.words_df['image']]
        return self.words_df

    def save_words_count(self, count_log_path):
        """Save the length of vocabulary list in a file"""
        word_counts = self.words_df.shape[0]
        count_before = self.word_cnt_df.shape[0]
        today_date = date.today()
        self.word_cnt_df.loc[count_before] = [today_date, word_counts]
        count_after = self.word_cnt_df.shape[0]
        if count_after == count_before + 1:
            self.word_cnt_df.to_csv(count_log_path, index=False, sep=';')
        else:
            print("# ERROR   | Words count not saved.")

    def save_performances(self, perf_paths):
        """Save performances for further analysis."""
        self.perf_df.loc[self.perf_df.shape[0]] = self.perf
        self.perf_df.to_csv(perf_paths, index=False, sep=';', encoding='utf-8')



class Rattrap(Interro):
    """Rattrapage !!!"""
    def run(self):
        """Launch the second test"""
        self.total = self.words_df.shape[0]
        for j in range(0, self.total):
            row = self.get_row()
            word_guessed = self.guess_word(row, j+1)
            self.update_faults_df(word_guessed, row)



class ViewQuestion():
    """View in MVC pattern."""
    def ask_word(self, title, row):
        mot_etranger = row[0]
        text_1 = f"Quelle traduction donnez-vous pour : {mot_etranger}?"
        user_answer = messagebox.showinfo(title=title, message=text_1)
        if user_answer is False:
            print("# ERROR   | Interruption by user")
            raise SystemExit

    def check_word(self, title, row):
        """Ask the user to decide if the answer was correct or not."""
        mot_natal = row[1]
        text_2 = f"Voici la traduction correcte : \'{mot_natal}\'. \nAviez-vous la bonne réponse ?"
        word_guessed = messagebox.askyesnocancel(title=title, message=text_2)
        if word_guessed is None:
            print("# ERROR interruption by user")
            raise SystemExit
        return word_guessed

    def plot_nuage_de_point(self):
        """Scatterplot of words, abscisses number of guesses, ordinates rate of
        success """
        # sns.scatterplot(words_df[['Nb', 'Taux']])
        return None

    def save_nuage_de_points(self):
        """Save the graph, so that analysis can be made on series of graphs"""



if __name__ == '__main__':
    # Get user inputs
    args = parse_arguments(sys.argv[1:])
    args = check_args(args)
    # Load data
    chargeur = Loader(args.type, args.rattraps)
    chargeur.data_extraction()
    words_df = chargeur.data['voc']
    perf_df = chargeur.data['perf']
    word_cnt_df = chargeur.data['word_cnt']
    # WeuuuuAaaaaInterrooo !!!
    test_1 = Test(words_df, args, perf_df, word_cnt_df)
    test_1.run()
    test_1.compute_success_rate()
    faults_df = test_1.faults_df
    # C'est les rattraaaaaaapssss !!!!
    if test_1.total == -1:
        while faults_df.shape[0] > 0:
            rattrap = Rattrap(faults_df)
            rattrap.run()
            faults_df = rattrap.faults_df
            rattrap.compute_success_rate()
    else:
        for i in range(test_1.total):
            rattrap = Rattrap(faults_df)
            rattrap.run()
            faults_df = rattrap.faults_df
            rattrap.compute_success_rate()
    # Save results
    test_1.save_performances(chargeur.paths['perf'])
    test_1.remove_known_words()
    test_1.save_words_count(chargeur.paths['word_cnt'])
    #
    test_1.words_df = test_1.words_df.drop('Query', axis=1)
    test_1.words_df.to_csv(chargeur.os_sep.join([r'.', 'data', chargeur.test_type + '_voc' + EXT]),
                           index=False, sep=';')
