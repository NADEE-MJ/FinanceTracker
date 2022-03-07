"""
config file for production use
"""

from datetime import timedelta
from os import path, environ
from pathlib import Path


BASE_DIR = Path(path.abspath(path.dirname(__file__)))
PARENT_DIR = BASE_DIR.parent.absolute()

ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=30)

RATE_LIMIT = "1/second;500/hour;1000/day"

if environ.get("flask_secret_key") == None:
    print("please set 'flask_secret_key' in your environment variables")
    raise EnvironmentError

SECRET_KEY = environ.get("flask_secret_key")
RATELIMIT_DEFAULT = RATE_LIMIT
SCHEDULER_API_ENABLED = False
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
JWT_TOKEN_LOCATION = ["headers"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(PARENT_DIR, "database.db")

if __name__ == "__main__":
    print(environ.get("flask_secret_key"))
