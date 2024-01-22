"""
    Creation date:
        16th December 2023
    Main purpose:

"""

import os
import sys
from abc import ABC, abstractmethod

import pandas as pd
import plotly.express as px
import plotly.io as pio
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)
from src.data.data_handler import DbManipulator



class WordsGraph(ABC):
    """Abstract class for creating and saving user-specific graphs."""
    def __init__(self, db_handler):
        """Constructor should get a database handler"""
        self.db_handler = db_handler
        self.data = pd.DataFrame()

    @abstractmethod
    def set_data(self):
        """Fetch the data that will feed the graph."""

    @abstractmethod
    def create(self):
        """
        Display the data in a graph
        and return this graph as an html file.
        """



class WordsGraph1(WordsGraph):
    """
    Graph that represents the evolution of test performance.
    """
    def set_data(self):
        """See abstract method description"""
        tables = self.db_handler.get_tables()
        voc_table_name = self.db_handler.test_type + '_perf'
        self.data = tables[voc_table_name]

    def correct_data(self):
        """Correct imprecisions or errors in the data"""
        self.data = self.data[self.data['test']<=100]
        self.data = self.data[self.data['test']>=0]

    def create(self):
        """See abstract method description"""
        self.set_data()
        self.correct_data()
        fig = px.scatter(
            x=list(self.data['test_date']),
            y=list(self.data['test']),
            labels={'x': 'Test count', 'y': 'Success rate'},
            title='Graph 1',
            render_mode='webgl',  # Use webgl for scattergl
            template='plotly_dark'  # Set the template to 'plotly_dark' for a black background
        )
        fig.update_traces(
            marker=dict(color='orange', size=5, opacity=0.8, line=dict(color='orange', width=2)),
            selector=dict(mode='markers')
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            width=1000,
            height=500
        )
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html



class WordsGraph2(WordsGraph):
    """
    Graph that represents the success rate of each word
    in function of the number of times it has been asked.
    """
    def set_data(self):
        """See abstract method description"""
        tables = self.db_handler.get_tables()
        voc_table_name = self.db_handler.test_type + '_voc'
        voc_table = tables[voc_table_name]
        self.data = voc_table[[
            self.db_handler.language_1.lower(),
            'nb',
            'taux'
        ]]

    def correct_data(self):
        """Correct imprecisions or errors in the data"""
        self.data = self.data[self.data['taux']<=100]
        self.data = self.data[self.data['taux']>=-100]

    def create(self):
        """See abstract method description"""
        self.set_data()
        self.correct_data()
        fig = px.scatter(
            x=list(self.data['nb']),
            y=list(self.data['taux']),
            labels={
                'x': 'Queries count',
                'y': 'Success rate'
            },
            title='Graph 2',
            render_mode='webgl',  # Use webgl for scattergl
            template='plotly_dark'  # Set the template to 'plotly_dark' for a black background
        )
        fig.update_traces(
            marker=dict(color='orange', size=5, opacity=0.8, line=dict(color='orange', width=2)),
            selector=dict(mode='markers')
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            width=450,
            height=500
        )
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html



class WordsGraph3(WordsGraph):
    """
    Graph that represents the success rate of each word
    in function of its date rank in the words table.
    """
    def set_data(self):
        """See abstract method description"""
        tables = self.db_handler.get_tables()
        voc_table_name = self.db_handler.test_type + '_voc'
        voc_table = tables[voc_table_name]
        self.data = voc_table[[
            self.db_handler.language_1.lower(),
            'taux'
        ]]

    def correct_data(self):
        """Correct imprecisions or errors in the data"""
        self.data = self.data[self.data['taux']<=100]
        self.data = self.data[self.data['taux']>=-100]

    def create(self):
        """See abstract method description"""
        self.set_data()
        self.correct_data()
        fig = px.scatter(
            x=list(self.data.index),
            y=list(self.data['taux']),
            labels={
                'x': 'Order',
                'y': 'Success rate'
            },
            title='Graph 3',
            render_mode='webgl',  # Use webgl for scattergl
            template='plotly_dark'  # Set the template to 'plotly_dark' for a black background
        )
        fig.update_traces(
            marker=dict(color='orange', size=5, opacity=0.8, line=dict(color='orange', width=2)),
            selector=dict(mode='markers')
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            width=1000,
            height=500
        )
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html



class WordsGraph4(WordsGraph):
    """
    Graph that represents the queries count of each word
    in function of its date rank in the words table.
    """
    def set_data(self):
        """See abstract method description"""
        tables = self.db_handler.get_tables()
        voc_table_name = self.db_handler.test_type + '_voc'
        voc_table = tables[voc_table_name]
        self.data = voc_table[[
            self.db_handler.language_1.lower(),
            'nb'
        ]]

    def correct_data(self):
        """Correct imprecisions or errors in the data"""
        self.data = self.data[self.data['nb']>=0]

    def create(self):
        """See abstract method description"""
        self.set_data()
        self.correct_data()
        fig = px.scatter(
            x=list(self.data.index),
            y=list(self.data['nb']),
            labels={
                'x': 'Order',
                'y': 'Queries count'
            },
            title='Graph 4',
            render_mode='webgl',  # Use webgl for scattergl
            template='plotly_dark'  # Set the template to 'plotly_dark' for a black background
        )
        fig.update_traces(
            marker=dict(color='orange', size=5, opacity=0.8, line=dict(color='orange', width=2)),
            selector=dict(mode='markers')
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            width=1000,
            height=500
        )
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html



class WordsGraph5(WordsGraph):
    """
    Graph that represents the queries count of each word
    in function of its date rank in the words table.
    """
    def set_data(self):
        """See abstract method description"""
        tables = self.db_handler.get_tables()
        voc_table_name = self.db_handler.test_type + '_words_count'
        self.data = tables[voc_table_name]

    def correct_data(self):
        """Correct imprecisions or errors in the data"""
        self.data = self.data[self.data['words_count']>=0]

    def create(self):
        """See abstract method description"""
        self.set_data()
        self.correct_data()
        fig = px.scatter(
            x=list(self.data['test_date']),
            y=list(self.data['words_count']),
            labels={
                'x': 'Test date',
                'y': 'Words count'
            },
            title='Graph 5',
            render_mode='webgl',  # Use webgl for scattergl
            template='plotly_dark'  # Set the template to 'plotly_dark' for a black background
        )
        fig.update_traces(
            marker=dict(color='orange', size=5, opacity=0.8, line=dict(color='orange', width=2)),
            selector=dict(mode='markers')
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            width=1000,
            height=500
        )
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html



def load_graphs():
    """Load the user's graphs"""
    html_graphs = []
    # Version
    data_manipulator = DbManipulator(
        host='web_local',
        db_name='english',
        test_type='version'
    )
    # Instanciate
    graph_1 = WordsGraph1(data_manipulator)
    graph_2 = WordsGraph2(data_manipulator)
    graph_3 = WordsGraph3(data_manipulator)
    graph_4 = WordsGraph4(data_manipulator)
    graph_5 = WordsGraph5(data_manipulator)
    # Create graphs
    graph_1_html = graph_1.create()
    graph_2_html = graph_2.create()
    graph_3_html = graph_3.create()
    graph_4_html = graph_4.create()
    graph_5_html = graph_5.create()
    # Save graphs
    html_graphs.append(graph_1_html)
    html_graphs.append(graph_2_html)
    html_graphs.append(graph_3_html)
    html_graphs.append(graph_4_html)
    html_graphs.append(graph_5_html)
    return html_graphs
