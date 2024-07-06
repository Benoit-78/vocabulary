"""
    Creator:
        B.Delorme
    Creation date:
        11th March 2023
    Main purpose:
        Test script for interro.py, main script of vocabulary application
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro
from src.views import terminal as view_terminal
from src.data import database_interface



class TestLoader(unittest.TestCase):
    """
    The Loader class should interact with database interfaces,
    such as csv handler or MariaDB handler.
    """
    @patch('src.data.database_interface.check_test_type')
    def setUp(self, mock_check_test_type):
        mock_check_test_type.side_effect = lambda **kwargs: kwargs['test_type']
        self.test_type = 'version'
        self.data_querier = database_interface.DbQuerier(
            user_name='mock_user_name',
            db_name='mock_db_name',
            test_type=self.test_type
        )
        self.loader = interro.Loader(
            words=10,
            data_querier=self.data_querier
        )

    def test_init(self):
        """
        Test the constructor.
        """
        # ----- ARRANGE
        # ----- ACT
        # ----- ASSERT
        self.assertEqual(hasattr(self.loader, 'test_type'), True)
        self.assertEqual(hasattr(self.loader, 'data_querier'), True)
        self.assertEqual(hasattr(self.loader, 'tables'), True)
        self.assertEqual(hasattr(self.loader, 'output_table'), True)
        self.assertEqual(self.loader.test_type, self.test_type)
        self.assertEqual(self.loader.data_querier, self.data_querier)
        self.assertEqual(self.loader.tables, {})
        self.assertEqual(self.loader.output_table, '')

    def test_adjust_test_length(self):
        """
        Test adjust_test_length function
        """
        # ----- ARRANGE
        words_table = pd.DataFrame({
            'some_column': [1, 2, 3, 4, 5],
        })
        self.loader.test_type = 'test_type'
        self.loader.tables = {'test_type_voc': words_table}
        # ----- ACT
        self.loader.adjust_test_length()
        # ----- ASSERT
        self.assertEqual(self.loader.words, 5)

    def test_adjust_test_length_small_table(self):
        """
        Test adjust_test_length function
        """
        # ----- ARRANGE
        words_table = pd.DataFrame(
            {
                'some_column': ['value_1', 'value_2', 'value_3'],
            }
        )
        self.loader.test_type = 'test_type'
        self.loader.tables = {
            'test_type_voc': words_table
        }
        # ----- ACT
        self.loader.adjust_test_length()
        # ----- ASSERT
        self.assertEqual(self.loader.words, 3)

    def test_adjust_test_length_empty_table(self):
        """
        Test adjust_test_length function
        """
        # ----- ARRANGE
        words_table = pd.DataFrame()
        self.loader.test_type = 'test_type'
        self.loader.tables = {
            'test_type_voc': words_table
        }
        # ----- ACT
        # ----- ASSERT
        with self.assertRaises(ValueError):
            self.loader.adjust_test_length()

    def test_get_random_step(self):
        """
        The step should be a random integer smaller than the size
        of the original words table.
        """
        # ----- ARRANGE
        self.loader.words_df = pd.DataFrame({
            'some_column': [1, 2, 3, 4, 5],
        })
        # ----- ACT
        result = self.loader.get_random_step()
        # ----- ASSERT
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
        self.assertLess(result, self.loader.words_df.shape[0] + 1)

    @patch('src.interro.random.randint')
    def test_get_another_index_bis(self, mock_randint):
        """
        This function should provide with a new index, corresponding to a new word.
        The new word should not have been already asked within the current test.
        """
        # ----- ARRANGE
        mock_randint.side_effect = [1, 2]
        self.loader.words_df = pd.DataFrame({
            'query': [0, 1, 0]
        })
        # ----- ACT
        next_index = self.loader.get_another_index()
        # ----- ASSERT
        self.assertEqual(next_index, 2)
        self.loader.words_df = pd.DataFrame({
            'query': [0, 1, 1]
        })
        mock_randint.call_count = 2

    @patch('src.interro.Loader.get_another_index')
    def test_get_next_index_if_not_bad_word(self, mock_get_another_index):
        """
        When the next index points to a bad word, the search should run once again.
        So the index search method should be called twice.
        """
        # ----- ARRANGE
        self.loader.words_df = pd.DataFrame(
            {
                'english': ['Hello', 'One', 'Two', 'Three', 'Four', 'Five'],
                'français': ['Bonjour', 'Un', 'Deux', 'Trois', 'Quatre', 'Cinq'],
                'bad_word': [0, 0, 0, 0, 0, 1],
                'query': [0, 0, 0, 0, 0, 0]
            }
        )
        mock_get_another_index.return_value = 3
        # ----- ACT
        next_index = self.loader.get_next_index()
        # ----- ASSERT
        self.assertEqual(next_index, 3)
        assert mock_get_another_index.call_count == 2
        self.assertEqual(self.loader.words_df['query'].loc[next_index], 0)

    @patch('src.interro.Loader.get_another_index')
    def test_get_next_index_if_bad_word(self, mock_get_another_index):
        """
        When the next index points to a bad word, the search should stop.
        So the index search method should be called once.
        """
        # Arrange
        self.loader.words_df = pd.DataFrame(
            {
                'english': ['Hello', 'One', 'Two', 'Three', 'Four', 'Five'],
                'français': ['Bonjour', 'Un', 'Deux', 'Trois', 'Quatre', 'Cinq'],
                'bad_word': [0, 0, 0, 0, 1, 0],
                'query': [0, 0, 0, 0, 0, 0]
            }
        )
        mock_get_another_index.return_value = 4
        # Act
        next_index = self.loader.get_next_index()
        # Assert
        self.assertEqual(next_index, 4)
        assert mock_get_another_index.call_count == 1

    @patch('src.interro.Loader.get_row')
    @patch('src.interro.Loader.get_next_index')
    @patch('src.interro.Loader.get_random_step')
    @patch('src.interro.Loader.adjust_test_length')
    def test_set_interro_df(
            self,
            mock_adjust_test_length,
            mock_create_random_step,
            mock_get_next_index,
            mock_get_row
        ):
        """
        A dataframe of words should be formed, that will be asked to the user
        """
        # ----- ARRANGE
        mock_create_random_step.return_value = True
        self.loader.words = 1
        self.loader.step = 23
        mock_get_next_index.return_value = 6
        self.loader.row = [0, 'Hello', 'Bonjour']
        mock_get_row.return_value = [
            0, ['Hello', 'Bonjour', "2024-01-01", 0, 0, 0, 0, 0]
        ]
        # ----- ACT
        self.loader.set_interro_df()
        # ----- ASSERT
        self.assertEqual(self.loader.index, 6)
        mock_adjust_test_length.assert_called_once()
        mock_create_random_step.assert_called_once()
        mock_get_next_index.assert_called_once()

    @patch('src.data.database_interface.DbQuerier.get_tables')
    def test_load_tables(self, mock_get_tables):
        """
        Input should be a dataframe, and it should be added a query column.
        """
        # ----- ARRANGE
        mock_get_tables.return_value = {
            self.loader.test_type + '_voc': pd.DataFrame({
                'creation_date': ['2022-01-01', '2022-02-01'],
                'taux': [0.5, 0.34],
                'bad_word': [0, 1]
            }),
            self.loader.test_type + '_perf': pd.DataFrame({
                'some_col_1': ['some_value_1']
            }),
            self.loader.test_type + '_words_count': pd.DataFrame({
                'some_col_2': ['some_value_2']
            }),
        }
        # ----- ACT
        self.loader.load_tables()
        # ----- ASSERT
        mock_get_tables.assert_called_once()
        self.assertIsInstance(self.loader.tables, dict)
        self.assertIsInstance(
            self.loader.tables[self.loader.test_type + '_voc'],
            pd.core.frame.DataFrame
        )
        self.assertIn('bad_word', self.loader.tables[self.loader.test_type + '_voc'].columns)
        pd.testing.assert_frame_equal(
            self.loader.perf_df,
            pd.DataFrame({'some_col_1': ['some_value_1']}),
        )
        pd.testing.assert_frame_equal(
            self.loader.words_count_df,
            pd.DataFrame({'some_col_2': ['some_value_2']}),
        )



class TestPremierTest(unittest.TestCase):
    """
    The Interro class represents the concept of a test taken by the user.
    It should then be abstract.
    """
    @classmethod
    @patch('src.data.database_interface.check_test_type')
    def setUpClass(cls, mock_check_test_type):
        """
        Run once before all tests
        """
        mock_check_test_type.side_effect = lambda **kwargs: kwargs['test_type']
        cls.data_querier_1 = database_interface.DbQuerier(
            user_name='test_user',
            db_name='test_db',
            test_type='test_type'
        )
        cls.loader_1 = interro.Loader(
            words=10,
            data_querier=cls.data_querier_1
        )

    def setUp(self):
        df = pd.DataFrame(columns=['english', 'français'])
        df.loc[df.shape[0]] = ['Hello', 'Bonjour']
        df.loc[df.shape[0]] = ['One', 'Un']
        df.loc[df.shape[0]] = ['Two', 'Deux']
        df.loc[df.shape[0]] = ['Three', 'Trois']
        df.loc[df.shape[0]] = ['Four', 'Quatre']
        df.loc[df.shape[0]] = ['Cinq', 'Cinq']
        df.loc[df.shape[0]] = ['Six', 'Six']
        df.loc[df.shape[0]] = ['Seven', 'Sept']
        df.loc[df.shape[0]] = ['Eight', 'Huit']
        df.loc[df.shape[0]] = ['Nine', 'Neuf']
        df.loc[df.shape[0]] = ['Ten', 'Dix']
        df['query'] = [0] * df.shape[0]
        df['nb'] = [0] * df.shape[0]
        df['score'] = [0] * df.shape[0]
        df['taux'] = [0] * df.shape[0]
        df['bad_word'] = [0] * df.shape[0]
        self.loader_1.tables = {}
        words = df.shape[0] //  2
        self.loader_1.tables['version_voc'] = df
        guesser = view_terminal.CliGuesser()
        self.interro_1 = interro.PremierTest(
            self.loader_1.tables['version_voc'],
            words,
            guesser
        )
        self.interro_1.step = 1

    def test_update_faults_df(self):
        """
        The Test class should save the words not guessed by the user,
        so that those words can be asked again.
        """
        # Arrange
        word_guessed = False
        row = ['Hello', 'Bonjour']
        shape_before = self.interro_1.faults_df.shape[0]
        # Act
        self.interro_1.update_faults_df(word_guessed, row)
        # Assert
        shape_after = self.interro_1.faults_df.shape[0]
        self.assertEqual(shape_before, shape_after - 1)
        new_length = self.interro_1.faults_df.shape[0] - 1
        last_row = self.interro_1.faults_df.loc[new_length]
        self.assertEqual(list(last_row)[-2:], row)

    def test_update_interro_df_success(self):
        """
        After the guess (or the non-guess, if the user is not very very smart),
        the word should be updated on number of queries, number of guesses, ...
        """
        # Arrange
        old_row = self.interro_1.interro_df.loc[self.interro_1.index]
        word_guessed = True
        # Act
        self.interro_1.update_interro_df(word_guessed)
        new_row = self.interro_1.interro_df.loc[self.interro_1.index]
        # Assert
        self.assertEqual(new_row['nb'], old_row['nb'] + 1)
        self.assertEqual(new_row['score'], old_row['score'] + 1)
        self.assertGreater(new_row['taux'], old_row['taux'])
        self.assertEqual(new_row['query'], old_row['query'] + 1)

    def test_update_interro_df_failure(self):
        """
        After the guess (or the non-guess, if the user is not very very smart),
        the word should be updated on number of queries, number of guesses, ...
        """
        # Arrange
        old_row = self.interro_1.interro_df.loc[self.interro_1.index]
        word_guessed = False
        # Act
        self.interro_1.update_interro_df(word_guessed)
        new_row = self.interro_1.interro_df.loc[self.interro_1.index]
        # Assert
        self.assertEqual(new_row['nb'], old_row['nb'] + 1)
        self.assertEqual(new_row['score'], old_row['score'] - 1)
        self.assertLess(new_row['taux'], old_row['taux'])
        self.assertEqual(new_row['query'], old_row['query'] + 1)

    def test_compute_success_rate(self):
        """Based on the user's guesses and the umber of words asked, a success rate is computed."""
        # Arrange
        self.interro_1.faults_df.loc[self.interro_1.faults_df.shape[0]] = ['Yes', 'Oui']
        self.interro_1.faults_df.loc[self.interro_1.faults_df.shape[0]] = ['No', 'Non']
        self.interro_1.faults_df.loc[self.interro_1.faults_df.shape[0]] = ['Maybe', 'Peut-être']
        # Act
        self.interro_1.compute_success_rate()
        # Assert
        self.assertIsInstance(self.interro_1.perf, int)
        self.assertLess(self.interro_1.perf, 101)
        self.assertGreater(self.interro_1.perf, -1)



class TestRattrap(unittest.TestCase):
    """
    Tests on Rattrap class methods.
    """
    def setUp(self):
        self.faults_df = pd.DataFrame({
            'english': [1, 2, 3],
            'français': [4, 5, 6]
        })
        self.guesser = MagicMock()
        self.rattrap = interro.Rattrap(
            interro_df=self.faults_df,
            guesser=self.guesser,
            old_interro_df=pd.DataFrame()
        )

    @patch('src.interro.Interro.__init__')
    def test_init(self, mock_interro_init):
        """
        The constructor should create a Rattrap object.
        """
        # ----- ARRANGE
        interro_df = pd.DataFrame({
            'english': [1, 2, 3],
            'français': [4, 5, 6]
        })
        self.guesser = 'mock_guesser'
        # ----- ACT
        self.rattrap = interro.Rattrap(
            interro_df=interro_df,
            guesser=self.guesser,
            old_interro_df=pd.DataFrame()
        )
        # ----- ASSERT
        mock_interro_init.assert_called_once_with(
            interro_df=interro_df,
            words=3,
            guesser='mock_guesser'
        )
        self.assertEqual(hasattr(self.rattrap, 'rattrap'), True)
        self.assertEqual(hasattr(self.rattrap, 'old_interro_df'), True)
        self.assertEqual(self.rattrap.rattrap, True)
        pd.testing.assert_frame_equal(
            self.rattrap.old_interro_df,
            pd.DataFrame()
        )



class TestUpdater(unittest.TestCase):
    """
    Should save the user's guesses in the database,
    after having processed the dataset so as to: 
    - flag bad words;
    - and remove good words.
    """
    def setUp(self):
        self.data_querier_1 = database_interface.DbQuerier(
            user_name='test_user',
            db_name='test_db',
            test_type='version'
        )
        words = 10
        self.loader_1 = interro.Loader(
            words=words,
            data_querier=self.data_querier_1
        )
        self.loader_1.tables = {
            'version_voc': pd.DataFrame(
                columns=[
                    'id_word',
                    'english',
                    'français',
                    'creation_date',
                    'nb',
                    'score',
                    'taux'
                ]
            ),
            'version_perf': pd.DataFrame(
                columns=[
                    'id_test',
                    'test_date',
                    'test'
                ]
            ),
            'version_words_count': pd.DataFrame(
                columns=[
                    'id_test',
                    'test_date',
                    'words_count'
                ]
            ),
            'output': pd.DataFrame(
                columns=[
                    'id_word',
                    'english',
                    'français',
                    'creation_date',
                    'nb',
                    'score',
                    'taux'
                ]
            )
        }
        df = pd.DataFrame({
            'english':
            [
                'Hello', 'One', 'Two', 'Three', 'Four', 'Five',
                'Six', 'Seven', 'Eight', 'Nine', 'Ten'
            ],
            'français':
            [
                'Bonjour', 'Un', 'Deux', 'Trois', 'Quatre', 'Cinq',
                'Six', 'Sept', 'Huit', 'Neuf', 'Dix'
            ]
        })
        df['query'] = [0] * df.shape[0]
        df['nb'] = [0] * df.shape[0]
        df['score'] = [0] * df.shape[0]
        df['taux'] = [0] * df.shape[0]
        df['bad_word'] = [0] * df.shape[0]
        df['img_good'] = [0] * df.shape[0]
        self.loader_1.tables['version_voc'] = df
        self.guesser = view_terminal.CliGuesser()
        self.interro_1 = interro.PremierTest(
            interro_df=self.loader_1.tables['version_voc'],
            words=words,
            guesser=self.guesser,
        )
        self.updater_1 = interro.Updater(
            self.loader_1,
            self.interro_1
        )

    def test_set_good_words(self):
        """
        Should flag the words that have been guessed sufficiently enough.
        """
        # Arrange
        if 'img_good' in self.updater_1.interro.interro_df.columns:
            self.updater_1.interro.interro_df.drop('img_good', axis=1, inplace=True)
        old_columns = list(self.updater_1.interro.interro_df.columns)
        self.loader_1.words_df = self.loader_1.tables['version_voc']
        # Act
        self.updater_1.set_good_words()
        # Assert
        new_columns = list(self.updater_1.interro.interro_df.columns)
        self.assertIn('img_good', new_columns)
        self.assertEqual(len(new_columns), len(old_columns) + 1)
        self.assertIsInstance(self.updater_1.good_words_df, pd.DataFrame)

    def test_copy_good_words(self):
        """
        Should copy the well good words in the output table.
        """
        # Arrange
        good_words_df = pd.DataFrame(columns=['english', 'français', 'creation_date'])
        good_words_df.loc[good_words_df.shape[0]] = ['One', 'Un', '2023-01-01']
        good_words_df.loc[good_words_df.shape[0]] = ['Two', 'Deux', '2023-02-01']
        good_words_df.loc[good_words_df.shape[0]] = ['Three', 'Trois', '2023-03-01']
        self.updater_1.good_words_df = good_words_df
        good_words = self.updater_1.good_words_df.shape[0]
        old_output_shape = self.loader_1.tables['output'].shape
        # Act
        self.updater_1.copy_good_words()
        # Assert
        new_output_shape = self.loader_1.tables['output'].shape
        self.assertEqual(new_output_shape[0], old_output_shape[0] + good_words)

    def test_delete_good_words(self):
        """Should remove good words from the table of to-be-guessed words."""
        # Arrange
        self.updater_1.loader.words_df = pd.DataFrame({
            'taux': [0.5, 0.34],
            'img_good': [0, 1],
        })
        old_shape = self.updater_1.loader.words_df.shape
        # Act
        self.updater_1.delete_good_words()
        # Assert
        new_shape = self.updater_1.loader.words_df.shape
        self.assertLessEqual(new_shape[0], old_shape[0])
        self.assertEqual(new_shape[1], old_shape[1] - 1)
        self.assertNotIn('img_good', self.updater_1.loader.words_df.columns)

    @patch('src.interro.Updater.delete_good_words')
    @patch('src.interro.DbManipulator.save_table')
    @patch('src.interro.Updater.copy_good_words')
    @patch('src.interro.Updater.set_good_words')
    def test_move_good_words(
            self,
            mock_set_good_words,
            mock_copy_good_words,
            mock_save_table,
            mock_delete_good_words,
        ):
        """
        Should move the words that have been guessed sufficiently enough
        from one table to its output.
        """
        # Arrange
        mock_set_good_words.return_value = True
        mock_copy_good_words.return_value = True
        self.updater_1.loader.tables['output'] = MagicMock()
        mock_save_table.retuirn_value = True
        mock_delete_good_words.return_value = True
        # Act
        self.updater_1.move_good_words()
        # Assert
        mock_set_good_words.assert_called_once()
        mock_copy_good_words.assert_called_once()
        self.updater_1.loader.tables['output'].reset_index.assert_called_once()
        mock_save_table.assert_called_once_with(
            table_name='output',
            table=self.updater_1.loader.tables['output']
        )
        mock_delete_good_words.assert_called_once()

    def test_flag_bad_words(self):
        """Should flag bad words, i.e. words rarely guessed by the user."""
        # ----- ARRANGE
        self.updater_1.loader.words_df = pd.DataFrame({
            'test_date': ['2022-01-01', '2022-02-01'],
            'nb': [1876, 2341],
            'taux': [0.5, 0.34],
        })
        old_length, old_width = self.updater_1.loader.words_df.shape
        # ----- ACT
        self.updater_1.flag_bad_words()
        # ----- ASSERT
        new_length, new_width = self.updater_1.loader.words_df.shape
        first_word = self.updater_1.loader.words_df.iloc[0]
        ord_bad = self.updater_1.criteria['ORD_BAD']
        steep_bad = self.updater_1.criteria['STEEP_BAD']
        img_bad = ord_bad + steep_bad * first_word['nb']
        self.assertLessEqual(new_length, old_length)
        self.assertEqual(new_width, old_width +1)
        if first_word['bad_word'] == 1:
            self.assertLess(first_word['taux'], img_bad) # strictly less
        elif first_word['bad_word'] == 0:
            self.assertGreaterEqual(first_word['taux'], img_bad) # greater or equal

    @patch('src.data.database_interface.DbManipulator.save_table')
    def test_save_words(self, mock_save_table):
        """
        Prepare the words table for saving, and save it.
        """
        # ----- ARRANGE
        self.updater_1.loader.words_count_df = pd.DataFrame({
            'test_date': ['2022-01-01', '2022-02-01'],
            'nb': [1876, 2341]
        })
        old_width = self.updater_1.loader.words_df.shape[1]
        # ----- ACT
        self.updater_1.save_words()
        # ----- ASSERT
        new_width = self.updater_1.loader.words_df.shape[1]
        self.assertEqual(new_width, old_width + 1)
        mock_save_table.assert_called_once_with(
            table_name=self.updater_1.loader.test_type + '_voc',
            table=self.updater_1.loader.words_df
        )

    @patch('src.data.database_interface.DbManipulator.save_table')
    def test_save_performances(self, mock_save_table):
        """
        Save performances for further analysis.
        """
        # Arrange
        perf_df = pd.DataFrame(columns=['test_date', 'test'])
        perf_df.loc[perf_df.shape[0]] = ["2022-01-01", 65]
        perf_df.loc[perf_df.shape[0]] = ["2022-02-01", 75]
        perf_df.loc[perf_df.shape[0]] = ["2022-03-01", 85]
        perf_df.loc[perf_df.shape[0]] = ["2022-04-01", 0]
        self.updater_1.loader.perf_df = perf_df
        old_shape = self.updater_1.loader.perf_df.shape
        mock_save_table.return_value = True
        # Act
        self.updater_1.save_performances()
        new_shape = self.updater_1.loader.perf_df.shape
        # Assert
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        self.assertEqual(new_shape[1], old_shape[1] + 1)
        mock_save_table.assert_called_once_with(
            table_name=self.updater_1.loader.test_type + '_perf',
            table=self.updater_1.loader.perf_df
        )
        last_perf = self.updater_1.loader.perf_df.loc[
            self.updater_1.loader.perf_df.shape[0] - 1
        ]
        last_perf = last_perf['test']
        self.assertEqual(last_perf, self.updater_1.interro.perf)

    @patch('src.data.database_interface.DbManipulator.save_table')
    def test_save_words_count(self, mock_save_table):
        """
        Save the number of words recorded on the current date.
        """
        # ----- ARRANGE
        self.updater_1.loader.words_count_df = pd.DataFrame({
            'test_date': ['2022-01-01', '2022-02-01'],
            'nb': [1876, 2341]
        })
        old_shape = self.updater_1.loader.words_count_df.shape
        # ----- ACT
        self.updater_1.save_words_count()
        # ----- ASSERT
        new_shape = self.updater_1.loader.words_count_df.shape
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        self.assertEqual(new_shape[1], old_shape[1])
        mock_save_table.assert_called_once_with(
            table_name=self.updater_1.loader.test_type + '_words_count',
            table=self.updater_1.loader.words_count_df
        )
        last_count = self.updater_1.loader.words_count_df.loc[
            self.updater_1.loader.words_count_df.shape[0] - 1
        ]
        last_count = last_count['nb']
        self.assertEqual(last_count, self.updater_1.loader.interro_df.shape[0])

    @patch('src.data.database_interface.DbManipulator.save_table')
    def test_save_words_count_reset_index(self, mock_save_table):
        """
        Save the number of words recorded on the current date.
        """
        # ----- ARRANGE
        self.updater_1.loader.words_count_df = pd.DataFrame({
            'test_date': ['2022-01-01', '2022-02-01'],
            'nb': [1876, 2341],
            'other_column': ['mock_value1', 'mock_value2']
        })
        self.updater_1.loader.words_count_df.set_index('test_date', inplace=True)
        old_shape = self.updater_1.loader.words_count_df.shape
        # ----- ACT
        self.updater_1.save_words_count()
        # ----- ASSERT
        new_shape = self.updater_1.loader.words_count_df.shape
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        self.assertEqual(new_shape[1], old_shape[1] + 1)
        mock_save_table.assert_called_once_with(
            table_name=self.updater_1.loader.test_type + '_words_count',
            table=self.updater_1.loader.words_count_df
        )
        last_count = self.updater_1.loader.words_count_df.loc[
            self.updater_1.loader.words_count_df.shape[0] - 1
        ]
        last_count = last_count['nb']
        self.assertEqual(last_count, self.updater_1.loader.interro_df.shape[0])

    @patch.object(interro.Updater, 'move_good_words')
    @patch.object(interro.Updater, 'flag_bad_words')
    @patch.object(interro.Updater, 'save_words')
    @patch.object(interro.Updater, 'save_performances')
    @patch.object(interro.Updater, 'save_words_count')
    @patch.object(interro.Updater, 'update_words')
    def test_update_data(
        self,
        mock_update_words,
        mock_save_words_count,
        mock_save_performances,
        mock_save_words,
        mock_flag_bad_words,
        mock_move_good_words):
        """
        Should move good words, flag bad words,
        save the table as well as performances & words count.
        """
        # Act
        self.updater_1.update_data()
        # Assert
        mock_update_words.assert_called_once()
        mock_move_good_words.assert_called_once()
        mock_flag_bad_words.assert_called_once()
        mock_save_words.assert_called_once()
        mock_save_performances.assert_called_once()
        mock_save_words_count.assert_called_once()



class TestUtils(unittest.TestCase):
    """
    Methods that tests functions of data module.
    """
    def test_complete_columns(self):
        """
        Guarantee that the well_known_words dataframe contains exactly 
        the columns of the output dataframe.
        """
        # ----- ARRANGE
        df_1 = pd.DataFrame(columns=['col1', 'col2', 'col3'])
        df_2 = pd.DataFrame(columns=['col1', 'col4'])
        # ----- ACT
        df_1 = interro.complete_columns(df_1, df_2)
        # ----- ASSERT
        self.assertIn('col4', df_1)
