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


class TokenBlocklist(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    jti = DB.Column(DB.String(36), nullable=False)
    revoked_at = DB.Column(DB.DateTime, nullable=False)


# the following two functions with the @JWT decorators run everytime the @jwt_required
# decorator is on a view
@JWT.expired_token_loader
def my_expired_token_callback(JWT_header, JWT_payload) -> dict:
    return {"message": "invalid token or token expired"}, 401


@JWT.token_in_blocklist_loader
def check_if_token_revoked(JWT_header, JWT_payload: dict) -> bool:
    jti = JWT_payload["jti"]
    token = DB.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


from sqlalchemy import event
from sqlalchemy.engine import Engine

# tells sqlite3 to accept foreign keys, this is necessary for sqlite3 to be able
# to cascade delete items that have relationships
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(DBapi_connection, connection_record):
    cursor = DBapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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
