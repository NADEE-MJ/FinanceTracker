"""
config file for production use
"""

from datetime import timedelta
from os import path
from pathlib import Path


def create_code_file() -> str:
    """creates a secret code file to store the secret code used to generate JWT
    tokens

    Returns:
        str: secret code
    """
    code = input("Enter super secret code: ")
    f = open("SUPER_SECRET_CODE.txt", "w")
    f.write(code)
    f.close()
    print("super secret code file created!")
    return code


# Try to load super secret code from file
try:
    f = open("SUPER_SECRET_CODE.txt", "r")
    SECRET_CODE = f.readline()
    f.close()
except FileNotFoundError:
    SECRET_CODE = create_code_file()

# determine where to store database, by default in the main directory
BASE_DIR = Path(path.abspath(path.dirname(__file__)))
PARENT_DIR = BASE_DIR.parent.absolute()

# access and refresh token expiration
ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=30)

# default rate limiting amounts (requests / unit of time)
RATE_LIMIT = "1/second;500/hour;1000/day"

# !flask config settings do not change variable names
SECRET_KEY = SECRET_CODE
RATELIMIT_DEFAULT = RATE_LIMIT
SCHEDULER_API_ENABLED = False
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
JWT_TOKEN_LOCATION = ["headers"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(PARENT_DIR, "database.db")
