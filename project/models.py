"""
stores all the different models for the different data types the app uses, this
includes TokenBlocklist, UserModel, StockModel, and CryptoModel
"""
from sqlalchemy.sql import func
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()
JWT = JWTManager()


class TokenBlocklist(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    jti = DB.Column(DB.String(36), nullable=False)
    revoked_at = DB.Column(DB.DateTime, nullable=False)


class UserModel(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(150), unique=True)
    username = DB.Column(DB.String(150), unique=True)
    password = DB.Column(DB.String(150))
    date_created = DB.Column(DB.DateTime(timezone=True), default=func.now())
    # one to many relationship with stocks and cryptos
    stocks = DB.relationship(
        "StockModel",
        back_populates="owner",
        cascade="all, delete",
        passive_deletes=True,
    )
    cryptos = DB.relationship(
        "CryptoModel",
        back_populates="owner",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"User(email ={self.email}, username = {self.username}, date_created = {self.date_created}, log_in = {self.log_in})"

    def fresh_login(self) -> dict:
        """generates fresh access token and refresh token for user with their
        username as the payload

        Returns:
            dict: dict of access_token and refresh_token
        """
        tokens = {
            "access_token": create_access_token(identity=self.username, fresh=True),
            "refresh_token": create_refresh_token(identity=self.username),
        }

        return tokens

    def stale_login(self) -> dict:
        """creates a stale access_token using the username for the payload

        Returns:
            string: access_token
        """
        token = create_access_token(identity=self.username, fresh=False)

        return token


class StockModel(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    ticker = DB.Column(DB.String(20))
    number_of_shares = DB.Column(DB.Float)
    cost_per_share = DB.Column(DB.Float)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey("user_model.id", ondelete="CASCADE"))
    owner = DB.relationship("UserModel", back_populates="stocks")

    def __repr__(self) -> str:
        return f"Stock(ticker = {self.ticker}, number_of_shares = {self.number_of_shares}, cost_per_share = {self.cost_per_share})"

    def update_shares(self, new_shares: float) -> None:
        """updates number of shares in the database

        Args:
            new_shares (float): new number of shares the user owns of that stock
        """
        self.number_of_shares = new_shares
        DB.session.commit()


class CryptoModel(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    symbol = DB.Column(DB.String(20))
    number_of_coins = DB.Column(DB.Float)
    cost_per_coin = DB.Column(DB.Float)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey("user_model.id", ondelete="CASCADE"))
    owner = DB.relationship("UserModel", back_populates="cryptos")

    def __repr__(self) -> str:
        return f"Stock(symbol = {self.symbol}, number_of_coins = {self.number_of_coins}, cost_per_coin = {self.cost_per_coin})"

    def update_coins(self, new_coins: float) -> None:
        """updates number of coins the database

        Args:
            new_coins (float): new number of coins the user owns of that crypto
        """
        self.number_of_coins = new_coins
        DB.session.commit()


# tells sqlite3 to accept foreign keys, this is necessary for sqlite3 to be able
# to cascade delete items that have relationships
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(DBapi_connection, connection_record):
    cursor = DBapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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


def add_to_database(item: object) -> None:
    DB.session.add(item)
    DB.session.commit()


def delete_from_database(item: object) -> None:
    DB.session.delete(item)
    DB.session.commit()
