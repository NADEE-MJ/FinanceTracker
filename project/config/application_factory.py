"""
Application factory is used to create instances of the flask app, all the views
are passed into the create_app function which can be configured for real world
usage or testing, then it is returned for use in other modules
"""
from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import DB, JWT

API = Api()
LIMITER = Limiter(key_func=get_remote_address)


def create_app(config_file: str) -> object:
    """creates flask app from config_file, adds views, initializes API, LIMITER,
    JWT, and DB objects with the app

    Args:
        config_file (str): should be a config.py file, there are two examples in
        the config folder one for testing and one for running the server

    Returns:
        object: flask app instance
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    create_views(app)

    DB.init_app(app)
    JWT.init_app(app)
    API.init_app(app)
    LIMITER.init_app(app)

    return app


def create_views(app: object) -> None:
    """adds views to flask app using API resources from the flask_restful module
    and using the built-in flask routes

    Args:
        app (object): flask app instance

    Returns:
        None: modifies object in place
    """
    # import resources
    from handlers.crypto import Crypto, Cryptos
    from handlers.stock import Stock, Stocks
    from handlers.user import User, DeleteUser, Refresh

    # Tell flask API what urls access which resources
    API.add_resource(Stocks, "/stocks", methods=["GET"])
    API.add_resource(Stock, "/stock", methods=["POST", "GET", "PATCH", "DELETE"])
    API.add_resource(Cryptos, "/cryptos", methods=["GET"])
    API.add_resource(Crypto, "/crypto", methods=["POST", "GET", "PATCH", "DELETE"])
    API.add_resource(User, "/user", methods=["POST", "PUT", "DELETE"])
    API.add_resource(DeleteUser, "/user/delete", methods=["DELETE"])
    API.add_resource(Refresh, "/user/refresh", methods=["PUT"])

    # extra routes
    @app.route("/", methods=["GET"])
    def index():
        return {
            "message": "Finance Tracker API",
            "github": "https://github.com/NADEE-MJ/FinanceTracker",
        }
