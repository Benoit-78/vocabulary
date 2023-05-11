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
        # Happy paths
        args = ["--type", "unit"]
        result = interro.parse_arguments(args)
        assert result == argparse.Namespace(type="unit")
        # Sad paths
        args = []
        result = interro.parse_arguments(args)
        assert result == argparse.Namespace(type=None)
        args = ["--invalid"]
        with pytest.raises(SystemExit):
            interro.parse_arguments(args)

    def test_check_args(self):
        # Happy paths
        for test_kind in ['version', 'theme']:
            args = argparse.Namespace(type=test_kind)
            result = interro.check_args(args)
            assert result == args
        # Sad paths
        args = argparse.Namespace(type=None)
        with pytest.raises(SystemExit):
            interro.check_args(args)
        args = argparse.Namespace(type='')
        with pytest.raises(SystemExit):
            expected_output = "# ERROR   | Please give a test type: either version or theme"
            with StringIO() as output:
                interro.check_args(args)
                self.assertEqual(output.getvalue(), expected_output)
        args = argparse.Namespace(type="invalid")
        with pytest.raises(SystemExit):
            interro.check_args(args)



class TestChargeur(unittest.TestCase):
    """Tests on Chargeur class methods."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        parser_version = interro.parse_arguments(['-t', 'version'])
        parser_theme = interro.parse_arguments(['-t', 'theme'])
        cls.chargeurs = [interro.Chargeur(parser_version),
                          interro.Chargeur(parser_theme)]

    def test_get_os_type(self):
        """Operating system should be either Windows or Linux"""
        for chargeur in self.chargeurs:
            # Happy paths
            chargeur.get_os_type()
            self.assertIn(chargeur.os_type, ['Windows', 'Linux', 'Mac', 'Android'])
            # Sad paths
            with self.assertRaises(AssertionError):
                self.assertEqual(chargeur.os_type, 'Ubuntu')

    def test_set_os_separator(self):
        """Separator should be OS-specific"""
        for chargeur in self.chargeurs:
            # Happy paths
            chargeur.set_os_separator()
            if chargeur.os_type == 'Windows':
                self.assertEqual(chargeur.os_sep, '\\')
            elif chargeur.os_type in ['Linux', 'Android', 'Mac']:
                self.assertEqual(chargeur.os_sep, '/')
            # Sad paths

    def test_set_data_paths(self):
        """Data paths should exist"""
        for chargeur in self.chargeurs:
            # Happy paths
            chargeur.set_data_paths()
            self.assertIsInstance(chargeur.paths, dict)
            self.assertEqual(len(chargeur.paths), 3)
            for _, path in chargeur.paths.items():
                self.assertIsInstance(path, str)
            # Sad paths

    def test_get_data(self):
        """Data should be correctly loaded"""
        for chargeur in self.chargeurs:
            chargeur.get_data()
            # Happy paths
            self.assertIsInstance(chargeur.data, dict)
            self.assertEqual(len(chargeur.data), 3)
            for df_name, dataframe in chargeur.data.items():
                self.assertIn(df_name, ['voc', 'perf', 'word_cnt'])
                self.assertIsInstance(dataframe, type(pd.DataFrame()))
            # Sad paths

    def test_data_extraction(self):
        """Input should be a dataframe, and it should be added a query column"""
        for chargeur in self.chargeurs:
            chargeur.data_extraction()
            voc_df = chargeur.data['voc']
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
        cls.chargeurs = [interro.Chargeur(parser_version),
                         interro.Chargeur(parser_theme)]

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite."""

    def setUp(self):
        """Runs before each test."""

    def tearDown(self):
        """Runs once after each test case."""
 
    def test_run(self):
        """"""

    def test_get_row(self):
        """The returned row should enable the user to guess the word"""
        for chargeur in self.chargeurs:
            chargeur.data_extraction()
            my_interro = interro.Interro(chargeur)
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
        for chargeur in self.chargeurs:
            chargeur.data_extraction()
            my_interro = interro.Interro(chargeur)
            self.index = random.randint(1, my_interro.words_df.shape[0])
            row = my_interro.get_row()    
            word_guessed = my_interro.guess_word(row, 1, 100)
            # Happy paths
            self.assertIsInstance(word_guessed, bool)
            # Sad paths

    def test_update_voc_df(self):
        """voc_df should be updated according to user's guess"""



class TestTest(unittest.TestCase):
    """Tests on Test class methods."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""
        parser_version = interro.parse_arguments(['-t', 'version'])
        parser_theme = interro.parse_arguments(['-t', 'theme'])
        cls.chargeurs = [interro.Chargeur(parser_version),
                         interro.Chargeur(parser_theme)]

    def test_create_random_step(self):
        """The step should be a random integer"""
        for chargeur in self.chargeurs:
            chargeur.data_extraction()
            my_test = interro.Test(chargeur)
            # Happy paths
            my_test.create_random_step()
            self.assertIsInstance(my_test.step, int)
            self.assertGreater(my_test.step, 0)
            self.assertLess(my_test.step, my_test.words_df.shape[0])
            # Sad paths

    def test_get_next_index(self):
        """Next index should point to a word that was not already asked"""
        for chargeur in self.chargeurs:
            chargeur.data_extraction()
            my_test = interro.Test(chargeur)
            step = my_test.create_random_step()
            index = step
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