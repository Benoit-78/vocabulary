# -*- coding: utf-8 -*-
"""
    Author: B.Delorme
    Mail: delormebenoit211@gmail.com
    Creation date: 2nd March 2023
    Main purpose: main script of vocabulary application.
"""

import random
import argparse
from datetime import date
from abc import ABC, abstractmethod
import sys
from typing import List
import pandas as pd
import numpy as np
import uvicorn

from data import data_handler
import views

STEEP_GOOD = -1.25
ORDINATE_GOOD = 112.5
STEEP_BAD = 2.5
ORDINATE_BAD = -125



class CliUser():
    "Class dedicated to users that launche the app through the CLI."
    def __init__(self):
        self.settings = None

    def parse_arguments(self, arg: List[str]) -> argparse.Namespace:
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
        self.settings = another_parser.parse_args(arg)

    def get_settings(self) -> argparse.Namespace:
        """Check the kind of interro, version or theme"""
        self.parse_arguments(sys.argv[1:])
        if not self.settings.type or not self.settings.words or not self.settings.rattraps :
            message = ' '.join([
                "# ERROR: Please give",
                "-t <test type>, ",
                "-w <number of words> and ",
                "-r <number of rattraps>"
            ])
            print(message)
            raise SystemExit
        if self.settings.type == '':
            print("# ERROR: Please give a test type: either version or theme")
            raise SystemExit
        if self.settings.type not in ['version', 'theme']:
            print("# ERROR: Test type must be either version or theme")
            raise SystemExit
        if self.settings.rattraps < -1:
            print("# ERROR: Number of rattraps must be greater than -1.")
            raise SystemExit
        if self.settings.words < 1:
            print("# ERROR: Number of words must be greater than 0.")
            raise SystemExit



class Loader():
    """Data loader"""
    def __init__(self, test_type, rattraps, data_handler_):
        """Must be done in the same session than the interroooo is launched"""
        self.test_type = test_type
        self.rattraps = rattraps
        self.tables = {}
        self.data_handler = data_handler_
        self.output_table = ''

    def load_tables(self):
        """Return the tables necessary for the interro to run"""
        self.tables = self.data_handler.get_tables()
        voc_table = self.test_type + '_voc'
        print("# DEBUG: ")
        self.tables[voc_table]['Query'] = [0] * self.tables[voc_table].shape[0]
        self.tables[voc_table] = self.tables[voc_table].sort_values(by='Date', ascending=True)
        self.tables[voc_table] = self.tables[voc_table].replace(r',', r'.', regex=True)
        self.tables[voc_table]['Taux'] = self.tables[voc_table]['Taux'].astype(float)
        if 'bad_word' not in self.tables[voc_table].columns:
            self.tables[voc_table]['bad_word'] = [0] * self.tables[voc_table].shape[0]



class Interro(ABC):
    """Abstract class for interrooooo!!!! !!! !"""
    def __init__(
        self,
        words_df_: pd.DataFrame,
        args: argparse.Namespace,
        guesser
        ):
        self.words_df = words_df_
        self.words = args.words
        self.guesser = guesser
        self.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
        self.index = 1

    @abstractmethod
    def run(self):
        """Launch the interroooo !!!!"""

    def get_row(self) -> List[str]:
        """Get the row of the word to be asked"""
        mot_etranger = self.words_df[self.words_df.columns[0]].loc[self.index]
        mot_natal = self.words_df[self.words_df.columns[1]].loc[self.index]
        row = [mot_etranger, mot_natal]
        return row

    def update_faults_df(self, word_guessed: bool, row: List[str]):
        """Save the faulty answers for the second test."""
        if word_guessed is False:
            self.faults_df.loc[self.faults_df.shape[0]] = [row[0], row[1]]



class Test(Interro):
    """First round"""
    def __init__(
        self,
        words_df_,
        args: argparse.Namespace,
        guesser,
        perf_df_: pd.DataFrame=None,
        words_cnt_df: pd.DataFrame=None,
        output_df: pd.DataFrame=None):
        super().__init__(words_df_, args, guesser)
        self.perf_df = perf_df_
        self.word_cnt_df = words_cnt_df
        self.output_df = output_df
        self.perf = []
        self.step = 0
        self.interro_df = pd.DataFrame(columns=['english', 'french'])

    def create_random_step(self):
        """Get random step, the jump from one word to another"""
        self.step = random.randint(1, self.words_df.shape[0])

    def get_another_index(self) -> int:
        """The word must not have been already asked."""
        next_index = (self.index + self.step) % self.words_df.shape[0]
        already_asked = self.words_df['Query'].loc[next_index] == 1
        title_row = next_index == 0
        while already_asked or title_row:
            next_index = (next_index + self.step) % self.words_df.shape[0]
            already_asked = self.words_df['Query'].loc[next_index] == 1
            title_row = next_index == 0
        return next_index

    def get_next_index(self) -> int:
        """
        If the word is NOT a bad word, it is skipped and another word is searched.
        This process is not a loop, it happens only once.
        This way, bad words (which are not skipped) are asked twice as much as other words.
        """
        another_index = self.get_another_index()
        bad_word = self.words_df['bad_word'].loc[another_index] == 1
        if not bad_word:
            next_index = self.get_another_index()
        else:
            next_index = another_index
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

    def get_interro_df(self):
        """Extract the words that will be asked."""
        self.create_random_step()
        self.index = self.step
        for _ in range(1, self.words + 1):
            self.index = self.get_next_index()
            row = self.get_row()
            self.interro_df.loc[len(self.interro_df)] = row

    def run(self):
        """Launch the vocabulary interoooooo !!!!"""
        for i in range(1, len(self.interro_df) + 1):
            row = self.interro_df.loc[i-1]
            word_guessed = self.guesser.guess_word(row, i, self.words)
            self.update_voc_df(word_guessed)
            self.update_faults_df(word_guessed, row)

    def compute_success_rate(self):
        """Compute success rate."""
        faults_total = self.faults_df.shape[0]
        success_rate = int(100 * (1 - (faults_total / self.words)))
        self.perf = success_rate



class Rattrap(Interro):
    """Rattrapage !!!"""
    def __init__(
        self,
        faults_df_: pd.DataFrame,
        arguments_: argparse.Namespace,
        guesser):
        super().__init__(faults_df_, arguments_, guesser)
        self.words_df = faults_df_.copy()
        self.rattraps = arguments_.rattraps

    def run(self):
        """Launch a rattrapage"""
        words_total = self.words_df.shape[0]
        for j in range(0, words_total):
            self.index = j
            row = self.get_row()
            word_guessed = self.guesser.guess_word(row, j+1, words_total)
            self.update_faults_df(word_guessed, row)
        self.words_df = self.faults_df.copy()
        self.faults_df.drop(self.faults_df.index, inplace=True)

    def start_loop(self):
        """Start rattrapages loop."""
        if self.rattraps == -1:
            while self.words_df.shape[0] > 0:
                self.run()
        else:
            for _ in range(self.rattraps):
                if self.words_df.shape[0] > 0:
                    self.run()



class Updater():
    """Update the tables of words (version and theme), counts, and archives."""
    def __init__(self, loader: Loader, interro: Interro):
        self.loader = loader
        self.interro = interro
        self.well_known_words = pd.DataFrame()
        self.output_table_name = ''

    def get_known_words(self):
        """Identify the words that have been sufficiently guessed."""
        self.interro.words_df['image_good'] = (
            ORDINATE_GOOD + STEEP_GOOD * self.interro.words_df['Nb']
        ) / 100
        self.well_known_words = self.interro.words_df[
            self.interro.words_df['Taux'] >= self.interro.words_df['image_good']
        ]

    def get_output_table_name(self):
        """Get output table name."""
        test_types = ['version', 'theme']
        test_types.remove(self.loader.test_type)
        self.output_table_name = test_types[0] + '_voc'

    def copy_well_known_words(self):
        """Copy the well-known words in the next step table"""
        self.get_known_words()
        self.get_output_table_name()
        output_col = self.loader.tables[self.output_table_name].columns
        well_known_words_col = self.well_known_words.columns
        missing_columns = set(output_col).difference(set(well_known_words_col))
        for column in missing_columns:
            self.well_known_words[column] = [0] * self.well_known_words.shape[0]
        self.loader.tables[self.output_table_name] = pd.concat(
            [self.loader.tables[self.output_table_name],
            self.well_known_words]
        )

    def transfer_well_known_words(self):
        """Transfer the well-known words in an ouput table, and save this."""
        self.copy_well_known_words()
        self.loader.data_handler.save_table(
            self.output_table_name,
            self.loader.tables[self.output_table_name]
        )

    def delete_known_words(self) -> pd.DataFrame:
        """Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will."""
        self.interro.words_df = self.interro.words_df[
            self.interro.words_df['Taux'] < self.interro.words_df['image_good']
        ]
        self.interro.words_df.drop('image_good', axis=1, inplace=True)

    def flag_bad_words(self):
        """
            Apply special flag to difficult words,
            i.e. words that are rarely guessed by the user.
        """
        if 'image_bad' in self.interro.words_df.columns:
            self.interro.words_df.drop('image_bad', axis=1, inplace=True)
        self.interro.words_df['image_bad'] = (
            ORDINATE_BAD + STEEP_BAD * self.interro.words_df['Nb']
        ) / 100
        self.interro.words_df['bad_word'] = np.where(
            self.interro.words_df['Taux'] < self.interro.words_df['image_bad'],
            1,
            0
        )
        self.interro.words_df.drop('image_bad', axis=1, inplace=True)

    def save_words(self):
        """Prepare the words table for saving, and save it."""
        self.loader.data_handler.save_table(
            self.loader.test_type + '_voc',
            self.interro.words_df
        )

    def save_performances(self):
        """Save performances for further analysis."""
        self.interro.perf_df.loc[self.interro.perf_df.shape[0]] = self.interro.perf
        self.loader.data_handler.save_table(
            self.loader.test_type + '_perf',
            self.interro.perf_df
        )

    def save_words_count(self):
        """Save the length of vocabulary list in a file"""
        word_counts = self.interro.words_df.shape[0]
        count_before = self.interro.word_cnt_df.shape[0]
        today_date = date.today()
        self.interro.word_cnt_df.loc[count_before] = [today_date, word_counts]
        count_after = self.interro.word_cnt_df.shape[0]
        if count_after == count_before + 1:
            self.loader.data_handler.save_table(
                self.loader.test_type + '_words_count',
                self.interro.word_cnt_df
            )
        else:
            print("# ERROR: Words count not saved.")

    def update_data(self):
        """Main method of Updater class"""
        self.transfer_well_known_words()
        self.delete_known_words()
        self.flag_bad_words()
        self.save_words()
        self.save_performances()
        self.save_words_count()



def cli_main():
    """Highest level of abstraction for interro!!! program."""
    # Get user settings
    user = CliUser()
    user.get_settings()
    # Load data
    data_handler_ = data_handler.MariaDBHandler(user.settings.type)
    loader = Loader(
        user.settings.type,
        user.settings.rattraps,
        data_handler_
    )
    loader.load_tables()
    # WeuuAaaInterrooo !!!
    guesser = views.CliGuesser()  # /!\
    test = Test(
        loader.tables[loader.test_type + '_voc'],
        user.settings,
        guesser,
        loader.tables[loader.test_type + '_perf'],
        loader.tables[loader.test_type + '_words_count']
    )
    test.get_interro_df()
    test.run()  # /!\
    test.compute_success_rate()
    # Rattraaaaaaap's !!!!
    rattrap = Rattrap(
        test.faults_df,
        user.settings,
        guesser
    )
    rattrap.start_loop()  # /!\
    # Save the results
    updater = Updater(loader, test)
    updater.update_data()


if __name__ == '__main__':
    cli_main()
