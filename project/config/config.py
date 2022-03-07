"""
config file for production use
"""

from datetime import timedelta
from os import path, environ
from pathlib import Path


BASE_DIR = Path(path.abspath(path.dirname(__file__)))
PARENT_DIR = BASE_DIR.parent.parent.absolute()

ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=30)

RATE_LIMIT = "1/second;500/hour;1000/day"

if environ.get("FLASK_SECRET_KEY") == None:
    print("please set 'FLASK_SECRET_KEY' in your environment variables")
    raise EnvironmentError

SECRET_KEY = environ.get("FLASK_SECRET_KEY")
RATELIMIT_DEFAULT = RATE_LIMIT
SCHEDULER_API_ENABLED = False
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
JWT_TOKEN_LOCATION = ["headers"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(PARENT_DIR, "data/database.db")
