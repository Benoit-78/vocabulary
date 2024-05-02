"""
    Author: Benoît DELORME
    Decoupling date: 31st August 2023
    Main purpose: vocabulary application in its CLI version.
"""

import os
import sys

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
sys.path.append(REPO_DIR)

from src import interro
from src import views_local
from src.data import data_handler


def cli_main():
    """Series of instructions executed when the user launches the program from CLI."""
    # Get user settings
    user = interro.CliUser()
    user.get_settings()
    # Load data
    user_name = 'benoit'
    data_handler_ = data_handler.MariaDBHandler(
        user_name,
        user.settings.type,
        'cli',
        'Zhongwen'
    )
    loader = interro.Loader(data_handler_)
    loader.load_tables()
    # WeuuAaaInterrooo !!!
    guesser = views_local.CliGuesser()
    test = interro.PremierTest(
        loader.tables[loader.test_type + '_voc'],
        user.settings.words,
        guesser,
        loader.tables[loader.test_type + '_perf'],
        loader.tables[loader.test_type + '_words_count']
    )
    test.run()
    # Raaattraaaaaaap's !!!!
    rattrap = interro.Rattrap(
        test.faults_df,
        user.settings.rattraps,
        guesser
    )
    rattrap.start_loop()
    # Save the results
    updater = interro.Updater(loader, test)
    updater.update_data()


if __name__ == '__main__':
    cli_main()
