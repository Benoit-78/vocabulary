#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creator: B.Delorme
Mail: delormebenoit211@gmail.com
Creation date: 11th March 2023
Main purpose: test script for interro.py, main script of vocabulary application
"""

import unittest
import numpy as np
import pandas as pd

import interro



class TestInterro(unittest.TestCase):
    """Interro script tests."""
    @classmethod
    def setUpClass(cls):
        """Run once before all tests."""

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite."""

    def setUp(self):
        """Runs before each test."""

    def tearDown(self):
        """Runs once after each test case."""

    def test_check_test_type(self):
        """The given test kind should be either version or theme"""
        # Happy paths
        version_case = interro.check_test_type('version')
        self.assertEqual(version_case, 'version')
        theme_case= interro.check_test_type('theme')
        self.assertEqual(theme_case, 'theme')
        # Sad paths
        with self.assertRaises(TypeError):
            interro.check_test_type(np.nan)
        with self.assertRaises(TypeError):
            interro.check_test_type(None)
        with self.assertRaises(ValueError):
            interro.check_test_type('')
        with self.assertRaises(TypeError):
            interro.check_test_type(7)
        with self.assertRaises(NameError):
            interro.check_test_type('versio')

    def test_get_os_type(self):
        """Operating system should be either Windows or Linux"""
        # Happy paths
        # global operating_system
        operating_system = interro.get_os_type()
        self.assertIn(operating_system, ['Windows', 'Linux', 'Mac', 'Android'])
        # Sad paths
        with self.assertRaises(AssertionError):
            self.assertEqual(operating_system, 'Ubuntu')

    def test_get_os_separator(self):
        """Separator should be OS-specific"""
        # Happy paths
        windows_case = interro.get_os_separator('Windows')
        self.assertEqual(windows_case, '\\')
        linux_case = interro.get_os_separator('Linux')
        self.assertEqual(linux_case, '/')
        # Sad paths
        with self.assertRaises(TypeError):
            interro.get_os_separator(['Windows', 'Linux'])
        with self.assertRaises(TypeError):
            interro.get_os_separator(None)
        with self.assertRaises(NameError):
            interro.get_os_separator('Delorme OS')

    def test_get_data_paths(self):
        """Data paths should exist"""
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_types = ['theme', 'version']
        for test_type in test_types:
            # Happy paths
            paths = interro.get_data_paths(os_sep, test_type)
            self.assertIsInstance(paths, dict)
            self.assertEqual(len(paths), 4)
            for _, path in paths.items():
                self.assertIsInstance(path, str)
            # Sad paths

    def test_get_data(self):
        """Data should be correctly loaded"""
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_types = ['theme', 'version']
        for test_type in test_types:
            paths = interro.get_data_paths(os_sep, test_type)
            data = interro.get_data(paths)
            # Happy paths
            self.assertIsInstance(data, dict)
            self.assertEqual(len(data), 4)
            for df_name, data in data.items():
                self.assertIn(df_name, ['voc', 'perf', 'word_cnt', 'test_cnt'])
                self.assertIsInstance(data, type(pd.DataFrame()))
            # Sad paths

    def test_data_preprocessing(self):
        """Input should be a dataframe, and it should be added a query column"""
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_types = ['theme', 'version']
        for test_type in test_types:
            paths = interro.get_data_paths(os_sep, test_type)
            data = interro.get_data(paths)
            voc_df = data['voc']
            # Happy paths
            self.assertIn('Date', list(voc_df.columns))
            voc_df = interro.data_preprocessing(voc_df)
            self.assertIn('Query', list(voc_df.columns))
            self.assertEqual(voc_df[voc_df.columns[0]].dtype, object)
            self.assertEqual(voc_df[voc_df.columns[1]].dtype, object)
            self.assertEqual(voc_df['Taux'].dtype, np.float64)
            self.assertGreater(voc_df.shape[0], 1)
            # Sad paths
 
    def test_create_random_step(self):
        """The step should be a random integer"""
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_kinds = ['theme', 'version']
        for test_kind in test_kinds:
            paths = interro.get_data_paths(os_sep, test_kind)
            data = interro.get_data(paths)
            voc_df = data['voc']
            # Happy paths            
            self.assertGreater(voc_df.shape[0], 0)
            step = interro.create_random_step(voc_df)
            self.assertIsInstance(step, int)
            self.assertGreater(step, 0)
            # Sad paths

    def test_get_next_index(self):
        """Next index should point to a word that was not already asked"""
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_kinds = ['theme', 'version']
        for test_kind in test_kinds:
            paths = interro.get_data_paths(os_sep, test_kind)
            data = interro.get_data(paths)
            voc_df = data['voc']
            voc_df = interro.data_preprocessing(voc_df)
            step = interro.create_random_step(voc_df)
            index = step
            for i in range(1, 101):
                # Happy paths
                next_index = interro.get_next_index(index, step, voc_df)
                self.assertIsInstance(next_index, int)
                self.assertGreater(next_index, 1)
                self.assertLess(next_index, voc_df.shape[0])
                self.assertEqual(voc_df['Query'].loc[next_index], 0)
                # Sad paths

    def test_get_row(self):
        """The returned row should enable the user to guess the word"""
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_kinds = ['theme', 'version']
        for test_kind in test_kinds:
            paths = interro.get_data_paths(os_sep, test_kind)
            data = interro.get_data(paths)
            voc_df = data['voc']
            voc_df = interro.data_preprocessing(voc_df)
            step = interro.create_random_step(voc_df)
            index = step
            for i in range(1, 101):
                next_index = interro.get_next_index(index, step, voc_df)
                row = interro.get_row(voc_df, next_index)
                # Happy paths
                self.assertIsInstance(row, list)
                self.assertEqual(len(row), 3)
                self.assertIsInstance(row[0], str)
                self.assertIsInstance(row[1], str)
                self.assertIsInstance(row[2], float)
                # Sad paths
        
    def test_guess_word(self):
        """The result should be either True or False"""
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_kinds = ['theme', 'version']
        for test_kind in test_kinds:
            paths = interro.get_data_paths(os_sep, test_kind)
            data = interro.get_data(paths)
            voc_df = data['voc']
            voc_df = interro.data_preprocessing(voc_df)
            step = interro.create_random_step(voc_df)
            index = step
            for i in range(1, 101):
                print("# DEBUG i", i)
                print("# DEBUG index", index)
                next_index = interro.get_next_index(index, step, voc_df)
                word_guessed = interro.guess_word(voc_df, next_index, i)
                # Happy paths
                self.assertIsInstance(word_guessed, bool)
                # Sad paths

    def test_update_voc_df(self):
        """voc_df should be updated according to user's guess"""
        
        
