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

REPO_DIR = os.getcwd().split('tests')[0]
sys.path.append(REPO_DIR)
from src import interro, views_local
from src.data import data_handler


class TestParser(unittest.TestCase):
    """Tests on arguments parser."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.user = interro.CliUser()

    # def test_parse_arguments(self):
    #     """The method should store three arguments."""
        # with unittest.mock.patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
        #     self.user.parse_arguments([])
        #     mock_parse_args.assert_called_with(
        #         [
        #             '-t', 'version',
        #             '-w', '10',
        #             '-r', '2'
        #         ]
        #     )
        # ### Happy paths
        # # Test case 1: Valid arguments provided
        # args = [
        #     '--type', 'version',
        #     '--words', '100',
        #     '--rattraps', '1'
        # ]
        # self.user.parse_arguments(args)
        # assert isinstance(self.user.settings, dict)
        # # Test case 2: Only required argument provided
        # args = ['-t', 'theme']
        # result = self.user.parse_arguments(args)
        # assert isinstance(result, argparse.Namespace)
        # assert result.type == 'theme'
        # assert result.rattraps is None
        # ### Sad paths

    # def test_get_settings(self):
    #     """Should save the user's settings as attributes."""
        # ### Happy paths
        # # Test case 1
        # for test_kind in ['version', 'theme']:
        #     args = argparse.Namespace(type=test_kind, words=100, rattraps=1)
        #     result = interro.check_args(args)
        #     assert result == args
        # ### Sad paths
        # # Test case 2
        # args = argparse.Namespace(type=None, words=10, rattraps=10)
        # with pytest.raises(SystemExit):
        #     interro.check_args(args)
        # # Test case 3
        # args = argparse.Namespace(type='', words=10, rattraps=1)
        # with pytest.raises(SystemExit):
        #     expected_output = "# ERROR   | Please give a test type: either version or theme"
        #     with StringIO() as output:
        #         interro.check_args(args)
        #         self.assertEqual(output.getvalue(), expected_output)
        # # Test case 4
        # args = argparse.Namespace(type="invalid", words=10, rattraps=1)
        # with pytest.raises(SystemExit):
        #     interro.check_args(args)



class TestLoader(unittest.TestCase):
    """
    The Loader class should interact with database interfaces, such as CsvHandler or MariaDBHandler.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        # Arrange
        cls.user = interro.CliUser()
        cls.user.parse_arguments(['-t', 'version'])
        cls.data_manipulator = data_handler.DbManipulator(
            user_name='test_user',
            db_name='test_db',
            host='test_host',
            test_type='test_type'
        )
        cls.loader = None

    def test_load_tables(self):
        """Input should be a dataframe, and it should be added a query column"""
        # Arrange
        # Act
        self.loader = interro.Loader(
            self.user.settings.rattraps,
            self.data_manipulator
        )
        # Assert
        for table in self.loader.tables.values():
            self.assertIn('creation_date', list(table.columns))
            self.assertIn('query', list(table.columns))
            self.assertEqual(table[table.columns[0]].dtype, object)
            self.assertEqual(table[table.columns[1]].dtype, object)
            self.assertEqual(table['taux'].dtype, np.float64)
            self.assertGreater(table.shape[0], 1)



class TestTest(unittest.TestCase):
    """
    The Interro class represents the concept of a test taken by the user.
    It should then be abstract.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.user_1 = interro.CliUser()
        cls.user_1.parse_arguments(['-t', 'version'])
        cls.data_handler_1 = data_handler.DbManipulator(
            user_name='test_user',
            db_name='test_db',
            host='test_host',
            test_type='test_type'
        )
        cls.loader_1 = interro.Loader(
            cls.user_1.settings.rattraps,
            cls.data_handler_1
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
        guesser = views_local.CliGuesser()
        self.interro_1 = interro.Test(
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

    def test_get_another_index(self):
        """
        This function should provide with a new index, corresponding to a new word.
        The new word should not have been already asked within the current test.
        """
        # Arrange
        former_index = self.interro_1.index
        self.interro_1.words_df['query'] = [0] * self.interro_1.words_df.shape[0]
        self.interro_1.words_df['bad_word'] = [0] * self.interro_1.words_df.shape[0]
        # Act
        next_index = self.interro_1.get_another_index()
        # Assert
        self.assertIsInstance(next_index, int)
        self.assertGreater(next_index, 0)
        self.assertLess(next_index, self.interro_1.words_df.shape[0])
        self.assertEqual(self.interro_1.words_df['query'].loc[next_index], 1)
        if next_index != 1: # Case where the first next_index falls on 1
            self.assertNotEqual(former_index, next_index)

    def test_get_next_index(self):
        """Bad words should be asked twice as much as other words."""
        # Arrange
        self.interro_1.step = 7
        self.interro_1.words_df['query'] = [0] * self.interro_1.words_df.shape[0]
        self.interro_1.words_df['bad_word'] = [0] * self.interro_1.words_df.shape[0]
        former_index = self.interro_1.index
        logger.debug(f"former_index: {former_index}")
        # Act
        next_index = self.interro_1.get_next_index()
        logger.debug(f"next_index: {next_index}")
        # Assert
        self.assertIsInstance(next_index, int)
        self.assertGreater(next_index, 0)
        self.assertLess(next_index, self.interro_1.words_df.shape[0])
        self.assertEqual(self.interro_1.words_df['query'].loc[next_index], 1)
        if next_index != 1: # Case where the first next_index falls on 1
            self.assertNotEqual(former_index, next_index)

    @patch.object(interro.Test, 'get_another_index', return_value=4)
    def test_get_next_index_if_bad_word(self, mock_get_another_index):
        """
        When the next index points to a bad word, the search should stop.
        So the index search method should be called once.
        """
        # Arrange
        self.interro_1.words_df['bad_word'] = [1] * self.interro_1.words_df.shape[0]
        # Act
        next_index = self.interro_1.get_next_index()
        # Assert
        self.assertEqual(next_index, 4)
        mock_get_another_index.assert_called()
        assert mock_get_another_index.call_count == 1

    @patch.object(interro.Test, 'get_another_index', return_value=4)
    def test_get_next_index_if_not_bad_word(self, mock_get_another_index):
        """
        When the next index points to a bad word, the search should run once again.
        So the index search method should be called twice.
        """
        # Arrange
        self.interro_1.words_df['bad_word'] = [0] * self.interro_1.words_df.shape[0]
        # Act
        next_index = self.interro_1.get_next_index()
        # Assert
        self.assertEqual(next_index, 4)
        mock_get_another_index.assert_called()
        assert mock_get_another_index.call_count == 2

    def test_set_interro_df(self):
        """A dataframe of words should be formed, that will be asked to the user."""
        # Act
        self.interro_1.set_interro_df()
        # Assert
        nan_values = self.interro_1.interro_df.isna().sum().sum()
        self.assertNotEqual(self.interro_1.step, 0)
        self.assertEqual(self.interro_1.interro_df.shape, (self.interro_1.words, 2))
        self.assertEqual(nan_values, 0)

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

    @patch('src.interro.Test.update_voc_df')
    @patch('src.interro.Test.update_faults_df')
    def test_ask_series_of_guesses(self, mock_update_voc_df, mock_update_faults_df):
        """Should ask a series of guesses to the user."""
        # Arrange
        mock_guess_word = MagicMock(return_value=True)
        self.interro_1.guesser.guess_word = mock_guess_word
        # Act
        self.interro_1.ask_series_of_guesses()
        # Assert
        self.assertEqual(mock_guess_word.call_count, len(self.interro_1.interro_df))
        for _, index in enumerate(self.interro_1.interro_df.index):
            row = list(self.interro_1.interro_df.loc[index])
            mock_update_voc_df.assert_any_call(True)
            mock_update_faults_df.assert_any_call(True, row)

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

    @patch.object(interro.Test, 'set_interro_df')
    @patch.object(interro.Test, 'ask_series_of_guesses')
    @patch.object(interro.Test, 'compute_success_rate')
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
    """Tests on Rattrap class methods."""



class TestUpdater(unittest.TestCase):
    """
    Should save the user's guesses in the database,
    after having processed the dataset so as to: 
    - flag bad words;
    - and remove good words.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        rattraps = 1
        cls.user_1 = interro.CliUser()
        cls.user_1.parse_arguments(['-t', 'version'])
        cls.data_handler_1 = data_handler.DbManipulator(
            user_name='test_user',
            db_name='test_db',
            host='test_host',
            test_type=cls.user_1.settings.type
        )
        cls.loader_1 = interro.Loader(rattraps, cls.data_handler_1)
        cls.loader_1.tables = {
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

    def setUp(self):
        """Runs before each test"""
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
        df['img_good'] = [0] * df.shape[0]
        self.loader_1.tables['version_voc'] = df
        words = 10
        self.guesser = views_local.CliGuesser()
        self.interro_1 = interro.Test(
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
        """Should copy the well good words in the output table."""
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

    def test_move_good_words(self):
        """
        Should move the words that have been guessed sufficiently enough
        from one table to its output.
        """
        # Arrange
        self.updater_1.set_good_words = MagicMock()
        self.updater_1.copy_good_words = MagicMock()
        self.updater_1.loader.tables['output'] = MagicMock()
        self.updater_1.loader.data_handler.save_table = MagicMock()
        self.updater_1.delete_good_words = MagicMock()
        # Act
        self.updater_1.move_good_words()
        # Assert
        self.updater_1.set_good_words.assert_called_once()
        self.updater_1.copy_good_words.assert_called_once()
        self.updater_1.loader.tables['output'].reset_index.assert_called_once()
        self.updater_1.loader.data_handler.save_table.assert_called_once_with(
            'output',
            self.updater_1.loader.tables['output']
        )
        self.updater_1.delete_good_words.assert_called_once()

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

    def test_save_words(self):
        """Prepare the words table for saving, and save it."""
        # Arrange
        self.updater_1.loader.data_handler.save_table = MagicMock()
        old_width = self.updater_1.interro.words_df.shape[1]
        # Act
        self.updater_1.save_words()
        new_width = self.updater_1.interro.words_df.shape[1]
        # Assert
        self.updater_1.loader.data_handler.save_table.assert_called_once_with(
            self.updater_1.loader.test_type + '_voc',
            self.updater_1.interro.words_df
        )
        self.assertEqual(new_width, old_width + 1)

    def test_save_performances(self):
        """Save performances for further analysis."""
        # Arrange
        self.updater_1.loader.data_handler.save_table = MagicMock()
        perf_df = pd.DataFrame(columns=['test_date', 'test'])
        perf_df.loc[perf_df.shape[0]] = ["2022-01-01", 65]
        perf_df.loc[perf_df.shape[0]] = ["2022-02-01", 75]
        perf_df.loc[perf_df.shape[0]] = ["2022-03-01", 85]
        perf_df.loc[perf_df.shape[0]] = ["2022-04-01", 0]
        self.updater_1.interro.perf_df = perf_df
        old_shape = self.updater_1.interro.perf_df.shape
        # Act
        self.updater_1.save_performances()
        new_shape = self.updater_1.interro.perf_df.shape
        # Assert
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        logger.debug(f"Columns: {self.updater_1.interro.perf_df.columns}")
        self.assertEqual(new_shape[1], old_shape[1] + 1)
        self.updater_1.loader.data_handler.save_table.assert_called_once_with(
            self.updater_1.loader.test_type + '_perf',
            self.updater_1.interro.perf_df
        )
        last_perf = self.updater_1.interro.perf_df.loc[
            self.updater_1.interro.perf_df.shape[0] - 1
        ]
        last_perf = last_perf['test']
        self.assertEqual(last_perf, self.updater_1.interro.perf)

    def test_save_words_count(self):
        """Save the number of words recorded on the current date."""
        # Arrange
        self.updater_1.loader.data_handler.save_table = MagicMock()
        word_cnt_df = pd.DataFrame(columns=['test_date', 'words_count'])
        word_cnt_df.loc[word_cnt_df.shape[0]] = ["2022-01-01", 1876]
        word_cnt_df.loc[word_cnt_df.shape[0]] = ["2022-02-01", 2341]
        self.updater_1.interro.word_cnt_df = word_cnt_df
        old_shape = self.updater_1.interro.word_cnt_df.shape
        # Act
        self.updater_1.save_words_count()
        new_shape = self.updater_1.interro.word_cnt_df.shape
        # Assert
        self.assertEqual(new_shape[0], old_shape[0] + 1)
        self.assertEqual(new_shape[1], old_shape[1] + 1)
        self.updater_1.loader.data_handler.save_table.assert_called_once_with(
            self.updater_1.loader.test_type + '_words_count',
            self.updater_1.interro.word_cnt_df
        )
        last_count = self.updater_1.interro.word_cnt_df.loc[
            self.updater_1.interro.word_cnt_df.shape[0] - 1
        ]
        last_count = last_count['words_count']
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
