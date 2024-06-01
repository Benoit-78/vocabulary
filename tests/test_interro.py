"""
    Creator:
        B.Delorme
    Creation date:
        11th March 2023
    Main purpose:
        Test script for interro.py, main script of vocabulary application
"""

import argparse
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



class TestCliUser(unittest.TestCase):
    """
    Tests on arguments parser.
    """
    def setUp(self):
        self.user = interro.CliUser()

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments_default(self, mock_parse_args):
        """
        The method should store three arguments.
        """
        # ----- ARRANGE
        args = []
        # ----- ACT
        self.user.parse_arguments(args)
        # ----- ASSERT
        mock_parse_args.assert_called_with(
            [
                '-t', 'version',
                '-w', '10',
                '-r', '2'
            ]
        )

    @patch('argparse.ArgumentParser.parse_args')
    def test_arguments_all(self, mock_parse_args):
        """
        Test case 1: Valid arguments provided
        """
        # ----- ARRANGE
        args = [
            '--type', 'version',
            '--words', '100',
            '--rattraps', '1'
        ]
        # ----- ACT
        self.user.parse_arguments(args)
        # ----- ASSERT
        mock_parse_args.assert_called_with(
            [
                '--type', 'version',
                '--words', '100',
                '--rattraps', '1',
                '-t', 'version',
                '-w', '10',
                '-r', '2'
            ]
        )

    @patch('argparse.ArgumentParser.parse_args')
    def test_arguments_required_only(self, mock_parse_args):
        """
        Test case 2: Only required argument provided
        """
        # ----- ARRANGE
        args = ['-t', 'theme']
        # ----- ACT
        self.user.parse_arguments(args)
        # ----- ASSERT
        mock_parse_args.assert_called_with(
            [
                '-t', 'theme',
                '-w', '10',
                '-r', '2'
            ]
        )

    @patch('src.interro.sys.argv', ['interro.py', '-t', '', '-w', '100', '-r', '1'])
    @patch('src.interro.logger')
    def test_get_settings_error_1(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        message = ' '.join([
            "Please give",
            "-t <test type>, ",
            "-w <number of words> and ",
            "-r <number of rattraps>"
        ])
        mock_logger.error.assert_called_with(message)

    @patch('src.interro.sys.argv', ['interro.py', '-t', 'mock_type', '-w', '100', '-r', '1'])
    @patch('src.interro.logger')
    def test_get_settings_error_2(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        mock_logger.error.assert_called_with("Test type must be either version or theme")

    @patch('src.interro.sys.argv', ['interro.py', '-t', 'version', '-w', '100', '-r', '-2'])
    @patch('src.interro.logger')
    def test_get_settings_rattraps_negative(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        mock_logger.error.assert_called_with(
            "Number of rattraps must be greater than -1."
        )

    @patch('src.interro.sys.argv', ['interro.py', '-t', 'version', '-w', '-100', '-r', '1'])
    @patch('src.interro.logger')
    def test_get_settings_words_negative(self, mock_logger):
        # ----- ARRANGE
        # ----- ACT
        with self.assertRaises(SystemExit):
            self.user.get_settings()
        # ----- ASSERT
        mock_logger.error.assert_called_with(
            "Number of words must be greater than 0."
        )



class TestLoader(unittest.TestCase):
    """
    The Loader class should interact with database interfaces,
    such as csv handler or MariaDB handler.
    """
    @patch('src.data.database_interface.check_test_type')
    def setUp(self, mock_check_test_type):
        mock_check_test_type.side_effect = lambda arg1: arg1
        self.test_type = 'mock_test_type'
        self.data_querier = database_interface.DbQuerier(
            user_name='mock_user_name',
            db_name='mock_db_name',
            test_type=self.test_type
        )
        self.loader = interro.Loader(self.data_querier)

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

    @patch('src.data.database_interface.DbQuerier.get_tables')
    def test_load_tables(self, mock_get_tables):
        """
        Input should be a dataframe, and it should be added a query column.
        """
        # ----- ARRANGE
        voc = self.loader.test_type + '_voc'
        mock_get_tables.return_value = {
            voc: pd.DataFrame({
                'creation_date': ['2022-01-01', '2022-02-01'],
                'taux': [0.5, 0.34],
                'bad_word': [0, 1]
            })
        }
        # ----- ACT
        self.loader.load_tables()
        # ----- ASSERT
        for table in self.loader.tables.values():
            self.assertIn('creation_date', list(table.columns))
            self.assertIn('query', list(table.columns))
            self.assertEqual(table['taux'].dtype, np.float64)
            self.assertGreater(table.shape[0], 1)

    @patch('src.data.database_interface.DbQuerier.get_tables')
    def test_load_tables_no_bad_word_column(self, mock_get_tables):
        """
        Input should be a dataframe, and it should be added a query column.
        """
        # ----- ARRANGE
        voc = self.loader.test_type + '_voc'
        mock_get_tables.return_value = {
            voc: pd.DataFrame({
                'creation_date': ['2022-01-01', '2022-02-01'],
                'taux': [0.5, 0.34],
            })
        }
        # ----- ACT
        self.loader.load_tables()
        # ----- ASSERT
        for table in self.loader.tables.values():
            self.assertIn('bad_word', list(table.columns))



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
        mock_check_test_type.side_effect = lambda arg1: arg1
        cls.user_1 = interro.CliUser()
        cls.user_1.parse_arguments(['-t', 'version'])
        cls.data_querier_1 = database_interface.DbQuerier(
            user_name='test_user',
            db_name='test_db',
            test_type='test_type'
        )
        cls.loader_1 = interro.Loader(cls.data_querier_1)

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

    def test_set_row(self):
        """
        The row should contain all what is necessary for the user to:
        1) get a word and guess it;
        2) check if its guess was correct.
        """
        # Act
        self.interro_1.set_row()
        # Assert
        self.assertIsInstance(self.interro_1.row, list)
        self.assertEqual(len(self.interro_1.row), 3)
        self.assertIsInstance(self.interro_1.row[1], str)
        self.assertIsInstance(self.interro_1.row[2], str)

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

    def test_create_random_step(self):
        """The step should be a random integer smaller than the ."""
        # Act
        self.interro_1.create_random_step()
        # Assert
        self.assertIsInstance(self.interro_1.step, int)
        self.assertGreater(self.interro_1.step, 0)
        self.assertLess(self.interro_1.step, self.interro_1.words_df.shape[0] + 1)

    @patch('src.interro.random.randint')
    def test_get_another_index_bis(self, mock_randint):
        """
        This function should provide with a new index, corresponding to a new word.
        The new word should not have been already asked within the current test.
        """
        # ----- ARRANGE
        mock_randint.side_effect = [1, 2]
        self.interro_1.words_df = pd.DataFrame({
            'query': [0, 1, 0]
        })
        # ----- ACT
        next_index = self.interro_1.get_another_index()
        # ----- ASSERT
        self.assertEqual(next_index, 2)
        self.interro_1.words_df = pd.DataFrame({
            'query': [0, 1, 1]
        })
        mock_randint.call_count = 2

    @patch('src.interro.PremierTest.get_another_index')
    def test_get_next_index_if_not_bad_word(self, mock_get_another_index):
        """
        When the next index points to a bad word, the search should run once again.
        So the index search method should be called twice.
        """
        # ----- ARRANGE
        mock_get_another_index.return_value = 3
        # ----- ACT
        next_index = self.interro_1.get_next_index()
        # ----- ASSERT
        self.assertEqual(next_index, 3)
        assert mock_get_another_index.call_count == 2
        self.assertEqual(self.interro_1.words_df['query'].loc[next_index], 0)

    @patch('src.interro.PremierTest.get_another_index')
    def test_get_next_index_if_bad_word(self, mock_get_another_index):
        """
        When the next index points to a bad word, the search should stop.
        So the index search method should be called once.
        """
        # Arrange
        self.interro_1.words_df['bad_word'] = [1] * self.interro_1.words_df.shape[0]
        mock_get_another_index.return_value = 4
        # Act
        next_index = self.interro_1.get_next_index()
        # Assert
        self.assertEqual(next_index, 4)
        assert mock_get_another_index.call_count == 1

    @patch('src.interro.PremierTest.set_row')
    @patch('src.interro.PremierTest.get_next_index')
    @patch('src.interro.PremierTest.create_random_step')
    def test_set_interro_df(
            self,
            mock_create_random_step,
            mock_get_next_index,
            mock_set_row
        ):
        """
        A dataframe of words should be formed, that will be asked to the user
        """
        # ----- ARRANGE
        mock_create_random_step.return_value = True
        self.interro_1.words = 1
        self.interro_1.step = 23
        mock_get_next_index.return_value = 6
        mock_set_row.return_value = True
        self.interro_1.row = [0, 'Hello', 'Bonjour']
        # ----- ACT
        self.interro_1.set_interro_df()
        # ----- ASSERT
        self.assertEqual(self.interro_1.index, 6)
        mock_create_random_step.assert_called_once()
        mock_get_next_index.assert_called_once()
        mock_set_row.assert_called_once()

    def test_update_voc_df_success(self):
        """
        After the guess (or the non-guess, if the user is not very very smart),
        the word should be updated on number of queries, number of guesses, ...
        """
        # Arrange
        old_row = self.interro_1.words_df.loc[self.interro_1.index]
        word_guessed = True
        # Act
        self.interro_1.update_voc_df(word_guessed)
        new_row = self.interro_1.words_df.loc[self.interro_1.index]
        # Assert
        self.assertEqual(new_row['nb'], old_row['nb'] + 1)
        self.assertEqual(new_row['score'], old_row['score'] + 1)
        self.assertGreater(new_row['taux'], old_row['taux'])
        self.assertEqual(new_row['query'], old_row['query'] + 1)

    def test_update_voc_df_failure(self):
        """
        After the guess (or the non-guess, if the user is not very very smart),
        the word should be updated on number of queries, number of guesses, ...
        """
        # Arrange
        old_row = self.interro_1.words_df.loc[self.interro_1.index]
        word_guessed = False
        # Act
        self.interro_1.update_voc_df(word_guessed)
        new_row = self.interro_1.words_df.loc[self.interro_1.index]
        # Assert
        self.assertEqual(new_row['nb'], old_row['nb'] + 1)
        self.assertEqual(new_row['score'], old_row['score'] - 1)
        self.assertLess(new_row['taux'], old_row['taux'])
        self.assertEqual(new_row['query'], old_row['query'] + 1)

    @patch('src.views.terminal.CliGuesser.guess_word')
    @patch('src.interro.PremierTest.update_faults_df')
    @patch('src.interro.PremierTest.update_voc_df')
    def test_ask_series_of_guesses(self, mock_update_voc_df, mock_update_faults_df, mock_guess_word):
        # ----- ARRANGE
        self.interro_1.interro_df = pd.DataFrame(
            {
                'english': ['Hello'],
                'français': ['Bonjour']
            },
            index=[1]
        )
        mock_update_voc_df.return_value = True
        mock_update_faults_df.return_value = True
        mock_guess_word.return_value = 'Bonjour'
        # ----- ACT
        self.interro_1.ask_series_of_guesses()
        # ----- ASSERT
        mock_guess_word.assert_called_once_with(
            ['Hello', 'Bonjour'],
            1,
            self.interro_1.words
        )
        mock_update_voc_df.assert_called_once_with(
            'Bonjour'
        )
        mock_update_faults_df.assert_called_once_with(
            'Bonjour',
            ['Hello', 'Bonjour']
        )

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

    @patch.object(interro.PremierTest, 'set_interro_df')
    @patch.object(interro.PremierTest, 'ask_series_of_guesses')
    @patch.object(interro.PremierTest, 'compute_success_rate')
    def test_run(
        self,
        mock_compute_success_rate,
        mock_ask_series_of_guesses,
        mock_set_interro_df):
        """
        Should run a series of guesses to be answered by the user.
        """
        # Act
        self.interro_1.run()
        # Assert
        mock_compute_success_rate.assert_called_once()
        mock_ask_series_of_guesses.assert_called_once()
        mock_set_interro_df.assert_called_once()



class TestRattrap(unittest.TestCase):
    """
    Tests on Rattrap class methods.
    """
    def setUp(self):
        self.faults_df = pd.DataFrame({
            'english': [1, 2, 3],
            'français': [4, 5, 6]
        })
        self.rattraps = 10
        self.guesser = MagicMock()
        self.rattrap = interro.Rattrap(
            self.faults_df,
            self.rattraps,
            self.guesser
        )

    def test_init(self):
        """
        The constructor should create a Rattrap object.
        """
        # ----- ARRANGE
        # ----- ACT
        # ----- ASSERT
        # Verify superclass constructor call
        pd.testing.assert_frame_equal(self.rattrap.words_df, self.faults_df)
        self.assertEqual(self.rattrap.words, self.faults_df.shape[0])
        self.assertEqual(self.rattrap.guesser, self.guesser)
        # Verify attribute initialization
        pd.testing.assert_frame_equal(self.rattrap.words_df, self.faults_df)
        self.assertEqual(self.rattrap.rattraps, self.rattraps)
        pd.testing.assert_frame_equal(self.rattrap.interro_df, self.faults_df)

    def test_run_2(self):
        # ----- ARRANGE
        self.rattrap.set_row = MagicMock()
        self.rattrap.guesser.guess_word = MagicMock(return_value='guessed_word')
        self.rattrap.update_faults_df = MagicMock()
        self.rattrap.words_df = pd.DataFrame(
            {
                'col1': [1, 2, 3],
                'col2': [4, 5, 6]
            }
        )
        self.rattrap.faults_df = pd.DataFrame(
            {
                'col1': [1, 2, 3],
                'col2': [4, 5, 6]
            }
        )
        # ----- ACT
        self.rattrap.run()
        # ----- ASSERT
        self.assertEqual(
            self.rattrap.set_row.call_count,
            self.rattrap.words_df.shape[0]
        )
        self.assertEqual(
            self.rattrap.guesser.guess_word.call_count,
            self.rattrap.words_df.shape[0]
        )
        self.assertEqual(
            self.rattrap.update_faults_df.call_count,
            self.rattrap.words_df.shape[0]
        )
        self.assertEqual(len(self.rattrap.faults_df), 0)

    def test_start_loop(self):
        """
        The method should run the test as many times as necessary
        to go through all the words.
        """
        # ----- ARRANGE
        self.rattrap.rattraps = -1
        self.rattrap.words_df = pd.DataFrame({
            'mock_column': [1, 2, 3]
        })
        old_length = self.rattrap.words_df.shape[0]
        self.rattrap.run = MagicMock()
        def side_effect():
            self.rattrap.words_df = self.rattrap.words_df.iloc[1:]
        self.rattrap.run.side_effect = side_effect
        # ----- ACT
        self.rattrap.start_loop()
        # ----- ASSERT
        assert self.rattrap.run.call_count == old_length

    def test_start_loop_with_positive_rattraps(self):
        """
        Should run the test as many times as the number of rattraps.
        """
        # ----- ARRANGE
        self.rattrap.rattraps = 2
        self.rattrap.words_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        self.rattrap.run = MagicMock()
        # ----- ACT
        self.rattrap.start_loop()
        # ----- ASSERT
        expected_calls = min(
            self.rattrap.rattraps,
            len(self.rattrap.words_df)
        )
        self.assertEqual(
            self.rattrap.run.call_count,
            expected_calls
        )



class TestUpdater(unittest.TestCase):
    """
    Should save the user's guesses in the database,
    after having processed the dataset so as to: 
    - flag bad words;
    - and remove good words.
    """
    def setUp(self):
        self.user_1 = interro.CliUser()
        self.user_1.parse_arguments(['-t', 'version'])
        self.data_querier_1 = database_interface.DbQuerier(
            user_name='test_user',
            db_name='test_db',
            test_type=self.user_1.settings.type
        )
        self.loader_1 = interro.Loader(self.data_querier_1)
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
        words = 10
        self.guesser = view_terminal.CliGuesser()
        self.interro_1 = interro.PremierTest(
            self.loader_1.tables['version_voc'],
            words,
            self.guesser,
            self.loader_1.tables['version_perf'],
            self.loader_1.tables['version_words_count']
        )
        self.updater_1 = interro.Updater(
            self.loader_1,
            self.interro_1
        )

    def test_set_good_words(self):
        """Should flag the words that have been guessed sufficiently enough."""
        # Arrange
        if 'img_good' in self.updater_1.interro.words_df.columns:
            self.updater_1.interro.words_df.drop('img_good', axis=1, inplace=True)
        old_columns = list(self.updater_1.interro.words_df.columns)
        # Act
        self.updater_1.set_good_words()
        # Assert
        new_columns = list(self.updater_1.interro.words_df.columns)
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
        old_shape = self.interro_1.words_df.shape
        # Act
        self.updater_1.delete_good_words()
        # Assert
        new_shape = self.interro_1.words_df.shape
        self.assertLessEqual(new_shape[0], old_shape[0])
        self.assertEqual(new_shape[1], old_shape[1] - 1)
        self.assertNotIn('img_good', self.interro_1.words_df.columns)

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
            'output',
            self.updater_1.loader.tables['output']
        )
        mock_delete_good_words.assert_called_once()

    def test_flag_bad_words(self):
        """Should flag bad words, i.e. words rarely guessed by the user."""
        # Arrange
        old_length, old_width = self.updater_1.interro.words_df.shape
        # Act
        self.updater_1.flag_bad_words()
        new_length, new_width = self.updater_1.interro.words_df.shape
        first_word = self.updater_1.interro.words_df.iloc[0]
        ord_bad = self.updater_1.criteria['ORD_BAD']
        steep_bad = self.updater_1.criteria['STEEP_BAD']
        img_bad = ord_bad + steep_bad * first_word['nb']
        # Assert
        self.assertLessEqual(new_length, old_length)
        self.assertEqual(new_width, old_width)
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
        old_width = self.updater_1.interro.words_df.shape[1]
        mock_save_table.return_value = True
        # ----- ACT
        self.updater_1.save_words()
        # ----- ASSERT
        new_width = self.updater_1.interro.words_df.shape[1]
        mock_save_table.assert_called_once_with(
            self.updater_1.loader.test_type + '_voc',
            self.updater_1.interro.words_df
        )
        self.assertEqual(new_width, old_width + 1)

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
        self.updater_1.interro.perf_df = perf_df
        old_shape = self.updater_1.interro.perf_df.shape
        mock_save_table.return_value = True
        # Act
        self.updater_1.save_performances()
        new_shape = self.updater_1.interro.perf_df.shape
        # Assert
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        self.assertEqual(new_shape[1], old_shape[1] + 1)
        mock_save_table.assert_called_once_with(
            self.updater_1.loader.test_type + '_perf',
            self.updater_1.interro.perf_df
        )
        last_perf = self.updater_1.interro.perf_df.loc[
            self.updater_1.interro.perf_df.shape[0] - 1
        ]
        last_perf = last_perf['test']
        self.assertEqual(last_perf, self.updater_1.interro.perf)

    @patch('src.data.database_interface.DbManipulator.save_table')
    def test_save_words_count(self, mock_save_table):
        """
        Save the number of words recorded on the current date.
        """
        # ----- ARRANGE
        self.updater_1.interro.word_cnt_df = pd.DataFrame({
            'test_date': ['2022-01-01', '2022-02-01'],
            'nb': [1876, 2341]
        })
        old_shape = self.updater_1.interro.word_cnt_df.shape
        mock_save_table.return_value = True
        # ----- ACT
        self.updater_1.save_words_count()
        # ----- ASSERT
        new_shape = self.updater_1.interro.word_cnt_df.shape
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        self.assertEqual(new_shape[1], old_shape[1])
        mock_save_table.assert_called_once_with(
            self.updater_1.loader.test_type + '_words_count',
            self.updater_1.interro.word_cnt_df
        )
        last_count = self.updater_1.interro.word_cnt_df.loc[
            self.updater_1.interro.word_cnt_df.shape[0] - 1
        ]
        last_count = last_count['nb']
        self.assertEqual(last_count, self.updater_1.interro.words_df.shape[0])

    @patch('src.data.database_interface.DbManipulator.save_table')
    def test_save_words_count_reset_index(self, mock_save_table):
        """
        Save the number of words recorded on the current date.
        """
        # ----- ARRANGE
        self.updater_1.interro.word_cnt_df = pd.DataFrame({
            'test_date': ['2022-01-01', '2022-02-01'],
            'nb': [1876, 2341]
        })
        self.updater_1.interro.word_cnt_df.set_index('test_date', inplace=True)
        old_shape = self.updater_1.interro.word_cnt_df.shape
        mock_save_table.return_value = True
        # ----- ACT
        self.updater_1.save_words_count()
        # ----- ASSERT
        new_shape = self.updater_1.interro.word_cnt_df.shape
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        self.assertEqual(new_shape[1], old_shape[1] + 1)
        mock_save_table.assert_called_once_with(
            self.updater_1.loader.test_type + '_words_count',
            self.updater_1.interro.word_cnt_df
        )
        last_count = self.updater_1.interro.word_cnt_df.loc[
            self.updater_1.interro.word_cnt_df.shape[0] - 1
        ]
        last_count = last_count['nb']
        self.assertEqual(last_count, self.updater_1.interro.words_df.shape[0])

    @patch.object(interro.Updater, 'move_good_words')
    @patch.object(interro.Updater, 'flag_bad_words')
    @patch.object(interro.Updater, 'save_words')
    @patch.object(interro.Updater, 'save_performances')
    @patch.object(interro.Updater, 'save_words_count')
    def test_update_data(
        self,
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
