"""
    Creator:
        B.Delorme
    Creation date:
        2nd March 2023
    Main purpose:
        Logic of the vocabulary application, including the interoooooo!!!!!
"""

import argparse
import json
import os
import random
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data.database_interface import DbManipulator
from src.views.api import FastapiGuesser



class Loader():
    """
    Data loader.
    """
    def __init__(self, words, data_querier):
        """
        Must be done in the same session than the interroooo is launched.
        """
        self.data_querier = data_querier
        self.test_type = data_querier.test_type
        self.words = words
        self.tables = {}
        self.output_table = ''
        self.words_df = pd.DataFrame()
        self.interro_df = pd.DataFrame(columns=['foreign', 'native'])
        self.index = 0

    def load_tables(self):
        """
        Return the tables necessary for the interro to run.
        """
        self.tables = self.data_querier.get_tables()
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
        self.words_df = self.tables[voc]

    def adjust_test_length(self):
        """
        Check the test length.
        """
        words_table = self.tables[self.test_type + '_voc']
        words_total = words_table.shape[0]
        self.words = min(words_total, self.words)
        if self.words == 0:
            raise ValueError

    def get_random_step(self):
        """
        Get random step, the jump from one word to another
        """
        step = random.randint(1, self.words_df.shape[0])
        return step

    def get_another_index(self) -> int:
        """
        The word must not have been already asked.
        """
        next_index = random.randint(0, self.words_df.shape[0] - 1)
        next_index = max(next_index, 1)
        already_asked = self.words_df.loc[next_index, 'query'] == 1
        i = 0
        while already_asked and i < (self.words_df.shape[0]):
            next_index = random.randint(0, self.words_df.shape[0] - 1)
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

    def get_row(self) -> pd.DataFrame:
        """
        Get the row of the word to be asked
        """
        mot_etranger = self.words_df.loc[self.index, self.words_df.columns[0]]
        mot_natal = self.words_df.loc[self.index, self.words_df.columns[1]]
        row = [self.index, mot_etranger, mot_natal]
        return row

    def set_interro_df(self):
        """
        Extract the words that will be asked.
        """
        self.adjust_test_length()
        self.index = self.get_random_step()
        for _ in range(1, self.words + 1):
            self.index = self.get_next_index()
            row = self.get_row()
            self.interro_df.loc[row[0]] = row[1:]

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls):
        pass



class Interro(ABC):
    """
    Abstract class for interrooooo!!!! !!! !
    """
    def __init__(
            self,
            interro_df: pd.DataFrame,
            words: int,
            guesser
        ):
        self.interro_df = interro_df
        self.words = words
        self.guesser = guesser
        self.faults_df = pd.DataFrame(columns=[['foreign', 'native']])
        self.index = 1
        self.row = []

    @abstractmethod
    def to_dict(self):
        """
        Serialize the instance by turning its attributes into a dict.
        """

    @abstractmethod
    def from_dict(self):
        """
        Instantiate the instance from a dict of its attributes.
        """

    def update_faults_df(self, word_guessed: bool, row: List[str]):
        """
        Save the faulty answers for the second test.
        """
        if word_guessed is False:
            self.faults_df.loc[self.faults_df.shape[0]] = [row[-2], row[-1]]



class PremierTest(Interro):
    """
    First round!
    """
    def __init__(
            self,
            interro_df: pd.DataFrame,
            words: int,
            guesser,
        ):
        super().__init__(
            interro_df=interro_df,
            words=int(words),
            guesser=guesser
        )
        self.perf = 0

    def update_interro_df(self, word_guessed: bool):
        """
        Update the vocabulary dataframe
        """
        # Nb
        self.interro_df.loc[self.index, 'nb'] += 1
        # Score
        if word_guessed:
            self.interro_df.loc[self.index, 'score'] += 1
        else:
            self.interro_df.loc[self.index, 'score'] -= 1
        # Taux
        nombre = self.interro_df.loc[self.index, 'nb']
        score = self.interro_df.loc[self.index, 'score']
        taux = int(score / nombre * 100)
        self.interro_df.loc[self.index, 'taux'] = taux
        # Query
        self.interro_df.loc[self.index, 'query'] += 1

    def compute_success_rate(self):
        """
        Compute success rate.
        """
        faults_total = self.faults_df.shape[0]
        success_rate = int(100 * (1 - (faults_total / self.words)))
        self.perf = success_rate

    def to_dict(self):
        """
        Create a dict out of the instance attributes
        """
        attributes_dict = {
            'interro_dict': self.interro_df.to_json(orient='records'),
            'test_length': self.words,
            'index': self.index,
            'faults_dict': self.faults_df.to_json(orient='records'),
            'perf': self.perf,
        }
        return attributes_dict

    @classmethod
    def from_dict(cls, data):
        """
        Instanciate a PremierTest out of a dictionnary of arguments &
        class attributes.
        """
        words = data['test_length']
        interro_df = data['interro_df']
        guesser = FastapiGuesser()
        instance = cls(
            interro_df=interro_df,
            words=words,
            guesser=guesser,
        )
        instance.faults_df = data['faults_df']
        instance.index = data['index']
        instance.row = data['row']
        instance.perf = data['perf']
        return instance



class Rattrap(Interro):
    """
    Rattrapage !!!
    """
    def __init__(
            self,
            interro_df: pd.DataFrame,
            rattraps: int,
            guesser
        ):
        super().__init__(
            interro_df=interro_df,
            words=interro_df.shape[0],
            guesser=guesser
        )
        self.rattraps = int(rattraps)

    def reshuffle_words_table(self):
        """
        Shuffle the words table, so that the words are asked
        in a different order than the precedent test.
        """
        self.interro_df = self.interro_df.sample(frac=1)
        self.interro_df = self.interro_df.reset_index(drop=True)

    def to_dict(self):
        attributes_dict = {
            'interro_dict': self.interro_df.to_dict(),
            'words': self.words,
            'faults_dict': self.faults_df.to_dict(),
            'index': self.index,
            'rattraps': self.rattraps,
        }
        return attributes_dict

    @classmethod
    def from_dict(cls, data):
        interro_df = pd.DataFrame(data['interro_dict'])
        rattraps = data['rattraps']
        guesser = FastapiGuesser()
        instance = cls(
            interro_df=interro_df,
            rattraps=rattraps,
            guesser=guesser,
        )
        instance.words = data['words']
        instance.faults_df = pd.DataFrame(data['faults_dict'])
        instance.index = data['index']
        instance.row = data['row']
        return instance



class Updater():
    """
    Update tables.
    """
    def __init__(
            self,
            loader: Loader,
            interro: Interro
        ):
        self.loader = loader
        self.interro = interro
        self.good_words_df = pd.DataFrame()
        self.criteria = {}
        self.set_criteria()
        self.db_manipulator = DbManipulator(
            loader.data_querier.user_name,
            loader.data_querier.db_name,
            loader.data_querier.test_type,
        )

    def set_criteria(self):
        """
        Upload the dictionnary of criteria.
        By the way, can you say 'criteria' three times in a row?
        """
        with open(REPO_DIR + '/conf/interro.json', 'r', encoding='utf-8') as file:
            self.criteria = json.load(file)
        self.criteria = self.criteria['interro']

    def set_good_words(self):
        """
        Identify the words that have been sufficiently guessed.
        """
        ord_good = self.criteria['ORD_GOOD']
        steep_good = self.criteria['STEEP_GOOD']
        self.interro.words_df['img_good'] = ord_good + steep_good * self.interro.words_df['nb']
        self.good_words_df = self.interro.words_df[
            self.interro.words_df['taux'] >= self.interro.words_df['img_good']
        ]

    def copy_good_words(self):
        """
        Copy the well-good words in the next step table.
        """
        self.good_words_df = complete_columns(
            df_1=self.loader.tables['output'],
            df_2=self.good_words_df
        )
        self.loader.tables['output'] = pd.concat(
            [
                self.loader.tables['output'],
                self.good_words_df
            ]
        )

    def delete_good_words(self) -> pd.DataFrame:
        """
        Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will.
        """
        self.interro.words_df = self.interro.words_df[
            self.interro.words_df['taux'] < self.interro.words_df['img_good']
        ]
        self.interro.words_df = self.interro.words_df.drop('img_good', axis=1)

    def move_good_words(self):
        """
        Transfer the well-good words in an ouput table, and save this.
        """
        self.set_good_words()
        self.copy_good_words()
        self.loader.tables['output'].reset_index(inplace=True)
        self.db_manipulator.save_table(
            table_name='output',
            table=self.loader.tables['output']
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
        ord_bad = self.criteria['ORD_BAD']
        steep_bad = self.criteria['STEEP_BAD']
        self.interro.words_df['img_bad'] = ord_bad + steep_bad * self.interro.words_df['nb']
        self.interro.words_df['bad_word'] = np.where(
            self.interro.words_df['taux'] < self.interro.words_df['img_bad'], 1, 0
        )
        self.interro.words_df.drop('img_bad', axis=1, inplace=True)

    def save_words(self):
        """
        1) Reset the index of words dataframe.
        2) Use data handler instance to save the table in the database.
        """
        self.interro.words_df.reset_index(inplace=True)
        self.db_manipulator.save_table(
            table_name=self.loader.test_type + '_voc',
            table=self.interro.words_df
        )

    def save_performances(self):
        """
        1) Save the user performance & today date.
        2) Save the former in the performance table.
        3) Save the updated performance table through the data handler instance.
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
        self.db_manipulator.save_table(
            table_name=self.loader.test_type + '_perf',
            table=self.interro.perf_df
        )

    def save_words_count(self):
        """
        1)
        """
        def correct_words_cnt_df():
            """
            Correct the words count dataframe.
            """
            real_columns = set(self.interro.word_cnt_df.columns)
            expected_columns = {'test_date', 'nb'}
            if real_columns != expected_columns:
                self.interro.word_cnt_df.reset_index(inplace=True)

        count_before = self.interro.word_cnt_df.shape[0]
        new_row = pd.DataFrame(
            data={
                'test_date': datetime.today().date().strftime('%Y-%m-%d'),
                'nb': self.interro.words_df.shape[0]
            },
            index=[count_before]
        )
        correct_words_cnt_df()
        self.interro.word_cnt_df = pd.concat([
            self.interro.word_cnt_df,
            new_row
        ])
        self.interro.word_cnt_df.sort_index(inplace=True)
        self.db_manipulator.save_table(
            table_name=self.loader.test_type + '_words_count',
            table=self.interro.word_cnt_df
        )

    def update_data(self):
        """
        Main method of Updater class
        """
        self.move_good_words()
        self.flag_bad_words()
        self.save_words()
        self.save_performances()
        self.save_words_count()



def complete_columns(
        df_1: pd.DataFrame,
        df_2: pd.DataFrame
    ):
    """
    Guarantee that the well_known_words dataframe contains exactly
    the columns of the output dataframe
    """
    missing_columns = set(df_1.columns).difference(set(df_2.columns))
    for column in missing_columns:
        df_2[column] = [0] * df_2.shape[0]
    return df_2
