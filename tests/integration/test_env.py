"""
    Creation date:
        9th October 2024
    Creator:
        Benoît DELORME
    Main purpose:
        Integration tests.
        Test the environment module.
"""

import os

import importlib.metadata
import subprocess
import unittest

ENV_VAR_LIST = [
    'VOC_GUEST_NAME',
    'VOC_DB_ROOT_USR',
    'VOC_DB_ROOT_PWD',
    'VOC_GUEST_DB'
]
PKG_LIST = [
    'awscli2',
    'check-devel',
    'python3',
    'python3-pip',
    'redis',
]
LIB_LIST = [
    # Functional
    'anyio',
    'awscli',
    'bcrypt',
    'botocore',
    'fastapi',
    'Jinja2',
    'mysql-connector-python',
    'numpy',
    'pandas',
    'pydantic',
    'pydantic_core',
    'redis',
    'scipy',
    'SQLAlchemy',
    'starlette',
    'uvicorn',
    # Development
    'loguru',
    'coverage',
    'mypy',
    'mypy-extensions',
    'pip_audit',
    'pytest',
    's3transfer'
]




class TestEnv(unittest.TestCase):
    """
    Check if the local Linux environmnet is correctly set.
    """
    def test_environment_variables(self):
        """
        Test if all necessary environment variables are set.
        """
        for var_name in ENV_VAR_LIST:
            self.assertIn(
                var_name,
                os.environ,
                f"'{var_name}' is not set in the environment variables."
            )
            var_value = os.getenv(var_name)
            self.assertIsNotNone(
                var_value,
                f"'{var_name}' should have a value"
            )

    def test_packages(self):
        """
        Test if all necessary packages are installed.
        """
        for pkg_name in PKG_LIST:
            self.assertTrue(
                check_package_installed(pkg_name),
                f"'{pkg_name}' is not installed."
            )

    def test_libraries_installed(self):
        for library in LIB_LIST:
            self.assertTrue(
                is_library_installed(library), 
                f"'{library}' is not installed."
            )



def check_package_installed(package_name):
        """
        Helper function to check if a package is installed
        """
        result = subprocess.run(
            ['rpm', '-q', package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # If the package is not found, dpkg returns a non-zero exit code
        return result.returncode == 0


def is_library_installed(library_name: str) -> bool:
    """
    Raise an exception if the package is not installed.
    """
    try:
        importlib.metadata.version(library_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False
