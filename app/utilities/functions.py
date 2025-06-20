#  standard library imports
import os


def is_development() -> bool:
    """
    Check if the application is running in development mode.
    """

    return os.getenv('FLASK_ENV') == 'development'
