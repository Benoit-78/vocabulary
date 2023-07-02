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
from typing import List
import pandas as pd


EXT = '.csv'


def parse_arguments(arg: List[str]) -> argparse.Namespace:
    """Parse command line argument"""
    another_parser = argparse.ArgumentParser()
    another_parser.add_argument("-t", "--type", type=str)
    another_parser.add_argument("-w", "--words", type=int)
    another_parser.add_argument("-r", "--rattraps", type=int)
    if '-t' not in arg:
        arg.append('-t')
        arg.append('version')
    if '-w' not in arg:
        arg.append('-w')
        arg.append('10')
    if '-r' not in arg:
        arg.append('-r')
        arg.append('2')
    args = another_parser.parse_args(arg)
    return args


def get_arguments() -> argparse.Namespace:
    """Check the kind of interro, version or theme"""
    args = parse_arguments(sys.argv[1:])
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
    def __init__(self, arguments_: argparse.Namespace):
        """Must be done in the same session than the interroooo is launched"""
        self.test_type = arguments_.type
        self.rattraps = arguments_.rattraps
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
    """Abstract class for interrooooo!!!! !!! !"""
    def __init__(self,
                 words_df_: pd.DataFrame,
                 args: argparse.Namespace=None,
                 perf_df_: pd.DataFrame=None,
                 words_cnt_df: pd.DataFrame=None):
        self.words_df = words_df_
        if args:
            self.words = args.words
        else:
            self.words = None
        self.perf_df = perf_df_
        self.word_cnt_df = words_cnt_df
        self.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
        self.index = 1
        self.perf = []
        self.steep = -1.25
        self.ordinate = 112.5
        self.output_df = pd.DataFrame()
        self.well_known_words = pd.DataFrame()

    @abstractmethod
    def run(self):
        """Launch the interroooo !!!!"""

    def get_row(self) -> List[str]:
        """Get the row of the word to be asked"""
        mot_etranger = self.words_df[self.words_df.columns[0]].loc[self.index]
        mot_natal = self.words_df[self.words_df.columns[1]].loc[self.index]
        row = [mot_etranger, mot_natal]
        return row

    def guess_word(self, row: List[str], i: int):
        """Given an index, ask a word to the user, and return a boolean."""
        title = f"Word {i}/{self.words}"
        question = ViewQuestion()
        question.ask_word(title, row)
        word_guessed = question.check_word(title, row)
        return word_guessed

    def update_faults_df(self, word_guessed: bool, row: List[str]):
        """Save the faulty answers for the second test."""
        if word_guessed is False:
            self.faults_df.loc[self.faults_df.shape[0]] = [row[0], row[1]]

    def compute_success_rate(self):
        """Compute success rate."""
        faults_total = self.faults_df.shape[0]
        success_rate = int(100 * (1 - (faults_total / self.words)))
        self.perf = success_rate

    def get_known_words(self) -> pd.DataFrame:
        """Identify the words that have been sufficiently guessed."""
        self.words_df['image'] = self.ordinate + self.steep * self.words_df['Nb']
        self.well_known_words = self.words_df[self.words_df['Taux'] >= self.words_df['image']]
        print("# DEBUG   | well known words", list(self.well_known_words[self.words_df.columns[0]]))



class Test(Interro):
    """First round"""
    def run(self):
        """Launch the vocabulary interoooooo !!!!"""
        self.create_random_step()
        self.index = self.step
        for i in range(1, self.words + 1):
            self.index = self.get_next_index()
            row = self.get_row()
            word_guessed = self.guess_word(row, i)
            self.update_voc_df(word_guessed)
            self.update_faults_df(word_guessed, row)

    def create_random_step(self):
        """Get random step, the jump from one word to another"""
        self.step = random.randint(1, self.words_df.shape[0])

    def get_next_index(self) -> int:
        """Get the next index. The word must not have been already asked."""
        next_index = (self.index + self.step) % self.words_df.shape[0]
        already_asked = self.words_df['Query'].loc[next_index] == 1
        title_row = next_index == 0
        while already_asked or title_row:
            next_index = (next_index + self.step) % self.words_df.shape[0]
            already_asked = self.words_df['Query'].loc[next_index] == 1
            title_row = next_index == 0
        return next_index

    def update_voc_df(self, word_guessed: str):
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



class Rattrap(Interro):
    """Rattrapage !!!"""
    def __init__(self, faults_df_: pd.DataFrame, rattraps: int):
        super().__init__(faults_df_)
        self.faults_df = faults_df_
        self.rattraps = rattraps

    def start_loop(self):
        """Start rattrapages loop."""
        if self.rattraps == -1:
            while self.faults_df.shape[0] > 0:
                self.run()
                self.compute_success_rate()
        else:
            for _ in range(chargeur.rattraps):
                if self.faults_df.shape[0] > 0:
                    self.run()
                    self.compute_success_rate()

    def run(self):
        """Launch the second test"""
        self.words = self.words_df.shape[0]
        for j in range(0, self.words):
            self.index = j
            row = self.get_row()
            word_guessed = self.guess_word(row, j+1)
            self.update_faults_df(word_guessed, row)



class Updater():
    """Update the tables of words (version and theme), counts, and archives."""
    def __init__(self, loader: Loader, interro: Interro):
        self.loader = loader
        self.interro = interro
        self.output_table_path = ''
        self.output_df = pd.DataFrame()

    def delete_known_words(self) -> pd.DataFrame:
        """Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will."""
        self.interro.words_df['image'] = self.interro.ordinate + self.interro.steep * self.interro.words_df['Nb']
        self.interro.words_df = self.interro.words_df[self.interro.words_df['Taux'] < self.interro.words_df['image']]

    def save_words(self):
        """Prepare the words table for saving, and save it."""
        self.delete_known_words()
        if 'Query' in self.interro.words_df.columns:
            self.interro.words_df.drop('Query', axis=1, inplace=True)
        self.interro.words_df.to_csv(self.loader.os_sep.join([r'.', 'data', self.loader.test_type + '_voc' + EXT]),
                                     index=False, sep=';')

    def set_output_table_path(self):
        """Determine the output tables according to the test type"""
        if self.loader.test_type == 'version':
            self.output_table_path = self.loader.os_sep.join(['.', 'data', 'theme_voc.csv'])
        elif self.loader.test_type == 'theme':
            self.output_table_path = self.loader.os_sep.join(['.', 'data', 'archives.csv'])
        else:
            print("# ERROR   | Wrong test_type argument in Updater class.")
            raise SystemExit

    def copy_well_known_words(self):
        """Copy the well-known words in the next step table"""
        self.output_df = pd.read_csv(self.output_table_path, sep=';', encoding='utf-8')
        missing_columns = set(self.output_df.columns).difference(set(self.interro.well_known_words))
        for column in missing_columns:
            self.interro.well_known_words[column] = [0] * self.interro.well_known_words.shape[0]
        self.output_df = pd.concat(self.output_df,
                                   self.interro.well_known_words)

    def transfer_well_known_words(self):
        """Transfer the well-known words in an ouput table, and save this."""
        self.set_output_table_path()
        self.copy_well_known_words()
        self.output_df.to_csv(self.output_table_path, index=False, sep=';')

    def save_performances(self):
        """Save performances for further analysis."""
        self.interro.perf_df.loc[self.interro.perf_df.shape[0]] = self.interro.perf
        self.interro.perf_df.to_csv(self.loader.paths['perf'],
                                    index=False, sep=';', encoding='utf-8')

    def save_words_count(self):
        """Save the length of vocabulary list in a file"""
        word_counts = self.interro.words_df.shape[0]
        count_before = self.interro.word_cnt_df.shape[0]
        today_date = date.today()
        self.interro.word_cnt_df.loc[count_before] = [today_date, word_counts]
        count_after = self.interro.word_cnt_df.shape[0]
        if count_after == count_before + 1:
            self.interro.word_cnt_df.to_csv(self.loader.paths['word_cnt'],
                                            index=False, sep=';')
        else:
            print("# ERROR   | Words count not saved.")

    def update_tables(self):
        """Main method of Updater class"""
        # self.transfer_well_known_words()
        self.save_words()
        self.save_performances()
        self.save_words_count()



class ViewQuestion():
    """View in MVC pattern."""
    def ask_word(self, title: str, row: List[str]):
        """Ask a word to the user through a GUI"""
        mot_etranger = row[0]
        text_1 = f"Quelle traduction donnez-vous pour : {mot_etranger}?"
        user_answer = messagebox.showinfo(title=title, message=text_1)
        if user_answer is False:
            print("# ERROR   | Interruption by user")
            raise SystemExit

    def check_word(self, title: str, row: str) -> bool:
        """Ask the user to decide if the answer was correct or not."""
        mot_natal = row[1]
        text_2 = f"Voici la traduction correcte : \'{mot_natal}\'. \nAviez-vous la bonne réponse ?"
        word_guessed = messagebox.askyesnocancel(title=title, message=text_2)
        if word_guessed is None:
            print("# ERROR   | Interruption by user")
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
    arguments = get_arguments()
    # Load data
    chargeur = Loader(arguments)
    chargeur.data_extraction()
    words_df = chargeur.data['voc']
    perf_df = chargeur.data['perf']
    word_cnt_df = chargeur.data['word_cnt']
    # WeuuuuAaaaaInterrooo !!!
    test_1 = Test(words_df, arguments, perf_df, word_cnt_df)
    test_1.run()
    test_1.compute_success_rate()
    # Rattraaaaaaap's !!!!
    rattrap = Rattrap(test_1.faults_df, chargeur.rattraps)
    rattrap.start_loop()
    # Save the results
    updater = Updater(chargeur, test_1)
    updater.update_tables()
