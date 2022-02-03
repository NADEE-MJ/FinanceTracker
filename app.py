"""
This is the main api file, run this file to start the server, in the if statement at the bottom there are options
for how to run the flask api server.
"""

from flask import Flask
from flask_restful import Api, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from datetime import timedelta

# creates the flask app object which runs the whole api
app = Flask(__name__)

# constant variables for how long the access and refresh token last before they expire
ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=30)

# creates the SUPER_SECRET_CODE.txt file that is used by flask_jwt_extended for encoding data and saves it in main directory
def create_code_file():
    code = input("Enter super secret code: ")
    f = open("SUPER_SECRET_CODE.txt", "w")
    f.write(code)
    f.close()
    print("super secret code file created!")
    return code


# tries to get code from SUPER_SECRET_CODE.txt if not run function to create it
try:
    f = open("SUPER_SECRET_CODE.txt", "r")
    code = f.readline()
    f.close()
except FileNotFoundError:
    code = create_code_file()

# configuring flask, flask_sqlalchemy, and flask_jwt_extended variables
app.config["SECRET_KEY"] = code
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = REFRESH_EXPIRES
app.config["JWT_TOKEN_LOCATION"] = ["json"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# object wrapper for use by flask_jwt_extended
jwt = JWTManager(app)

# object wrapper for use by flask_RESTful
api = Api(app)

# object wrapper for use by flask_sqlalchemy
db = SQLAlchemy(app)

limiter = Limiter(app, key_func=get_remote_address, default_limits=["1 per second"])

# tells api how to format stock output
stock_resource_fields = {
    "id": fields.Integer,
    "ticker": fields.String,
    "number_of_shares": fields.Float,
    "cost_per_share": fields.Float,
}

# tells api how to format crypto output
crypto_resource_fields = {
    "id": fields.Integer,
    "symbol": fields.String,
    "number_of_coins": fields.Float,
    "cost_per_coin": fields.Float,
}

if __name__ == "__main__":
    from views import *

    # different ways to start flask server
    app.run(debug=True)  # localhost
    # app.run(debug=True, host='0.0.0.0')  # host on network
    # app.run(host='0.0.0.0')  # host on network no debug
