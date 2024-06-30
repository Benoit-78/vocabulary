import functools

from loguru import logger


def print_arguments_and_output(func):
    """
    Decorator to print function arguments and output.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"function: {func.__name__}")
        if args or kwargs:
            logger.debug(f"args: \nargs={args}")
            logger.debug(f"kwargs: \nkwargs={kwargs}")
        result = func(*args, **kwargs)
        if result is not None:
            logger.debug(f"return: \n{result}")
        return result
    return wrapper
