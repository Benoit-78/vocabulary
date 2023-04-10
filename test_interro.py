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
import sys

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

    # def test_check_test_type(self):
    #     """The given test kind should be either version or theme"""
    #     # Happy paths
    #     version_case = interro.check_test_type('version')
    #     self.assertEqual(version_case, 'version')
    #     theme_case= interro.check_test_type('theme')
    #     self.assertEqual(theme_case, 'theme')
    #     # Sad paths
    #     with self.assertRaises(TypeError):
    #         interro.check_test_type(['interro.py', np.nan])
    #     with self.assertRaises(TypeError):
    #         interro.check_test_type(['interro.py', None])
    #     with self.assertRaises(ValueError):
    #         interro.check_test_type(['interro.py', ''])
    #     with self.assertRaises(TypeError):
    #         interro.check_test_type(['interro.py', 7])
    #     with self.assertRaises(NameError):
    #         interro.check_test_type(['interro.py', 'versio'])

    def test_get_os_type(self):
        """Operating system should be either Windows or Linux"""
        # Happy paths
        operating_system = interro.get_os_type()
        self.assertIn(operating_system, ['Windows', 'Linux', 'Mac', 'Android'])
        # Sad paths

    def test_get_os_separator(self):
        """Separator should be OS-specific"""
        # Happy paths
        windows_case = interro.get_os_separator('Windows')
        self.assertEqual(windows_case, '\\')
        linux_case = interro.get_os_separator('Linux')
        self.assertEqual(linux_case, '/')
        # Sad paths
        with self.assertRaises(NameError):
            interro.get_os_separator('Delorme OS')
        with self.assertRaises(TypeError):
            interro.get_os_separator(['Windows', 'Linux'])

    def test_get_data_paths(self):
        """Data paths should exist"""
        # Happy paths
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_types = ['theme', 'version']
        for test_type in test_types:
            paths = interro.get_data_paths(os_sep, test_type)
            self.assertIsInstance(paths, dict)
            self.assertEqual(len(paths), 4)
            for _, path in paths.items():
                self.assertIsInstance(path, str)
        # Sad paths

    def test_get_data(self):
        """Data should be correctly loaded"""
        # Happy paths
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_types = ['theme', 'version']
        for test_type in test_types:
            paths = interro.get_data_paths(os_sep, test_type)
            data = interro.get_data(paths)
            self.assertIsInstance(data, dict)
            self.assertEqual(len(data), 4)
            for df_name, data in data.items():
                self.assertIn(df_name, ['voc', 'perf', 'word_cnt', 'test_cnt'])
                self.assertIsInstance(data, type(pd.DataFrame()))
        # Sad paths

    def test_data_processing(self):
        """Input should be a dataframe, and it should be added a query column"""
        # Happy paths
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_types = ['theme', 'version']
        for test_type in test_types:
            paths = interro.get_data_paths(os_sep, test_type)
            data = interro.get_data(paths)
            voc_df = data['voc']
            self.assertIn('Date', list(voc_df.columns))
            voc_df = interro.data_processing(voc_df)
            self.assertIn('Query', list(voc_df.columns))
            self.assertEqual(voc_df[voc_df.columns[0]].dtype, object)
            self.assertEqual(voc_df[voc_df.columns[1]].dtype, object)
            self.assertEqual(voc_df['Taux'].dtype, np.float64)
        # Sad paths

 
    def test_create_random_step(self):
        """The step should be a random integer"""
        # Happy paths
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_kinds = ['theme', 'version']
        for test_kind in test_kinds:
            paths = interro.get_data_paths(os_sep, test_kind)
            data = interro.get_data(paths)
            voc_df = data['voc']
            self.assertGreater(voc_df.shape[0], 0)
            step = interro.create_random_step(voc_df)
            self.assertIsInstance(step, int)
            self.assertGreater(step, 0)
        # Sad paths

    def test_get_next_index(self):
        """Next index should point to a word that was not already asked"""
        # Happy paths
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_kinds = ['theme', 'version']
        for test_kind in test_kinds:
            paths = interro.get_data_paths(os_sep, test_kind)
            data = interro.get_data(paths)
            voc_df = data['voc']
            voc_df = interro.data_processing(voc_df)
            self.assertGreater(voc_df.shape[0], 1)
            step = interro.create_random_step(voc_df)
            index = step
            for i in range(1, 101):
                next_index = interro.get_next_index(index, step, voc_df)
                self.assertIsInstance(next_index, int)
                self.assertGreater(next_index, 0)
                self.assertLess(next_index, voc_df.shape[0])
        # Sad paths

    def test_get_row(self):
        """The returned row should enable the user to guess the word"""
        # Happy paths
        operating_system = interro.get_os_type()
        os_sep = interro.get_os_separator(operating_system)
        test_kinds = ['theme', 'version']
        for test_kind in test_kinds:
            paths = interro.get_data_paths(os_sep, test_kind)
            data = interro.get_data(paths)
            voc_df = data['voc']
            voc_df = interro.data_processing(voc_df)
            step = interro.create_random_step(voc_df)
            index = step
            for i in range(1, 101):
                next_index = interro.get_next_index(index, step, voc_df)
                row = interro.get_row(voc_df, next_index)
                self.assertIsInstance(row, list)
                self.assertEqual(len(row), 3)
                self.assertIsInstance(row[0], str)
                self.assertIsInstance(row[1], str)
                self.assertIsInstance(row[2], float)
        # Sad paths

    # def test_guess_word(self):
    #     """The result should be either True or False"""
    #     # Happy paths
    #     operating_system = interro.get_os_type()
    #     os_sep = interro.get_os_separator(operating_system)
    #     test_kinds = ['theme', 'version']
    #     for test_kind in test_kinds:
    #         paths = interro.get_data_paths(os_sep, test_kind)
    #         data = interro.get_data(paths)
    #         voc_df = data['voc']
    #         voc_df = interro.data_processing(voc_df)
    #         step = interro.create_random_step(voc_df)
    #         index = step
    #         for i in range(1, 101):
    #             next_index = interro.get_next_index(index, step, voc_df)
    #             word_guessed = interro.guess_word(voc_df, next_index, i)
    #             self.assertIsInstance(word_guessed, bool)
    #     # Sad paths

