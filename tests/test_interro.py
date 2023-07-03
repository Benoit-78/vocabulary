#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Creator: B.Delorme1
    Mail: delormebenoit211@gmail.com
    Creation date: 11th March 2023
    Main purpose: test script for interro.py, main script of vocabulary application
"""

import unittest
import pytest
import numpy as np
import pandas as pd
import random
import argparse
from io import StringIO

import interro



class TestParser(unittest.TestCase):
    """Tests on arguments parser."""
    def test_parse_arguments(self):
        ### Happy paths
        # Test case 1: Valid arguments provided
        args = ['--type', 'version',
                '--words', '100',
                '--rattraps', '1']
        result = interro.parse_arguments(args)
        assert isinstance(result, argparse.Namespace)
        assert result.type == 'version'
        assert result.rattraps == 1
        # Test case 2: Only required argument provided
        args = ['-t', 'theme']
        result = interro.parse_arguments(args)
        assert isinstance(result, argparse.Namespace)
        assert result.type == 'theme'
        assert result.rattraps is None
        ### Sad paths

    def test_check_args(self):
        ### Happy paths
        # Test case 1
        for test_kind in ['version', 'theme']:
            args = argparse.Namespace(type=test_kind, words=100, rattraps=1)
            result = interro.check_args(args)
            assert result == args
        ### Sad paths
        # Test case 2
        args = argparse.Namespace(type=None, words=10, rattraps=10)
        with pytest.raises(SystemExit):
            interro.check_args(args)
        # Test case 3
        args = argparse.Namespace(type='', words=10, rattraps=1)
        with pytest.raises(SystemExit):
            expected_output = "# ERROR   | Please give a test type: either version or theme"
            with StringIO() as output:
                interro.check_args(args)
                self.assertEqual(output.getvalue(), expected_output)
        # Test case 4
        args = argparse.Namespace(type="invalid", words=10, rattraps=1)
        with pytest.raises(SystemExit):
            interro.check_args(args)



class TestLoader(unittest.TestCase):
    """Tests on Loader class methods."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        parser_version = interro.parse_arguments(['-t', 'version'])
        parser_theme = interro.parse_arguments(['-t', 'theme'])
        cls.loaders = [interro.Loader(parser_version),
                       interro.Loader(parser_theme)]

    def test_get_os_type(self):
        """Operating system should be either Windows or Linux"""
        for loader in self.loaders:
            # Happy paths
            loader.get_os_type()
            self.assertIn(loader.os_type, ['Windows', 'Linux', 'Mac', 'Android'])
            # Sad paths
            with self.assertRaises(AssertionError):
                self.assertEqual(loader.os_type, 'Ubuntu')

    def test_set_os_separator(self):
        """Separator should be OS-specific"""
        for loader in self.loaders:
            # Happy paths
            loader.set_os_separator()
            if loader.os_type == 'Windows':
                self.assertEqual(loader.os_sep, '\\')
            elif loader.os_type in ['Linux', 'Android', 'Mac']:
                self.assertEqual(loader.os_sep, '/')
            # Sad paths

    def test_set_data_paths(self):
        """Data paths should exist"""
        for loader in self.loaders:
            # Happy paths
            loader.set_data_paths()
            self.assertIsInstance(loader.paths, dict)
            self.assertEqual(len(loader.paths), 3)
            for _, path in loader.paths.items():
                self.assertIsInstance(path, str)
            # Sad paths

    def test_get_data(self):
        """Data should be correctly loaded"""
        for loader in self.loaders:
            loader.get_data()
            # Happy paths
            self.assertIsInstance(loader.data, dict)
            self.assertEqual(len(loader.data), 3)
            for df_name, dataframe in loader.data.items():
                self.assertIn(df_name, ['voc', 'perf', 'word_cnt'])
                self.assertIsInstance(dataframe, type(pd.DataFrame()))
            # Sad paths

    def test_data_extraction(self):
        """Input should be a dataframe, and it should be added a query column"""
        for loader in self.loaders:
            loader.data_extraction()
            voc_df = loader.data['voc']
            # Happy paths
            self.assertIn('Date', list(voc_df.columns))
            self.assertIn('Query', list(voc_df.columns))
            self.assertEqual(voc_df[voc_df.columns[0]].dtype, object)
            self.assertEqual(voc_df[voc_df.columns[1]].dtype, object)
            self.assertEqual(voc_df['Taux'].dtype, np.float64)
            self.assertGreater(voc_df.shape[0], 1)
            # Sad paths



class TestInterro(unittest.TestCase):
    """Tests on Interro abstract class methods."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        parser_version = interro.parse_arguments(['-t', 'version'])
        parser_theme = interro.parse_arguments(['-t', 'theme'])
        cls.loaders = [interro.Loader(parser_version),
                       interro.Loader(parser_theme)]

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite."""

    def setUp(self):
        """Runs before each test."""

    def tearDown(self):
        """Runs once after each test case."""
 
    def test_run(self):
        """"""



class TestTest(unittest.TestCase):
    """Tests on Test class methods."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        parser_version = interro.parse_arguments(['-t', 'version'])
        parser_theme = interro.parse_arguments(['-t', 'theme'])
        cls.loaders = [interro.Loader(parser_version),
                       interro.Loader(parser_theme)]

    def test_get_row(self):
        """The returned row should enable the user to guess the word"""
        for loader in self.loaders:
            loader.data_extraction()
            my_interro = interro.Test(loader.data['voc'],
                                      loader.data['perf'],
                                      loader.data['word_cnt'])
            self.index = random.randint(1, my_interro.words_df.shape[0])
            row = my_interro.get_row()
            # Happy paths
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), 2)
            self.assertIsInstance(row[0], str)
            self.assertIsInstance(row[1], str)
            # Sad paths

    def test_guess_word(self):
        """The result should be either True or False"""
        for loader in self.loaders:
            loader.data_extraction()
            my_interro = interro.Test(loader.data['voc'],
                                      loader.data['perf'],
                                      loader.data['word_cnt'])
            self.index = random.randint(1, my_interro.words_df.shape[0])
            row = my_interro.get_row()
            word_guessed = my_interro.guess_word(row, 1)
            # Happy paths
            self.assertIsInstance(word_guessed, bool)
            # Sad paths

    def test_update_voc_df(self):
        """voc_df should be updated according to user's guess"""

    def test_ask_total_to_the_user(self):
        """The user should be asked a total as an input"""

    def test_create_random_step(self):
        """The step should be a random integer"""
        for loader in self.loaders:
            loader.data_extraction()
            my_test = interro.Test(loader.data['voc'],
                                   loader.data['perf'],
                                   loader.data['word_cnt'])
            # Happy paths
            my_test.create_random_step()
            self.assertIsInstance(my_test.step, int)
            self.assertGreater(my_test.step, 0)
            self.assertLess(my_test.step, my_test.words_df.shape[0])
            # Sad paths

    def test_get_next_index(self):
        """Next index should point to a word that was not already asked"""
        for loader in self.loaders:
            loader.data_extraction()
            my_test = interro.Test(loader.data['voc'],
                                   loader.data['perf'],
                                   loader.data['word_cnt'])
            my_test.create_random_step()
            for i in range(1, 101):
                # Happy paths
                next_index = my_test.get_next_index()
                self.assertIsInstance(next_index, int)
                self.assertGreater(next_index, 1)
                self.assertLess(next_index, (my_test.words_df.shape[0]))
                self.assertEqual(my_test.words_df['Query'].loc[next_index], 0)
                # Sad paths


class TestRattrap(unittest.TestCase):
    """Tests on Rattrap class methods."""



class TestGraphiques(unittest.TestCase):
    """Tests on Rattrap class methods."""