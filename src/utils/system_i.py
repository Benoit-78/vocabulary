"""
    Background functions for vocabulary program.
"""

import platform

from loguru import logger


def get_os_type():
    """
    Get operating system kind: Windows or Linux
    """
    os_type = platform.platform()
    os_type = os_type.split('-')[0]
    if os_type.lower() not in ['windows', 'linux', 'mac', 'android']:
        logger.error("Operating system cannot be identified.")
        logger.warning("Operating system was arbitrarily set to 'linux'.")
    return os_type


def get_os_separator():
    """
    Get separator specific to operating system.
    """
    os_type = get_os_type()
    if os_type == 'Windows':
        os_sep = '\\'
    elif os_type in ['Linux', 'Mac', 'Android']:
        os_sep = '/'
    else:
        print("# ERROR: Wrong input for operating system.")
        raise NameError
    return os_sep
