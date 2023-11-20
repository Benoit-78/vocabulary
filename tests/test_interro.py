"""
    Creator:
        B.Delorme
    Creation date:
        11th March 2023
    Main purpose:
        Test script for interro.py, main script of vocabulary application
"""

import unittest
from unittest.mock import patch
import sys
import numpy as np
import pandas as pd
from loguru import logger

sys.path.append('\\src')
from src import interro
from src import views_local
from src.data import data_handler



class TestParser(unittest.TestCase):
    """Tests on arguments parser."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.user = interro.CliUser()

    def test_parse_arguments(self):
        """The method should store three arguments."""
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

    def test_get_settings(self):
        """Should save the user's settings as attributes."""
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
        cls.user_1 = interro.CliUser()
        cls.user_2 = interro.CliUser()
        cls.user_1.parse_arguments(['-t', 'version'])
        cls.user_2.parse_arguments(['-t', 'theme'])
        cls.data_handler_1_2 = data_handler.MariaDBHandler(
            cls.user_1.settings.type,
            'cli',
            'English'
        )
        cls.data_handler_2_2 = data_handler.MariaDBHandler(
            cls.user_2.settings.type,
            'cli',
            'Zhongwen'
        )
        cls.loader_1_1 = None
        cls.loader_1_2 = None
        cls.loader_2_1 = None
        cls.loader_2_2 = None

    def test_load_tables(self):
        """Input should be a dataframe, and it should be added a query column"""
        # Arrange
        # Act
        self.loader_1_2 = interro.Loader(
            self.user_1.settings.rattraps,
            self.data_handler_1_2
        )
        self.loader_2_2 = interro.Loader(
            self.user_2.settings.rattraps,
            self.data_handler_2_2
        )
        # Assert
        for loader in [self.loader_1_2, self.loader_2_2]:
            logger.debug(loader)
            for table in loader.tables.values():
                self.assertIn('Date', list(table.columns))
                self.assertIn('Query', list(table.columns))
                self.assertEqual(table[table.columns[0]].dtype, object)
                self.assertEqual(table[table.columns[1]].dtype, object)
                self.assertEqual(table['Taux'].dtype, np.float64)
                self.assertGreater(table.shape[0], 1)



class TestTest(unittest.TestCase):
    """
    The Interro class represents the concept of a test to be taken by the user.
    It should then be abstract.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        cls.user_1 = interro.CliUser()
        cls.user_2 = interro.CliUser()
        cls.user_1.parse_arguments(['-t', 'version'])
        cls.user_2.parse_arguments(['-t', 'theme'])
        cls.data_handler_1 = data_handler.MariaDBHandler(
            cls.user_1.settings.type,
            'cli',
            'English'
        )
        cls.data_handler_2 = data_handler.MariaDBHandler(
            cls.user_2.settings.type,
            'cli',
            'Zhongwen'
        )
        cls.loader_1 = interro.Loader(
            cls.user_1.settings.rattraps,
            cls.data_handler_1
        )
        cls.loader_2 = interro.Loader(
            cls.user_2.settings.rattraps,
            cls.data_handler_2
        )
        words_df = pd.DataFrame(columns=['English', 'Français'])
        words_df.loc[words_df.shape[0]] = ['Hello', 'Bonjour']
        words_df.loc[words_df.shape[0]] = [
            'Do you want to dance with me?',
            'M\'accorderiez-vous cette danse ?'
        ]
        words_df.loc[words_df.shape[0]] = ['One', 'Un']
        words_df.loc[words_df.shape[0]] = ['Two', 'Deux']
        words_df.loc[words_df.shape[0]] = ['Three', 'Trois']
        words_df.loc[words_df.shape[0]] = ['Four', 'Quatre']
        words_df.loc[words_df.shape[0]] = ['Cinq', 'Cinq']
        words_df.loc[words_df.shape[0]] = ['Six', 'Six']
        words_df.loc[words_df.shape[0]] = ['Seven', 'Sept']
        words_df.loc[words_df.shape[0]] = ['Eight', 'Huit']
        words_df.loc[words_df.shape[0]] = ['Nine', 'Neuf']
        words_df.loc[words_df.shape[0]] = ['Ten', 'Dix']
        words_df['Query'] = [0] * words_df.shape[0]
        words_df['Nb'] = [0] * words_df.shape[0]
        words_df['Score'] = [0] * words_df.shape[0]
        words_df['Taux'] = [0] * words_df.shape[0]
        words_df['Bad_word'] = [0] * words_df.shape[0]
        words = words_df.shape[0] //  2
        guesser = views_local.CliGuesser()
        cls.interro_1 = interro.Test(words_df, words, guesser)
        cls.interro_1.step = 1

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
        self.interro_1.words_df['Query'] = [0] * self.interro_1.words_df.shape[0]
        self.interro_1.words_df['bad_word'] = [0] * self.interro_1.words_df.shape[0]
        # Act
        next_index = self.interro_1.get_another_index()
        # Assert
        self.assertIsInstance(next_index, int)
        self.assertGreater(next_index, 0)
        self.assertLess(next_index, self.interro_1.words_df.shape[0])
        self.assertEqual(self.interro_1.words_df['Query'].loc[next_index], 1)
        if next_index != 1: # Case where the first next_index falls on 1
            self.assertNotEqual(former_index, next_index)

    def test_get_next_index(self):
        """Bad words should be asked twice as much as other words."""
        # Arrange
        self.interro_1.step = 7
        self.interro_1.words_df['Query'] = [0] * self.interro_1.words_df.shape[0]
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
        self.assertEqual(self.interro_1.words_df['Query'].loc[next_index], 1)
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
        self.assertEqual(new_row['Nb'], old_row['Nb'] + 1)
        self.assertEqual(new_row['Score'], old_row['Score'] + 1)
        self.assertGreater(new_row['Taux'], old_row['Taux'])
        self.assertEqual(new_row['Query'], old_row['Query'] + 1)

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
        self.assertEqual(new_row['Nb'], old_row['Nb'] + 1)
        self.assertEqual(new_row['Score'], old_row['Score'] - 1)
        self.assertLess(new_row['Taux'], old_row['Taux'])
        self.assertEqual(new_row['Query'], old_row['Query'] + 1)

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
    """Tests on Rattrap class methods."""



class TestUpdater(unittest.TestCase):
    """
    Should save the user's guesses in the database, after having processed the dataset so as to: 
    - flag bad words;
    - and remove good words.
    """
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        rattraps = 1
        cls.user_1 = interro.CliUser()
        cls.user_1.parse_arguments(['-t', 'version'])
        cls.data_handler_1 = data_handler.CsvHandler(
            cls.user_1.settings.type
        )
        cls.loader_1 = interro.Loader(rattraps, cls.data_handler_1)
        cls.loader_1.load_tables()
        words_df = pd.DataFrame(columns=['English', 'Français'])
        words_df.loc[words_df.shape[0]] = ['Hello', 'Bonjour']
        words_df.loc[words_df.shape[0]] = [
            'Do you want to dance with me?',
            'M\'accorderiez-vous cette danse ?'
        ]
        words_df.loc[words_df.shape[0]] = ['One', 'Un']
        words_df.loc[words_df.shape[0]] = ['Two', 'Deux']
        words_df.loc[words_df.shape[0]] = ['Three', 'Trois']
        words_df.loc[words_df.shape[0]] = ['Four', 'Quatre']
        words_df.loc[words_df.shape[0]] = ['Cinq', 'Cinq']
        words_df.loc[words_df.shape[0]] = ['Six', 'Six']
        words_df.loc[words_df.shape[0]] = ['Seven', 'Sept']
        words_df.loc[words_df.shape[0]] = ['Eight', 'Huit']
        words_df.loc[words_df.shape[0]] = ['Nine', 'Neuf']
        words_df.loc[words_df.shape[0]] = ['Ten', 'Dix']
        words_df['Query'] = [0] * words_df.shape[0]
        words_df['Nb'] = [0] * words_df.shape[0]
        words_df['Score'] = [0] * words_df.shape[0]
        words_df['Taux'] = [0] * words_df.shape[0]
        words_df['Bad_word'] = [0] * words_df.shape[0]
        words = 10
        cls.guesser = views_local.CliGuesser()
        cls.interro_1 = interro.Test(words_df, words, cls.guesser)
        cls.updater_1 = interro.Updater(cls.loader_1, cls.interro_1)

    def test_set_known_words(self):
        """Should flag the words that have been guessed sufficiently enough."""
        # Arrange
        if 'img_good' in self.interro_1.words_df.columns:
            self.interro_1.words_df = self.interro_1.words_df.drop('img_good', axis=1)
        old_columns = list(self.interro_1.words_df.columns)
        # Act
        self.updater_1.set_known_words()
        # Assert
        new_columns = list(self.interro_1.words_df.columns)
        self.assertIn('img_good', new_columns)
        self.assertEqual(len(new_columns), len(old_columns) + 1)
        self.assertIsInstance(self.updater_1.known_words_df, pd.DataFrame)

    def test_copy_known_words(self):
        """Should copy the well known words in the output table."""
        # Arrange
        old_output_shape = self.loader_1.tables['output'].shape
        good_words = self.updater_1.known_words_df.shape[0]
        # Act
        self.updater_1.copy_known_words()
        # Assert
        new_output_shape = self.loader_1.tables['output'].shape
        self.assertEqual(new_output_shape[0], old_output_shape[0] + good_words)

    def test_transfer_known_words(self):
        """"""
