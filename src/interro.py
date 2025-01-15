"""
    Creator:
        B.Delorme
    Creation date:
        2nd March 2023
    Main purpose:
        Logic of the vocabulary application, including the interoooooo!!!!!
"""

import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME

from src.data.database_interface import DbManipulator, DbQuerier
from src.views.api import FastapiGuesser



class Loader():
    """
    Data loader.
    """
    def __init__(self, test_length: int, data_querier: DbQuerier):
        """
        Must be done in the same session than the interroooo is launched.
        """
        self.data_querier = data_querier
        self.test_type = data_querier.test_type
        self.test_length = test_length
        self.tables: Dict[str, pd.DataFrame] = {}
        self.output_table = ''
        self.words_df = pd.DataFrame()
        self.interro_df = pd.DataFrame(
            columns=[
                'foreign',
                'native',
                'creation_date',
                'nb',
                'score',
                'taux',
                'query',
                'bad_word'
            ]
        )
        self.index = 0
        self.perf_df = pd.DataFrame()
        self.words_count_df = pd.DataFrame()
        self.criteria: Dict[str, float] = {}
        self.set_criteria()

    def set_criteria(self):
        """
        Upload the dictionnary of criteria.
        By the way, can you say 'criteria' three times in a row?
        """
        with open(REPO_DIR + '/conf/interro.json', 'r', encoding='utf-8') as file:
            raw_criteria = json.load(file)
        self.criteria = raw_criteria['interro']

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
        self.words_df['img_bad'] = ord_bad + steep_bad * self.words_df['nb']
        self.words_df['bad_word'] = np.where(
            self.words_df['taux'] < self.words_df['img_bad'], 1, 0
        )
        self.words_df.drop('img_bad', axis=1, inplace=True)

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
        self.flag_bad_words()
        self.perf_df = self.tables[self.test_type + '_perf']
        self.words_count_df = self.tables[self.test_type + '_words_count']

    def adjust_test_length(self):
        """
        Check the test length.
        """
        words_table = self.tables[self.test_type + '_voc']
        words_total = words_table.shape[0]
        self.test_length = min(words_total, self.test_length)
        if self.test_length == 0:
            logger.error("Test length is equal to 0!")
            raise ValueError

    def set_interro_df(self):
        """
        Extract the words that will be asked.
        """
        self.adjust_test_length()
        bad_words_df = self.words_df[self.words_df['bad_word']==1]
        good_words_df = self.words_df[self.words_df['bad_word']==0]
        enough_bad_words = bad_words_df.shape[0] >= self.test_length * 0.67
        enough_good_words = good_words_df.shape[0] >= self.test_length * 0.33
        if enough_bad_words:
            if enough_good_words:
                bad_words_df = bad_words_df.sample(n=int(self.test_length * 0.67))
                sample_size = self.test_length - bad_words_df.shape[0]
                good_words_df = good_words_df.sample(n=sample_size)
                self.interro_df = pd.concat([bad_words_df, good_words_df])
            else:
                sample_size = self.test_length - good_words_df.shape[0]
                sample_size = min(sample_size, bad_words_df.shape[0])
                bad_words_df = bad_words_df.sample(n=sample_size)
                self.interro_df = pd.concat([bad_words_df, good_words_df])
        else:
            if enough_good_words:
                sample_size = self.test_length - bad_words_df.shape[0]
                sample_size = min(sample_size, bad_words_df.shape[0])
                good_words_df = good_words_df.sample(n=sample_size)
                self.interro_df = pd.concat([bad_words_df, good_words_df])
            else:
                self.interro_df = pd.concat([bad_words_df, good_words_df])
                self.test_length = self.interro_df.shape[0]
        self.interro_df = self.interro_df.sort_index()



class Interro(ABC):
    """
    Abstract class for interrooooo!!!! !!! !
    """
    def __init__(
            self,
            interro_df: pd.DataFrame,
            test_length: int,
            guesser
        ):
        self.interro_df: pd.DataFrame = interro_df
        self.test_length = test_length
        self.guesser = guesser
        self.faults_df = pd.DataFrame(columns=[['foreign', 'native']])
        self.index = 0

    @abstractmethod
    def to_dict(self):
        """
        Serialize the instance by turning its attributes into a dict.
        """

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]):
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
            test_length: int,
            guesser: FastapiGuesser,
        ):
        super().__init__(
            interro_df=interro_df,
            test_length=int(test_length),
            guesser=guesser
        )
        self.perf = 0
        self.index = int(self.interro_df.index[0].item())

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
        nombre = int(self.interro_df.at[self.index, 'nb'])
        score = int(self.interro_df.at[self.index, 'score'])
        taux = int(score / nombre * 100)
        self.interro_df.loc[self.index, 'taux'] = taux
        # Query
        self.interro_df.loc[self.index, 'query'] += 1

    def update_index(self):
        """
        Update the current index.
        """
        indices = list(self.interro_df.index)
        for idx_nb, idx in enumerate(indices):
            if idx == self.index:
                self.index = indices[idx_nb + 1]
                break

    def compute_success_rate(self):
        """
        Compute success rate.
        """
        faults_total = self.faults_df.shape[0]
        success_rate = int(100 * (1 - (faults_total / self.test_length)))
        self.perf = success_rate

    def to_dict(self) -> Dict[str, Any]:
        """
        Create a dict out of the instance attributes
        Keys of the dictionnary have the JavaScript case.
        """
        self.interro_df = self.interro_df.reset_index(names='index')
        attributes_dict = {
            'faultsDict': self.faults_df.to_json(orient='records'),
            'interroDict': self.interro_df.to_json(orient='records'),
            'testIndex': self.index,
            'testLength': self.test_length,
            'testPerf': self.perf,
        }
        return attributes_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PremierTest':
        """
        Instanciate a PremierTest out of a dictionnary of arguments &
        class attributes.
        Keys of the input dictionnary have the JavaScript case.
        """
        test_length = data['testLength']
        interro_df = data['interroTable']
        guesser = FastapiGuesser()
        instance = cls(
            interro_df=interro_df,
            test_length=test_length,
            guesser=guesser,
        )
        instance.faults_df = data['faultsTable']
        instance.index = data['testIndex']
        instance.perf = data['testPerf']
        return instance



class Rattrap(Interro):
    """
    Rattrapage !!!
    """
    def __init__(
            self,
            interro_df: pd.DataFrame,
            guesser: FastapiGuesser,
            old_interro_df: pd.DataFrame
        ):
        super().__init__(
            interro_df=interro_df,
            test_length=interro_df.shape[0],
            guesser=guesser
        )
        self.rattrap = True
        self.old_interro_df = old_interro_df

    def reshuffle_words_table(self):
        """
        Shuffle the words table, so that the words are asked
        in a different order than the precedent test.
        """
        old_index = list(self.interro_df.index)
        if len(old_index) == 1:
            return True
        new_index = list(self.interro_df.index)
        iterations = 0
        while new_index == old_index and iterations < 100:
            self.interro_df = self.interro_df.sample(frac=1)
            new_index = list(self.interro_df.index)
            iterations += 1
        self.interro_df = self.interro_df.reset_index(drop=True)

    def to_dict(self) -> Dict[str, Any]:
        attributes_dict = {
            'faultsDict': self.faults_df.to_json(orient='records'),
            'interroDict': self.interro_df.to_json(orient='records'),
            'oldInterroDict': self.old_interro_df.to_json(orient='records'),
            'testIndex': self.index,
            'testLength': self.test_length,
        }
        return attributes_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rattrap':
        interro_df = pd.DataFrame(data['interroDict'])
        old_interro_df = pd.DataFrame(data['oldInterroDict'])
        guesser = FastapiGuesser()
        instance = cls(
            interro_df=interro_df,
            guesser=guesser,
            old_interro_df=old_interro_df
        )
        instance.test_length = data['testLength']
        instance.faults_df = pd.DataFrame(data['faultsDict'])
        instance.index = data['testIndex']
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
        self.criteria: Dict[str, float] = {}
        self.set_criteria()
        self.db_manipulator = DbManipulator(
            loader.data_querier.user_name,
            loader.data_querier.db_name,
            loader.data_querier.test_type,
        )

    def update_words(self):
        """
        Update words table with the interro results.
        """
        for idx in self.interro.interro_df.index:
            row = list(self.interro.interro_df.loc[idx])
            self.loader.words_df.loc[idx] = row
        logger.info(f"Table {self.loader.data_querier.db_name} updated!")

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
        self.loader.words_df['img_good'] = ord_good + steep_good * self.loader.words_df['nb']
        self.good_words_df = self.loader.words_df[
            self.loader.words_df['taux'] >= self.loader.words_df['img_good']
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

    def delete_good_words(self):
        """
        Remove words that have been guessed sufficiently enough.
        This \'sufficiently\' criteria is totally arbitrary, and can be changed
        only under the author's dictatorial will.
        """
        self.loader.words_df = self.loader.words_df[
            self.loader.words_df['taux'] < self.loader.words_df['img_good']
        ]
        self.loader.words_df = self.loader.words_df.drop('img_good', axis=1)

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

    def save_words(self):
        """
        1) Reset the index of words dataframe.
        2) Use data handler instance to save the table in the database.
        """
        self.loader.words_df.reset_index(inplace=True)
        self.db_manipulator.save_table(
            table_name=self.loader.test_type + '_voc',
            table=self.loader.words_df
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
            index=[self.loader.perf_df.shape[0] + 1]
        )
        self.loader.perf_df = pd.concat([self.loader.perf_df, new_row])
        self.loader.perf_df.reset_index(inplace=True, names=['id_test'])
        self.db_manipulator.save_table(
            table_name=self.loader.test_type + '_perf',
            table=self.loader.perf_df
        )

    def save_words_count(self):
        """
        1)
        """
        def correct_words_count_df():
            """
            Correct the words count dataframe.
            """
            real_columns = set(self.loader.words_count_df.columns)
            expected_columns = {'test_date', 'nb'}
            if real_columns != expected_columns:
                self.loader.words_count_df.reset_index(inplace=True)

        count_before = self.loader.words_count_df.shape[0]
        new_row = pd.DataFrame(
            data={
                'test_date': datetime.today().date().strftime('%Y-%m-%d'),
                'nb': self.loader.words_df.shape[0]
            },
            index=[count_before]
        )
        correct_words_count_df()
        self.loader.words_count_df = pd.concat([
            self.loader.words_count_df,
            new_row
        ])
        self.loader.words_count_df.sort_index(inplace=True)
        self.db_manipulator.save_table(
            table_name=self.loader.test_type + '_words_count',
            table=self.loader.words_count_df
        )

    def update_data(self):
        """
        Main method of Updater class
        """
        self.update_words()
        self.move_good_words()
        self.loader.flag_bad_words()
        self.save_words()
        self.save_performances()
        self.save_words_count()



def complete_columns(
        df_1: pd.DataFrame,
        df_2: pd.DataFrame
    ) -> pd.DataFrame:
    """
    Guarantee that the well_known_words dataframe contains exactly
    the columns of the output dataframe
    """
    missing_columns = set(df_1.columns).difference(set(df_2.columns))
    for column in missing_columns:
        df_2[column] = [0] * df_2.shape[0]
    return df_2
