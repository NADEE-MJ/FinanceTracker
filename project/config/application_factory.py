"""
Application factory creates instances of the flask app
"""
from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .errors import register_error_handlers


DB = SQLAlchemy()
JWT = JWTManager()
API = Api()
MA = Marshmallow()
LIMITER = Limiter(key_func=get_remote_address)


def create_app(config_file: str) -> object:
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
    from handlers import Crypto, Cryptos, Stock, Stocks, User, DeleteUser, Refresh

    API.add_resource(Stocks, "/stocks", methods=["GET"])
    API.add_resource(Stock, "/stock", methods=["POST", "GET", "PATCH", "DELETE"])
    API.add_resource(Cryptos, "/cryptos", methods=["GET"])
    API.add_resource(Crypto, "/crypto", methods=["POST", "GET", "PATCH", "DELETE"])
    API.add_resource(User, "/user", methods=["POST", "PUT", "DELETE"])
    API.add_resource(DeleteUser, "/user/delete", methods=["DELETE"])
    API.add_resource(Refresh, "/user/refresh", methods=["PUT"])

    @app.route("/", methods=["GET"])
    def index():
        return {
            "message": "Finance Tracker API",
            "github": "https://github.com/NADEE-MJ/FinanceTracker",
        }
