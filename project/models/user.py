from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.sql import func

from config import DB
from . import StockModel, CryptoModel


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

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def __repr__(self) -> str:
        return f"User(email = {self.email}, username = {self.username}, date_created = {self.date_created})"

    def fresh_login(self) -> dict:
        tokens = {
            "access_token": create_access_token(identity=self.username, fresh=True),
            "refresh_token": create_refresh_token(identity=self.username),
        }

        return tokens

    def stale_login(self) -> dict:
        token = create_access_token(identity=self.username, fresh=False)

        return {"access_token": token}

    def owns_stock(self, ticker: str) -> object or bool:
        stocks = StockModel.get_by_owner_id(self.id)

        for stock in stocks:
            if stock.ticker == ticker.upper():
                return stock

        return False

    def owns_crypto(self, symbol: str) -> object or bool:
        cryptos = CryptoModel.get_by_owner_id(self.id)

        for crypto in cryptos:
            if crypto.symbol == symbol.upper():
                return crypto

        return False
