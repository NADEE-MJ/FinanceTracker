"""
Application factory creates instances of the flask app
"""
from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_marshmallow import Marshmallow
from flask_limiter.util import get_remote_address

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .errors import register_error_handlers


DB = SQLAlchemy()
JWT = JWTManager()
API = Api()
MA = Marshmallow()
LIMITER = Limiter(key_func=get_remote_address)


def create_app(config_file: str) -> object:
    """creates flask app from config_file, adds views, initializes API, LIMITER,
    JWT, and DB objects with the app

    Args:
        config_file (str): should be a config.py file, there are two examples in
        the config folder one for testing and one for running a production server

    Returns:
        object: flask app instance
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    create_views(app)
    register_error_handlers(app)

    DB.init_app(app)
    MA.init_app(app)
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
    from handlers import Crypto, Cryptos, Stock, Stocks, User, DeleteUser, Refresh

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
