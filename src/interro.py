# -*- coding: utf-8 -*-
"""
    Author: B.Delorme
    Mail: delormebenoit211@gmail.com
    Creation date: 2nd March 2023
    Main purpose: script containing the logic of the vocabulary application.
"""

import random
import argparse
from datetime import date, datetime
from abc import ABC, abstractmethod
import sys
from typing import List
import pandas as pd
import numpy as np
from loguru import logger


STEEP_GOOD = -1.25
ORDINATE_GOOD = 112.5
STEEP_BAD = 2.5
ORDINATE_BAD = -125



class CliUser():
    """User who launchs the app through the CLI."""
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
                "Please give",
                "-t <test type>, ",
                "-w <number of words> and ",
                "-r <number of rattraps>"
            ])
            logger.error(message)
            raise SystemExit
        if self.settings.type == '':
            logger.error("Please give a test type: either version or theme")
            raise SystemExit
        if self.settings.type not in ['version', 'theme']:
            logger.error("Test type must be either version or theme")
            raise SystemExit
        if self.settings.rattraps < -1:
            logger.error("Number of rattraps must be greater than -1.")
            raise SystemExit
        if self.settings.words < 1:
            logger.error("Number of words must be greater than 0.")
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
        voc = self.test_type + '_voc'
        self.tables[voc]['Query'] = [0] * self.tables[voc].shape[0]
        self.tables[voc] = self.tables[voc].sort_values(by='Date_de_creation', ascending=True)
        self.tables[voc]['Taux'] = self.tables[voc]['Taux'].replace(r',', r'.', regex=True)
        self.tables[voc]['Taux'] = self.tables[voc]['Taux'].astype(float)
        if 'bad_word' not in self.tables[voc].columns:
            self.tables[voc]['bad_word'] = [0] * self.tables[voc].shape[0]



class Interro(ABC):
    """Abstract class for interrooooo!!!! !!! !"""
    def __init__(
        self,
        words_df_: pd.DataFrame,
        words,
        guesser
        ):
        self.words_df = words_df_
        self.words = words
        self.guesser = guesser
        self.faults_df = pd.DataFrame(columns=[['Foreign', 'Native']])
        self.index = 1

    @abstractmethod
    def run(self):
        """Launch the interroooo !!!!"""

    def get_row(self) -> pd.DataFrame:
        """Get the row of the word to be asked"""
        mot_etranger = self.words_df.loc[self.index, self.words_df.columns[0]]
        mot_natal = self.words_df.loc[self.index, self.words_df.columns[1]]
        row = [self.index, mot_etranger, mot_natal]
        return row

    def update_faults_df(self, word_guessed: bool, row: List[str]):
        """Save the faulty answers for the second test."""
        if word_guessed is False:
            self.faults_df.loc[self.faults_df.shape[0]] = [row[-2], row[-1]]



class Test(Interro):
    """First round"""
    def __init__(
        self,
        words_df_,
        words: int,
        guesser,
        perf_df_: pd.DataFrame=None,
        words_cnt_df: pd.DataFrame=None,
        ):
        super().__init__(words_df_, int(words), guesser)
        self.perf_df = perf_df_
        self.word_cnt_df = words_cnt_df
        self.perf = 0
        self.step = 0
        self.interro_df = pd.DataFrame(columns=['english', 'french'])

    def create_random_step(self):
        """Get random step, the jump from one word to another"""
        self.step = random.randint(1, self.words_df.shape[0])

    def get_another_index(self) -> int:
        """The word must not have been already asked."""
        next_index = (self.index + self.step) % self.words_df.shape[0]
        already_asked = self.words_df.loc[next_index, 'Query'] == 1
        title_row = next_index == 0
        while already_asked or title_row:
            next_index = (next_index + self.step) % self.words_df.shape[0]
            already_asked = self.words_df.loc[next_index, 'Query'] == 1
            title_row = next_index == 0
        return next_index

    def get_next_index(self) -> int:
        """
        If the word is NOT a bad word, it is skipped and another word is searched.
        This process is not a loop, it happens only once.
        Bad words are not skipped: this way, they are asked twice as much as other words.
        """
        another_index = self.get_another_index()
        bad_word = self.words_df.loc[another_index, 'bad_word'] == 1
        if not bad_word:
            next_index = self.get_another_index()
        else:
            next_index = another_index
        return next_index

    def update_voc_df(self, word_guessed: bool):
        """Update the vocabulary dataframe"""
        # Update Nb
        self.words_df.loc[self.index, 'Nb'] += 1
        # Update Score
        if word_guessed:
            self.words_df.loc[self.index, 'Score'] += 1
        else:
            self.words_df.loc[self.index, 'Score'] -= 1
        # Update Taux
        nombre = self.words_df.loc[self.index, 'Nb']
        score = self.words_df.loc[self.index, 'Score']
        taux = int(score / nombre * 100)
        self.words_df.loc[self.index, 'Taux'] = taux
        # Update Query
        self.words_df.loc[self.index, 'Query'] += 1

    def set_interro_df(self):
        """Extract the words that will be asked."""
        self.create_random_step()
        self.index = self.step
        for _ in range(1, self.words + 1):
            self.index = self.get_next_index()
            row = self.get_row()
            self.interro_df.loc[row[0]] = row[1:]

    def run(self):
        """Launch the vocabulary interoooooo !!!!"""
        self.set_interro_df()
        for i, index in enumerate(self.interro_df.index):
            row = self.interro_df.loc[index]
            word_guessed = self.guesser.guess_word(row, i+1, self.words)
            self.update_voc_df(word_guessed)
            self.update_faults_df(word_guessed, row)
        self.compute_success_rate()

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
        rattraps: int,
        guesser
        ):
        super().__init__(faults_df_, faults_df_.shape[0], guesser)
        self.words_df = faults_df_.copy()
        self.rattraps = int(rattraps)

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
    """Update tables."""
    def __init__(self, loader: Loader, interro: Interro):
        self.loader = loader
        self.interro = interro
        self.well_known_words = pd.DataFrame()
        self.output_table_name = ''

    def get_known_words(self):
        """Identify the words that have been sufficiently guessed."""
        self.interro.words_df['img_good'] = ORDINATE_GOOD + STEEP_GOOD * self.interro.words_df['Nb']
        self.well_known_words = self.interro.words_df[
            self.interro.words_df['Taux'] >= self.interro.words_df['img_good']
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
        self.loader.tables[self.output_table_name].reset_index(inplace=True)
        self.loader.data_handler.save_table(
            self.output_table_name,
            self.loader.tables[self.output_table_name]
        )

    def delete_well_known_words(self) -> pd.DataFrame:
        """Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will."""
        self.interro.words_df = self.interro.words_df[
            self.interro.words_df['Taux'] < self.interro.words_df['img_good']
        ]
        self.interro.words_df.drop('img_good', axis=1, inplace=True)

    def flag_bad_words(self):
        """Apply special flag to difficult words, i.e. words that are rarely guessed by the user."""
        if 'img_bad' in self.interro.words_df.columns:
            self.interro.words_df.drop('img_bad', axis=1, inplace=True)
        self.interro.words_df['img_bad'] = ORDINATE_BAD + STEEP_BAD * self.interro.words_df['Nb']
        self.interro.words_df['bad_word'] = np.where(
            self.interro.words_df['Taux'] < self.interro.words_df['img_bad'],
            1,
            0
        )
        self.interro.words_df.drop('img_bad', axis=1, inplace=True)

    def save_words(self):
        """Prepare the words table for saving, and save it."""
        self.interro.words_df.reset_index(inplace=True)
        self.loader.data_handler.save_table(
            self.loader.test_type + '_voc',
            self.interro.words_df
        )

    def save_performances(self):
        """Save performances for further analysis."""
        new_row = pd.DataFrame(
            data={
                'date_du_test': datetime.today().date().strftime('%Y-%m-%d'),
                'test': self.interro.perf
                },
            index=[self.interro.perf_df.shape[0] + 1]
        )
        self.interro.perf_df = pd.concat([self.interro.perf_df, new_row])
        self.interro.perf_df.reset_index(inplace=True, names=['id_test'])
        self.loader.data_handler.save_table(
            self.loader.test_type + '_perf',
            self.interro.perf_df
        )

    def save_words_count(self):
        """Save the length of vocabulary list in a file"""
        count_before = self.interro.word_cnt_df.shape[0]
        new_row = pd.DataFrame(
            data={
                'date_du_test': datetime.today().date().strftime('%Y-%m-%d'),
                'nombre_de_mots': self.interro.words_df.shape[0]
                },
            index=[count_before + 1]
        )
        self.interro.word_cnt_df = pd.concat([self.interro.word_cnt_df, new_row])
        self.interro.word_cnt_df.sort_index(inplace=True)
        count_after = self.interro.word_cnt_df.shape[0]
        if count_after == count_before + 1:
            self.interro.word_cnt_df.reset_index(inplace=True, names=['id_test'])
            self.loader.data_handler.save_table(
                self.loader.test_type + '_words_count',
                self.interro.word_cnt_df
            )
        else:
            logger.error("Words count could not be saved.")

    def update_data(self):
        """Main method of Updater class"""
        self.transfer_well_known_words()
        self.delete_well_known_words()
        self.flag_bad_words()
        self.save_words()
        self.save_performances()
        self.save_words_count()
