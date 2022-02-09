from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models import db, jwt

# !move to somewhere else or maybe stay here idk
api = Api()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1 per second", "500 per hour", "1000 per day"],
)


def create_app(config_file: str):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    create_views(app)

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    limiter.init_app(app)

    return app


def create_views(app):
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
