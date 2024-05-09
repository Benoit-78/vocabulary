"""
    Creator:
        B.Delorme
    Creation date:
        20th April 2024
    Main purpose:
        Test script for 
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.api import dashboard as dashboard_api
from src.data import database_interface


class TestDashboard(unittest.TestCase):
    @patch('src.api.dashboard.load_graphs')
    def test_get_user_dashboards(self, mock_load_graphs):
        # ----- ARRANGE
        request = 'mock_request'
        user_name = 'mock_user_name'
        user_password = 'mock_pwd'
        db_name = 'mock_db_name'
        mock_load_graphs.return_value = [1, 2, 3, 4, 5]
        # ----- ACT
        result = dashboard_api.get_user_dashboards(
            request,
            user_name,
            user_password,
            db_name
        )
        # ----- ASSERT
        self.assertIsInstance(result, dict)
        mock_load_graphs.assert_called_once_with(
            user_name,
            user_password,
            db_name
        )
        expected_dict = {
            "request": 'mock_request',
            "graph_1": 1,
            "graph_2": 2,
            "graph_3": 3,
            "graph_4": 4,
            "graph_5": 5,
            "userName": 'mock_user_name',
            "userPassword": 'mock_pwd'
        }
        self.assertEqual(result, expected_dict)

    def test_load_graphs(self):
        # Mock the DbManipulator instance# ----- ARRANGE
        mock_data_manipulator = MagicMock(spec=dashboard_api.DbManipulator)
        mock_graph_1 = MagicMock(spec=dashboard_api.WordsGraph1)
        mock_graph_1.create.return_value = "<div>Graph 1 HTML</div>"
        mock_graph_2 = MagicMock(spec=dashboard_api.WordsGraph2)
        mock_graph_2.create.return_value = "<div>Graph 2 HTML</div>"
        mock_graph_3 = MagicMock(spec=dashboard_api.WordsGraph3)
        mock_graph_3.create.return_value = "<div>Graph 3 HTML</div>"
        mock_graph_4 = MagicMock(spec=dashboard_api.WordsGraph4)
        mock_graph_4.create.return_value = "<div>Graph 4 HTML</div>"
        mock_graph_5 = MagicMock(spec=dashboard_api.WordsGraph5)
        mock_graph_5.create.return_value = "<div>Graph 5 HTML</div>"
        with unittest.mock.patch.multiple(
            "src.api.dashboard",
            WordsGraph1=mock_graph_1,
            WordsGraph2=mock_graph_2,
            WordsGraph3=mock_graph_3,
            WordsGraph4=mock_graph_4,
            WordsGraph5=mock_graph_5,
        ):
            # ----- ACT
            result = dashboard_api.load_graphs(
                "user_name",
                "user_password",
                "db_name"
            )
            # ----- ASSERT
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 5)



class TestWordsGraph1(unittest.TestCase):
    """
    Test class for WordsGraph1
    """
    def setUp(self):
        user_name = 'mock_user_name'
        db_name = 'mock_db_name'
        test_type = 'mock_test_type'
        db_handler = database_interface.DbManipulator(
            user_name,
            db_name,
            test_type
        )
        self.graph = dashboard_api.WordsGraph1(db_handler)

    def test_init(self):
        # ----- ARRANGE
        # ----- ACT
        # ----- ASSERT
        self.assertTrue(hasattr(self.graph, 'db_handler'))
        self.assertTrue(hasattr(self.graph, 'data'))

    @patch('src.api.dashboard.DbManipulator.get_tables')
    def test_set_data(self, mock_get_tables):
        # ----- ARRANGE
        password = 'mock_password'
        mock_df = pd.DataFrame({
            'col_1': [1, 2, 3],
            'col_2': [4, 5, 6]
        })
        mock_get_tables.return_value = {
            'mock_test_type_perf': mock_df,
            'table_2': pd.DataFrame(),
        }
        # ----- ACT
        self.graph.set_data(password)
        # ----- ASSERT
        pd.testing.assert_frame_equal(self.graph.data, mock_df)

    def test_correct_data(self):
        # ----- ARRANGE
        mock_df_before = pd.DataFrame({
            'test': [101, 2, 3, -1],
            'col_2': [4, 5, 6, 7]
        })
        self.graph.data = mock_df_before
        # ----- ACT
        self.graph.correct_data()
        # ----- ASSERT
        mock_df_after = pd.DataFrame(
            data={
                'test': [2, 3,],
                'col_2': [5, 6]
            },
            index=[1, 2]
        )
        logger.debug(f"graph.data : \n{self.graph.data}")
        logger.debug(f"mock_df_after : \n{mock_df_after}")
        pd.testing.assert_frame_equal(self.graph.data, mock_df_after)

    # @patch('src.api.dashboard.px.scatter')
    # @patch('src.api.dashboard.WordsGraph1.correct_data')
    # @patch('src.api.dashboard.WordsGraph1.set_data')
    # def test_create_method(
    #         self,
    #         mock_set_data,
    #         mock_correct_data,
    #         mock_px_scatter
    #     ):
    #     # ----- ARRANGE
    #     self.graph.data = pd.DataFrame({
    #         'test_date': [1, 2, 3],
    #         'test': [4, 5, 6]
    #     })
    #     mock_set_data.return_value = True
    #     mock_correct_data.return_value = True
    #     mock_px_scatter.return_value = MagicMock()
    #     # ----- ACT
    #     graph_html = self.graph.create("test_password")
    #     # ----- ASSERT
    #     self.assertTrue('<html>' in graph_html)
    #     self.assertTrue('<script>' in graph_html)
    #     # self.assertIn("Graph 1", graph_html)
    #     # self.assertIn("Test count", graph_html)
    #     # self.assertIn("Success rate", graph_html)
    #     # self.assertIn("plotly_dark", graph_html)
    #     mock_set_data.assert_called_once_with("test_password")
    #     mock_correct_data.assert_called_once()



class TestWordsGraph2(unittest.TestCase):
    def setUp(self):
        user_name = 'mockusername'
        db_name = 'mockdbname'
        test_type = 'mocktesttype'
        db_handler = database_interface.DbManipulator(
            user_name,
            db_name,
            test_type
        )
        self.graph = dashboard_api.WordsGraph2(db_handler)

    @patch('src.api.dashboard.DbManipulator.get_tables')
    def test_set_data(self, mock_get_tables):
        # ----- ARRANGE
        password = 'mock_password'
        mock_df = pd.DataFrame({
            'mockdbname': [1, 2, 3],
            'nb': [4, 5, 6],
            'taux': [4, 5, 6]
        })
        mock_get_tables.return_value = {
            'mocktesttype_voc': mock_df,
            'table_2': pd.DataFrame(),
        }
        # ----- ACT
        self.graph.set_data(password)
        # ----- ASSERT
        pd.testing.assert_frame_equal(self.graph.data, mock_df)

    def test_correct_data(self):
        # ----- ARRANGE
        mock_df_before = pd.DataFrame({
            'taux': [101, 2, 3, -101],
            'col_2': [4, 5, 6, 7]
        })
        self.graph.data = mock_df_before
        # ----- ACT
        self.graph.correct_data()
        # ----- ASSERT
        mock_df_after = pd.DataFrame(
            data={
                'taux': [2, 3,],
                'col_2': [5, 6]
            },
            index=[1, 2]
        )
        logger.debug(f"graph.data : \n{self.graph.data}")
        logger.debug(f"mock_df_after : \n{mock_df_after}")
        pd.testing.assert_frame_equal(self.graph.data, mock_df_after)



class TestWordsGraph3(unittest.TestCase):
    def setUp(self):
        user_name = 'mockusername'
        db_name = 'mockdbname'
        test_type = 'mocktesttype'
        db_handler = database_interface.DbManipulator(
            user_name,
            db_name,
            test_type
        )
        self.graph = dashboard_api.WordsGraph3(db_handler)

    @patch('src.api.dashboard.DbManipulator.get_tables')
    def test_set_data(self, mock_get_tables):
        # ----- ARRANGE
        password = 'mock_password'
        mock_df = pd.DataFrame({
            'mockdbname': [1, 2, 3],
            'taux': [4, 5, 6]
        })
        mock_get_tables.return_value = {
            'mocktesttype_voc': mock_df,
            'table_2': pd.DataFrame(),
        }
        # ----- ACT
        self.graph.set_data(password)
        # ----- ASSERT
        pd.testing.assert_frame_equal(self.graph.data, mock_df)

    def test_correct_data(self):
        # ----- ARRANGE
        mock_df_before = pd.DataFrame({
            'taux': [101, 2, 3, -101],
            'col_2': [4, 5, 6, 7]
        })
        self.graph.data = mock_df_before
        # ----- ACT
        self.graph.correct_data()
        # ----- ASSERT
        mock_df_after = pd.DataFrame(
            data={
                'taux': [2, 3,],
                'col_2': [5, 6]
            },
            index=[1, 2]
        )
        pd.testing.assert_frame_equal(self.graph.data, mock_df_after)



class TestWordsGraph4(unittest.TestCase):
    def setUp(self):
        user_name = 'mockusername'
        db_name = 'mockdbname'
        test_type = 'mocktesttype'
        db_handler = database_interface.DbManipulator(
            user_name,
            db_name,
            test_type
        )
        self.graph = dashboard_api.WordsGraph4(db_handler)

    @patch('src.api.dashboard.DbManipulator.get_tables')
    def test_set_data(self, mock_get_tables):
        # ----- ARRANGE
        password = 'mock_password'
        mock_df = pd.DataFrame({
            'mockdbname': [1, 2, 3],
            'nb': [4, 5, 6]
        })
        mock_get_tables.return_value = {
            'mocktesttype_voc': mock_df,
            'table_2': pd.DataFrame(),
        }
        # ----- ACT
        self.graph.set_data(password)
        # ----- ASSERT
        pd.testing.assert_frame_equal(self.graph.data, mock_df)

    def test_correct_data(self):
        # ----- ARRANGE
        mock_df_before = pd.DataFrame({
            'nb': [101, 2, 3, -101],
            'col_2': [4, 5, 6, 7]
        })
        self.graph.data = mock_df_before
        # ----- ACT
        self.graph.correct_data()
        # ----- ASSERT
        mock_df_after = pd.DataFrame(
            data={
                'nb': [101, 2, 3,],
                'col_2': [4, 5, 6]
            },
            index=[0, 1, 2]
        )
        pd.testing.assert_frame_equal(self.graph.data, mock_df_after)



class TestWordsGraph5(unittest.TestCase):
    def setUp(self):
        user_name = 'mockusername'
        db_name = 'mockdbname'
        test_type = 'mocktesttype'
        db_handler = database_interface.DbManipulator(
            user_name,
            db_name,
            test_type
        )
        self.graph = dashboard_api.WordsGraph5(db_handler)

    @patch('src.api.dashboard.DbManipulator.get_tables')
    def test_set_data(self, mock_get_tables):
        # ----- ARRANGE
        password = 'mock_password'
        mock_df = pd.DataFrame({
            'mockdbname': [1, 2, 3],
            'words_count': [4, 5, 6]
        })
        mock_get_tables.return_value = {
            'mocktesttype_words_count': mock_df,
            'table_2': pd.DataFrame(),
        }
        # ----- ACT
        self.graph.set_data(password)
        # ----- ASSERT
        pd.testing.assert_frame_equal(self.graph.data, mock_df)

    def test_correct_data(self):
        # ----- ARRANGE
        mock_df_before = pd.DataFrame({
            'words_count': [101, 2, 3, -101],
            'col_2': [4, 5, 6, 7]
        })
        self.graph.data = mock_df_before
        # ----- ACT
        self.graph.correct_data()
        # ----- ASSERT
        mock_df_after = pd.DataFrame(
            data={
                'words_count': [101, 2, 3,],
                'col_2': [4, 5, 6]
            },
            index=[0, 1, 2]
        )
        pd.testing.assert_frame_equal(self.graph.data, mock_df_after)