"""
config file for testing purposes, do not use for production, does not include
rate limiting by default
"""

from datetime import timedelta
from os import path, environ
from pathlib import Path


# determine where to store database, by default in the main directory
BASE_DIR = Path(path.abspath(path.dirname(__file__)))
PARENT_DIR = BASE_DIR.parent.parent.absolute()

# access and refresh token expiration
ACCESS_EXPIRES = timedelta(seconds=2)
REFRESH_EXPIRES = timedelta(seconds=2)

# !flask config settings do not change variable names
TESTING = True

if environ.get("flask_secret_key") == None:
    print("please set 'flask_secret_key' in your environment variables")
    raise EnvironmentError

SECRET_KEY = environ.get("flask_secret_key_test")
RATELIMIT_ENABLED = False
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
JWT_TOKEN_LOCATION = ["json"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(PARENT_DIR, "data/test_database.db")
