"""
    Author: Benoît Delorme
    Creation date: 10 July 2023
    Main purpose: Listener design pattern.
"""

from collections import defaultdict

events_dict = defaultdict(list)


def add_function_to_event(func, event_type: str):
    """Add the given function to the given event."""
    events_dict[event_type].append(func)


def trigger_event_function_on_data(event_type: str, data):
    """Trigger the function associated with the given event, on the given data."""
    if not event_type in events_dict:
        return None
    for func in events_dict[event_type]:
        return func(data)
