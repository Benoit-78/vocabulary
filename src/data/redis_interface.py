"""
    Creator:
        B.DELORME
    Creation date:
        20th April 2024
    Main purpose:
        Redis interface for storing and loading tests and loaders.
"""

import pickle
import redis

REDIS_DB = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)


def save_interro_in_redis(interro, token, interro_category, redis_db=REDIS_DB):
    """
    Save a test object in redis using token as key.
    """
    interro = pickle.dumps(interro)
    key = token + '_' + interro_category
    redis_db.set(key, interro)


def load_interro_from_redis(token, interro_category, redis_db=REDIS_DB):
    """
    Load a test object from redis using token as key.
    """
    key = token + '_' + interro_category
    pickelized_test = redis_db.get(key)
    interro = pickle.loads(pickelized_test)
    return interro


def save_loader_in_redis(loader, token, redis_db=REDIS_DB):
    """
    Save a loader object in redis using token as key.
    """
    loader = pickle.dumps(loader)
    redis_db.set(token + '_loader', loader)


def load_loader_from_redis(token, redis_db=REDIS_DB):
    """
    Load a test object from redis using token as key.
    """
    pickelized_loader = redis_db.get(token + '_loader')
    loader = pickle.loads(pickelized_loader)
    return loader
