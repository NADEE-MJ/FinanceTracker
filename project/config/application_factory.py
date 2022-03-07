"""
Application factory creates instances of the flask app
"""
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .errors import register_error_handlers


DB = SQLAlchemy()
JWT = JWTManager()
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
    LIMITER.init_app(app)

    return app


def create_views(app: object) -> None:
    from handlers import Crypto, Cryptos, Stock, Stocks, User, DeleteUser, Refresh

    user_rule = "/api/user"
    app.add_url_rule(
        rule=user_rule + "/all-stocks",
        endpoint="all-stocks",
        view_func=Stocks.as_view("all-stocks"),
    )
    app.add_url_rule(
        rule=user_rule + "/stock", endpoint="stock", view_func=Stock.as_view("stock")
    )
    app.add_url_rule(
        rule=user_rule + "/all-cryptos",
        endpoint="all-cryptos",
        view_func=Cryptos.as_view("all-cryptos"),
    )
    app.add_url_rule(
        rule=user_rule + "/crypto",
        endpoint="crypto",
        view_func=Crypto.as_view("crypto"),
    )
    app.add_url_rule(
        rule=user_rule + "/logon",
        endpoint="logon",
        view_func=User.as_view("user"),
    )
    app.add_url_rule(
        rule=user_rule + "/delete",
        endpoint="delete",
        view_func=DeleteUser.as_view("delete"),
    )
    app.add_url_rule(
        rule=user_rule + "/refresh",
        endpoint="refresh",
        view_func=Refresh.as_view("refresh"),
    )

    @app.route("/", methods=["GET"])
    def index():
        return {
            "message": "Finance Tracker API",
            "github": "https://github.com/NADEE-MJ/FinanceTracker",
        }
