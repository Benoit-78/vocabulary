"""
    Creation date:
        5th May 2024
    Creator:
        B.DELORME
    Main purpose:
        Interface between the app and the Machine Learning models
"""


def ask_new_words_based_on_worsts():
    """
    Ask the user to provide new words based on the worst words
    """
    words = ['a', 'b', 'c', 'd', 'e']
    return words


def ask_new_words_based_on_bests():
    """
    Ask the user to provide new words based on the best words
    """
    words = ['a', 'b', 'c', 'd', 'e']
    return words


def ask_new_words_based_on_selection(word: str):
    """
    Ask the user to provide new words based:
    - on a chosen word
    - or on a chosen category
    """
    words = [
        'a' + word,
        'b' + word,
        'c' + word,
        'd' + word,
        'e' + word
    ]
    return words


def ask_new_words_based_on_last_added():
    """
    Ask the user to provide new words based on the last words added
    """
    words = ['a', 'b', 'c', 'd', 'e']
    return words


def ask_new_words_based_on_all():
    """
    Ask the user to provide new words based on all words
    """
    words = ['a', 'b', 'c', 'd', 'e']
    return words
