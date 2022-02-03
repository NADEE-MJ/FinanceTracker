"""
This file creates the path structure for the API to follow, using the api wrapper from flask_RESTful and the app object from flask
api.add_resource takes a class that inherits from Resource(part of flask_RESTful) and maps the methods in it to an 
HTTP method post, patch, put etc... so when the api call is made to that path it runs the different fuction based
on what method the request was sent with

@app.route is a function decorator that creates a path that when accessed runs the function directly after it
"""

from app import api, app

from handlers.crypto import Crypto, Cryptos
from handlers.stock import Stock, Stocks
from handlers.user import User, Refresh

api.add_resource(Stocks, "/stocks", methods=["GET"])
api.add_resource(Stock, "/stock", methods=["POST", "GET", "PATCH", "DELETE"])
api.add_resource(Cryptos, "/cryptos", methods=["GET"])
api.add_resource(Crypto, "/crypto", methods=["POST", "GET", "PATCH", "DELETE"])
api.add_resource(User, "/user", methods=["POST", "PUT", "DELETE"])
api.add_resource(Refresh, "/user/refresh", methods=["PUT"])


@app.route("/", methods=["GET"])
def index():
    return {
        "message": "Finance Tracker API",
        "github": "https://github.com/NADEE-MJ/FinanceTracker",
    }
