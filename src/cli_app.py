"""
    Author: Benoît DELORME
    Decoupling date: 31st August 2023
    Main purpose: vocabulary application in its CLI version.
"""

import interro
from data import data_handler
import views_local


def cli_main():
    """Series of instructions execuated when the user launches the program from CLI."""
    # Get user settings
    user = interro.CliUser()
    user.get_settings()
    # Load data
    data_handler_ = data_handler.MariaDBHandler(user.settings.type)
    loader = interro.Loader(
        user.settings.type,
        user.settings.rattraps,
        data_handler_
    )
    loader.load_tables()
    # WeuuAaaInterrooo !!!
    guesser = views_local.CliGuesser()
    test = interro.Test(
        loader.tables[loader.test_type + '_voc'],
        user.settings.words,
        guesser,
        loader.tables[loader.test_type + '_perf'],
        loader.tables[loader.test_type + '_words_count']
    )
    test.run()
    # Rattraaaaaaap's !!!!
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
