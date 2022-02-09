from datetime import timedelta
from os import path
from pathlib import Path


def create_code_file():
    code = input("Enter super secret code: ")
    f = open("config\\SUPER_SECRET_CODE.txt", "w")
    f.write(code)
    f.close()
    print("super secret code file created!")
    return code


try:
    f = open("config\\SUPER_SECRET_CODE.txt", "r")
    code = f.readline()
    f.close()
except FileNotFoundError:
    code = create_code_file()

BASE_DIR = Path(path.abspath(path.dirname(__file__)))
PARENT_DIR = BASE_DIR.parent.absolute()

ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=30)

TESTING = True
SECRET_KEY = code
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
JWT_TOKEN_LOCATION = ["json"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(PARENT_DIR, "test_database.db")
