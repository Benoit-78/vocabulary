
from loguru import logger



def get_error_messages(error_message: str) -> tuple:
    """
    Based on the result of the POST method, returns the corresponding error messages
    that will feed the sign-in html page.
    """
    messages = [
        "User successfully authenticated",
        "Unknown user",
        "Password incorrect",
        ''
    ]
    if error_message == messages[0]:
        result = ("", "")
    elif error_message == messages[1]:
        result = ("Unknown user name", "")
    elif error_message == messages[2]:
        result = ("", "Password incorrect")
    elif error_message == messages[3]:
        result = ("", "")
    else:
        logger.error(f"Error message incorrect: {error_message}")
        logger.error(f"Should be in: {messages}")
    return result
