"""
    Creator:
        B.Delorme
    Creation date:
        2nd March 2023
    Main purpose:
        Logic of the vocabulary application, including the interoooooo!!!!!
"""

import argparse
import os
import random
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd
from loguru import logger

repo_dir = os.getcwd().split('src')[0]
sys.path.append(repo_dir)
from src import utils

STEEP_GOOD = -1.25
ORD_GOOD = 112.5
STEEP_BAD = 2.5
ORD_BAD = -125



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
        cond_1 = not self.settings.type
        cond_2 = not self.settings.words
        cond_3 = not self.settings.rattraps
        if cond_1 or cond_2 or cond_3:
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
    def __init__(self, rattraps, data_handler_):
        """Must be done in the same session than the interroooo is launched"""
        self.test_type = data_handler_.test_type
        self.rattraps = rattraps
        self.data_handler = data_handler_
        self.tables = {}
        self.output_table = ''

    def load_tables(self):
        """Return the tables necessary for the interro to run"""
        self.tables = self.data_handler.get_tables()
        voc = self.test_type + '_voc'
        self.tables[voc]['query'] = [0] * self.tables[voc].shape[0]
        self.tables[voc] = self.tables[voc].sort_values(
            by='creation_date',
            ascending=True
        )
        self.tables[voc]['taux'] = self.tables[voc]['taux'].replace(
            r',',
            r'.',
            regex=True
        )
        self.tables[voc]['taux'] = self.tables[voc]['taux'].astype(float)
        if 'bad_word' not in self.tables[voc].columns:
            self.tables[voc]['bad_word'] = [0] * self.tables[voc].shape[0]



class Interro(ABC):
    """Abstract class for interrooooo!!!! !!! !"""
    def __init__(self, words_df_: pd.DataFrame, words: int, guesser):
        self.words_df = words_df_
        self.words = words
        self.guesser = guesser
        self.faults_df = pd.DataFrame(columns=[['foreign', 'native']])
        self.index = 1
        self.row = []

    @abstractmethod
    def run(self):
        """Launch the interroooo !!!!"""

    def set_row(self) -> pd.DataFrame:
        """Get the row of the word to be asked"""
        mot_etranger = self.words_df.loc[self.index, self.words_df.columns[0]]
        mot_natal = self.words_df.loc[self.index, self.words_df.columns[1]]
        self.row = [self.index, mot_etranger, mot_natal]

    def update_faults_df(self, word_guessed: bool, row: List[str]):
        """Save the faulty answers for the second test."""
        if word_guessed is False:
            self.faults_df.loc[self.faults_df.shape[0]] = [row[-2], row[-1]]



class Test(Interro):
    """First round"""
    def __init__(self, words_df_, words: int, guesser, perf_df_=None, words_cnt_df=None):
        super().__init__(words_df_, int(words), guesser)
        self.perf_df = perf_df_
        self.word_cnt_df = words_cnt_df
        self.perf = 0
        self.step = 0
        self.interro_df = pd.DataFrame(columns=['english', 'français'])

    def create_random_step(self):
        """Get random step, the jump from one word to another"""
        self.step = random.randint(1, self.words_df.shape[0])

    def get_another_index(self) -> int:
        """The word must not have been already asked."""
        next_index = random.randint(1, self.words_df.shape[0] - 1)
        next_index = max(next_index, 1)
        # logger.debug(f"words_df shape: {self.words_df.shape}")
        # logger.debug(f"words_df head: \n{self.words_df.head()}")
        already_asked = self.words_df.loc[next_index, 'query'] == 1
        i = 0
        while already_asked and i < (self.words_df.shape[0] + 1):
            next_index = random.randint(1, self.words_df.shape[0] - 1)
            next_index = max(next_index, 1)
            already_asked = self.words_df.loc[next_index, 'query'] == 1
            i += 1
        self.words_df.loc[next_index, 'query'] = 1
        return next_index

    def get_next_index(self) -> int:
        """
        If the word is NOT a bad word, it IS skipped.
        This process happens only once, it is not a loop.
        If the word IS a bad word, it is NOT skipped.
        This way, bad words are asked twice as much as other words.
        """
        another_index = self.get_another_index()
        bad_word = self.words_df.loc[another_index, 'bad_word'] == 1
        if bad_word:
            next_index = another_index
        else:
            self.words_df.loc[another_index, 'query'] = 0
            next_index = self.get_another_index()
        return next_index

    def set_interro_df(self):
        """Extract the words that will be asked."""
        self.create_random_step()
        self.index = self.step
        for _ in range(1, self.words + 1):
            self.index = self.get_next_index()
            self.set_row()
            self.interro_df.loc[self.row[0]] = self.row[1:]

    def update_voc_df(self, word_guessed: bool):
        """Update the vocabulary dataframe"""
        # -----
        self.words_df.loc[self.index, 'nb'] += 1
        # -----
        if word_guessed:
            self.words_df.loc[self.index, 'score'] += 1
        else:
            self.words_df.loc[self.index, 'score'] -= 1
        # -----
        nombre = self.words_df.loc[self.index, 'nb']
        score = self.words_df.loc[self.index, 'score']
        taux = int(score / nombre * 100)
        self.words_df.loc[self.index, 'taux'] = taux
        # -----
        self.words_df.loc[self.index, 'query'] += 1

    def ask_series_of_guesses(self):
        """
        1) Extract one sample
        2) Ask a guess to the user
        3) Update the words table with the user input
        4) Update the faults table with the user input
        """
        for i, index in enumerate(self.interro_df.index):
            row = list(self.interro_df.loc[index])
            word_guessed = self.guesser.guess_word(row, i + 1, self.words)
            self.update_voc_df(word_guessed)
            self.update_faults_df(word_guessed, row)

    def compute_success_rate(self):
        """Compute success rate."""
        faults_total = self.faults_df.shape[0]
        success_rate = int(100 * (1 - (faults_total / self.words)))
        self.perf = success_rate

    def run(self):
        """
        1) Set the interro table,
        2) Ask guesses to the user,
        3) Compute the performances.
        """
        self.set_interro_df()
        self.ask_series_of_guesses()
        self.compute_success_rate()



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
            self.set_row()
            word_guessed = self.guesser.guess_word(self.row, j+1, words_total)
            self.update_faults_df(word_guessed, self.row)
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
        self.good_words_df = pd.DataFrame()

    def set_good_words(self):
        """Identify the words that have been sufficiently guessed."""
        self.interro.words_df['img_good'] = ORD_GOOD + STEEP_GOOD * self.interro.words_df['nb']
        self.good_words_df = self.interro.words_df[
            self.interro.words_df['taux'] >= self.interro.words_df['img_good']
        ]

    def copy_good_words(self):
        """Copy the well-good words in the next step table."""
        logger.debug(f"Table names:\n{self.loader.tables.keys()}")
        self.good_words_df = utils.complete_columns(
            self.loader.tables['output'],
            self.good_words_df
        )
        self.loader.tables['output'] = pd.concat(
            [
                self.loader.tables['output'],
                self.good_words_df
            ]
        )

    def delete_good_words(self) -> pd.DataFrame:
        """Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will."""
        self.interro.words_df = self.interro.words_df[
            self.interro.words_df['taux'] < self.interro.words_df['img_good']
        ]
        self.interro.words_df.drop('img_good', axis=1, inplace=True)

    def move_good_words(self):
        """Transfer the well-good words in an ouput table, and save this."""
        self.set_good_words()
        self.copy_good_words()
        self.loader.tables['output'].reset_index(inplace=True)
        self.loader.data_handler.save_table(
            'output',
            self.loader.tables['output']
        )
        self.delete_good_words()

    def flag_bad_words(self):
        """
        1) Drop the img_bad columns if present.
        2) Create the img_bad columns, that is the score of each word if it were a bad word,
        based on the number of guesses on it.
        3) Flag the words having a worst score as their bad_image, as bad words.
        4) Drop the img_bad column.
        """
        self.interro.words_df['img_bad'] = ORD_BAD + STEEP_BAD * self.interro.words_df['nb']
        self.interro.words_df['bad_word'] = np.where(
            self.interro.words_df['taux'] < self.interro.words_df['img_bad'], 1, 0
        )
        self.interro.words_df.drop('img_bad', axis=1, inplace=True)

    def save_words(self):
        """
        1) Reset the index of words dataframe.
        2) Use data_handler instance to save the table in the database.
        """
        self.interro.words_df.reset_index(inplace=True)
        self.loader.data_handler.save_table(
            self.loader.test_type + '_voc',
            self.interro.words_df
        )

    def save_performances(self):
        """
        1) Save the user performance & today date.
        2) Save the former in the performance table.
        3) Save the updated performance table through the data_handler instance.
        """
        new_row = pd.DataFrame(
            data={
                'test_date': datetime.today().date().strftime('%Y-%m-%d'),
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
        """
        1) 
        """
        count_before = self.interro.word_cnt_df.shape[0]
        new_row = pd.DataFrame(
            data={
                'test_date': datetime.today().date().strftime('%Y-%m-%d'),
                'words_count': self.interro.words_df.shape[0]
                },
            index=[count_before + 1]
        )
        self.interro.word_cnt_df = pd.concat(
            [
                self.interro.word_cnt_df,
                new_row
            ]
        )
        self.interro.word_cnt_df.sort_index(inplace=True)
        self.interro.word_cnt_df.reset_index(
            inplace=True,
            names=['id_test']
        )
        self.loader.data_handler.save_table(
            self.loader.test_type + '_words_count',
            self.interro.word_cnt_df
        )

    def update_data(self):
        """Main method of Updater class"""
        self.move_good_words()
        self.flag_bad_words()
        self.save_words()
        self.save_performances()
        self.save_words_count()
