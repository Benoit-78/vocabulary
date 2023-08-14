"""
    Background functions for vocabulary program.
"""

import platform


def get_os_type():
    """Get operating system kind: Windows or Linux"""
    operating_system = platform.platform()
    operating_system = operating_system.split('-')[0]
    if operating_system.lower() not in ['windows', 'linux', 'mac', 'android']:
        print("# ERROR: Operating system cannot be identified.")
        raise OSError
    os_type = operating_system
    return os_type


def get_os_separator():
    """Get separator specific to operating system: / or \\ """
    os_type = get_os_type()
    if not isinstance(os_type, str):
        raise TypeError
    if os_type == 'Windows':
        os_sep = '\\'
    elif os_type in ['Linux', 'Mac', 'Android']:
        os_sep = '/'
    else:
        print("# ERROR: Wrong input for operating system.")
        raise NameError
    return os_sep
