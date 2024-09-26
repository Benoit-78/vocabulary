"""
    Creation date:
        16th December 2023
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro router.
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
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src.data.database_interface import DbQuerier



class WordsGraph(ABC):
    """
    Abstract class for creating and saving user-specific graphs.
    """
    def __init__(self, db_querier):
        """
        Constructor should get a database handler.
        """
        self.db_querier = db_querier
        self.data = pd.DataFrame()

    @abstractmethod
    def set_data(self, user_password):
        """
        Fetch the data that will feed the graph.
        """

    @abstractmethod
    def create(self, user_password):
        """
        Display the data in a graph
        and return this graph as an html file.
        """



class WordsGraph1(WordsGraph):
    """
    Graph that represents the evolution of test performance.
    """
    def set_data(self, user_password):
        """
        See abstract method description
        """
        tables = self.db_querier.get_tables(user_password)
        voc_table_name = self.db_querier.test_type + '_perf'
        self.data = tables[voc_table_name]

    def correct_data(self):
        """
        Correct imprecisions or errors in the data
        """
        self.data = self.data[self.data['test']<=100]
        self.data = self.data[self.data['test']>=0]

    def create(self, user_password):
        """
        See abstract method description
        """
        self.set_data(user_password)
        self.correct_data()
        fig = px.scatter(
            x=list(self.data['test_date']),
            y=list(self.data['test']),
            labels={'x': 'Test count', 'y': 'Success rate'},
            title='Graph 1',
            render_mode='webgl',
            template='plotly_dark'
        )
        fig.update_traces(
            marker={
                'color': 'orange',
                'size': 5,
                'opacity': 0.8,
                'line': {'color': 'orange', 'width': 2}
            },
            selector={'mode': 'markers'}
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': 'white'},
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
    def set_data(self, user_password):
        """
        See abstract method description.
        """
        tables = self.db_querier.get_tables(user_password)
        voc_table_name = self.db_querier.test_type + '_voc'
        voc_table = tables[voc_table_name]
        db_name_short = self.db_querier.db_name.split('_')[1]
        self.data = voc_table[[
            db_name_short,
            'nb',
            'taux'
        ]]

    def correct_data(self):
        """Correct imprecisions or errors in the data"""
        self.data = self.data[self.data['taux']<=100]
        self.data = self.data[self.data['taux']>=-100]

    def create(self, user_password):
        """See abstract method description"""
        self.set_data(user_password)
        self.correct_data()
        fig = px.scatter(
            x=list(self.data['nb']),
            y=list(self.data['taux']),
            labels={
                'x': 'Queries count',
                'y': 'Success rate'
            },
            title='Graph 2',
            render_mode='webgl',
            template='plotly_dark'
        )
        fig.update_traces(
            marker={
                'color': 'orange',
                'size': 5,
                'opacity': 0.8,
                'line': {'color': 'orange', 'width': 2}
            },
            selector={'mode': 'markers'}
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={
                'color': 'white'
            },
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
    def set_data(self, user_password):
        """
        See abstract method description
        """
        tables = self.db_querier.get_tables(user_password)
        voc_table_name = self.db_querier.test_type + '_voc'
        voc_table = tables[voc_table_name]
        db_name_short = self.db_querier.db_name.split('_')[1]
        self.data = voc_table[[
            db_name_short,
            'taux'
        ]]

    def correct_data(self):
        """
        Correct imprecisions or errors in the data
        """
        self.data = self.data[self.data['taux']<=100]
        self.data = self.data[self.data['taux']>=-100]

    def create(self, user_password):
        """See abstract method description"""
        self.set_data(user_password)
        self.correct_data()
        fig = px.scatter(
            x=list(self.data.index),
            y=list(self.data['taux']),
            labels={
                'x': 'Order',
                'y': 'Success rate'
            },
            title='Graph 3',
            render_mode='webgl',
            template='plotly_dark'
        )
        fig.update_traces(
            marker={
                'color': 'orange',
                'size': 5,
                'opacity': 0.8,
                'line': {'color': 'orange', 'width': 2}
            },
            selector={'mode': 'markers'}
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': 'white'},
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
    def set_data(self, user_password):
        """
        See abstract method description
        """
        tables = self.db_querier.get_tables(user_password)
        voc_table_name = self.db_querier.test_type + '_voc'
        voc_table = tables[voc_table_name]
        db_name_short = self.db_querier.db_name.split('_')[1]
        self.data = voc_table[[
            db_name_short,
            'nb'
        ]]

    def correct_data(self):
        """
        Correct imprecisions or errors in the data
        """
        self.data = self.data[self.data['nb']>=0]

    def create(self, user_password):
        """
        See abstract method description
        """
        self.set_data(user_password)
        self.correct_data()
        fig = px.scatter(
            x=list(self.data.index),
            y=list(self.data['nb']),
            labels={
                'x': 'Order',
                'y': 'Queries count'
            },
            title='Graph 4',
            render_mode='webgl',
            template='plotly_dark'
        )
        fig.update_traces(
            marker={
                'color': 'orange',
                'size': 5,
                'opacity': 0.8,
                'line': {'color': 'orange', 'width': 2}
            },
            selector={'mode': 'markers'}
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': 'white'},
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
    def set_data(self, user_password):
        """
        See abstract method description
        """
        tables = self.db_querier.get_tables(user_password)
        voc_table_name = self.db_querier.test_type + '_words_count'
        self.data = tables[voc_table_name]

    def correct_data(self):
        """
        Correct imprecisions or errors in the data
        """
        self.data = self.data[self.data['words_count']>=0]

    def create(self, user_password):
        """
        See abstract method description
        """
        self.set_data(user_password)
        self.correct_data()
        fig = px.scatter(
            x=list(self.data['test_date']),
            y=list(self.data['words_count']),
            labels={
                'x': 'Test date',
                'y': 'Words count'
            },
            title='Graph 5',
            render_mode='webgl',
            template='plotly_dark'
        )
        fig.update_traces(
            marker={
                'color': 'orange',
                'size': 5,
                'opacity': 0.8,
                'line': {'color': 'orange', 'width': 2}
            },
            selector={'mode': 'markers'}
        )
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': 'white'},
            width=1000,
            height=500
        )
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html



def get_user_dashboards(
        request,
        user_name,
        user_password,
        db_name
    ):
    """
    Get the user dashboards.
    """
    logger.info(f"User: {user_name}")
    graphs = load_graphs(
        user_name=user_name,
        user_password=user_password,
        db_name=db_name
    )
    request_dict = {
        "request": request,
        "graph_1": graphs[0],
        "graph_2": graphs[1],
        "graph_3": graphs[2],
        "graph_4": graphs[3],
        "graph_5": graphs[4],
        "userName": user_name,
        "userPassword": user_password
    }
    return request_dict


def load_graphs(user_name, user_password, db_name):
    """
    Load the user's graphs.
    """
    html_graphs = []
    # Version
    data_querier = DbQuerier(
        user_name=user_name,
        db_name=db_name,
        test_type='version'
    )
    # Instanciate
    graph_1 = WordsGraph1(db_querier=data_querier)
    graph_2 = WordsGraph2(db_querier=data_querier)
    graph_3 = WordsGraph3(db_querier=data_querier)
    graph_4 = WordsGraph4(db_querier=data_querier)
    graph_5 = WordsGraph5(db_querier=data_querier)
    # Create graphs
    graph_1_html = graph_1.create(user_password=user_password)
    graph_2_html = graph_2.create(user_password=user_password)
    graph_3_html = graph_3.create(user_password=user_password)
    graph_4_html = graph_4.create(user_password=user_password)
    graph_5_html = graph_5.create(user_password=user_password)
    # Save graphs
    html_graphs.append(graph_1_html)
    html_graphs.append(graph_2_html)
    html_graphs.append(graph_3_html)
    html_graphs.append(graph_4_html)
    html_graphs.append(graph_5_html)
    return html_graphs
