from .event import subscribe


def create_word(user, table):
    """Add a word to the table"""
    pass


def read_word(user, word):
    """Read the given word"""
    pass


def update_word(user, word):
    """Update statistics on the given word"""
    pass


def copy_word(user):
    pass


def delete_word(user):
    pass


def setup_database_event_handlers():
    subscribe("add_word", create_word)
    subscribe("ask_word", read_word)
    subscribe("update_word", update_word)
    subscribe("copy_word", copy_word)
    subscribe("delete_word", delete_word)