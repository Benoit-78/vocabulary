"""
    Creation date:
        23rd February 2024
    Creator:
        B. Delorme
    Main purpose:
        Hosts the functions of interro router.
"""

import os
import sys

from fastapi import HTTPException, status
from loguru import logger

REPO_NAME = 'vocabulary'
REPO_DIR = os.getcwd().split(REPO_NAME)[0] + REPO_NAME
if REPO_DIR not in sys.path:
    sys.path.append(REPO_DIR)

from src import interro, views
from src.data import data_handler, users

cred_checker = users.CredChecker()


def load_interro_settings(request, creds: dict):
    """
    API function to load the interro settings.
    """
    user_name = creds.get("userName")
    user_password = creds.get("userPassword")
    # Authenticate user
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Load settings
    result_dict = {
        "request": request,
        "userName": user_name,
        "userPassword": user_password
    }
    return result_dict


def load_test(user_name, db_name, test_type, test_length, password):
    """
    Load the interroooo!
    """
    db_handler = data_handler.DbManipulator(
        user_name=user_name,
        db_name=db_name,
        test_type=test_type,
    )
    db_handler.check_test_type(test_type)
    loader_ = interro.Loader(0, db_handler)
    loader_.load_tables(password)
    guesser = views.FastapiGuesser()
    test_ = interro.Test(
        loader_.tables[loader_.test_type + '_voc'],
        test_length,
        guesser,
        loader_.tables[loader_.test_type + '_perf'],
        loader_.tables[loader_.test_type + '_words_count']
    )
    test_.set_interro_df()
    return loader_, test_


def get_interro_question(
        request,
        user_name,
        user_password,
        db_name,
        test_type,
        total,
        count,
        score
    ):
    """
    API function to load the interro question.
    """
    # Authenticate user
    if user_name:
        cred_checker.check_credentials(user_name, user_password)
    else:
        logger.error("User name not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User name not found."
        )
    # Check input consistency
    try:
        count = int(count)
    except NameError:
        count = 0
    try:
        score = int(score)
    except NameError:
        score = 0
    # Test instanciation
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    test = load_test(user_name, db_name, test_type, total, user_password)[1]
    progress_percent = int(count / int(total) * 100)
    index = test.interro_df.index[count]
    english = test.interro_df.loc[index][0]
    english = english.replace("'", "\'")
    count += 1
    request_dict = {
        "request": request,
        "userName": user_name,
        "numWords": total,
        "count": count,
        "score": score,
        "progressPercent": progress_percent,
        "content_box1": english
    }
    return request_dict



# async def store_object_id_in_session(
#         request: Request,
#         obj: MyObject
#     ):
#     """
#     Storing the object ID in the session
#     """
#     # Generate a unique ID for the object
#     obj_id = str(uuid.uuid4())
#     # Store the object ID in the session
#     session = request.session
#     session["object_id"] = obj_id
#     response = JSONResponse(
#         content={
#             "message": "Object stored in session",
#             "object_id": obj_id
#         }
#     )
#     return response


# async def retrieve_object_from_session(request: Request):
#     """
#     Retrieving an object from the session
#     """
#     # Retrieve the object ID from the session
#     session = request.session
#     obj_id = session.get("object_id")
#     # If the object ID is not found in the session, return an error
#     if not obj_id:
#         raise HTTPException(
#             status_code=404,
#             detail="Object not found in session"
#         )
#     # Retrieve the object from the database or another storage mechanism using the object ID
#     # For demonstration purposes, we'll just create a new object with a name based on the object ID
#     obj = MyObject(name=f"Object_{obj_id}")
#     response = JSONResponse(
#         content={
#             "message": "Object retrieved from session",
#             "object": obj.__dict__
#         }
#     )
#     return response


# Redis

# Limit the Size: Implement logic to limit the number or size of objects stored in memory.
#     For example, you could set a maximum limit on the number of objects a user can store
#     or limit the size of individual objects.

# Expiration: Set expiration times for the stored objects so that they are automatically
#     removed from memory after a certain period. This ensures that memory usage doesn't grow indefinitely.

# Rate Limiting:
#     Implement rate limiting to prevent users from creating an excessive number of objects
#     within a short period. This can help prevent abuse and reduce the risk of OOM errors.

# Separate Data and Behavior:
#     If possible, separate the data and behavior in your classes.
#     Serialize only the data attributes of your objects to JSON, excluding any methods.
#     You can then reconstruct your objects and reattach the methods when deserializing the JSON data.


# import redis

# # Connect to Redis
# redis_db = redis.Redis(
#     host='localhost',
#     port=6379,
#     db=0
# )

# # --------------------------------------------
# # Define a sample object
# data = {
#     'a': 1,
#     'b': 2,
#     'c': 3
# }

# # Serialize the object
# serialized_data = pickle.dumps(data)

# # Store the serialized data in Redis
# redis_db.set('my_data_key', serialized_data)

# # --------------------------------------------
# # Retrieve the serialized data from Redis
# serialized_data = redis_db.get('my_data_key')

# # Deserialize the data
# loaded_data = pickle.loads(serialized_data)

# print(loaded_data)  # Output: {'a': 1, 'b': 2, 'c': 3}
