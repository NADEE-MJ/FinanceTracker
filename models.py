from os.path import exists
from sqlalchemy.sql import func
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=False)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    stocks = db.relationship("StockModel", backref="usermodel", passive_deletes=True)
    cryptos = db.relationship("CryptoModel", backref="usermodel", passive_deletes=True)

    def __repr__(self):
        return f"User(email ={self.email}, username = {self.username}, date_created = {self.date_created}, log_in = {self.log_in})"

    def fresh_login(self):
        tokens = {
            "access_token": create_access_token(identity=self.username, fresh=True),
            "refresh_token": create_refresh_token(identity=self.username),
        }

        return tokens

    def stale_login(self):
        """creates a stale access_token using the objects username for the payload

        Returns:
            string: JWT access_token
        """
        token = create_access_token(identity=self.username, fresh=False)

        return token


class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20))
    number_of_shares = db.Column(db.Float)
    cost_per_share = db.Column(db.Float)
    owner = db.Column(
        db.Integer, db.ForeignKey("user_model.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"Stock(ticker = {self.ticker}, number_of_shares = {self.number_of_shares}, cost_per_share = {self.cost_per_share})"

    def update_shares(self, new_shares: float):
        self.number_of_shares = new_shares
        db.session.commit()


class CryptoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20))
    number_of_coins = db.Column(db.Float)
    cost_per_coin = db.Column(db.Float)
    owner = db.Column(
        db.Integer, db.ForeignKey("user_model.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"Stock(symbol = {self.symbol}, number_of_coins = {self.number_of_coins}, cost_per_coin = {self.cost_per_coin})"

    def update_coins(self, new_coins):
        self.number_of_coins = new_coins
        db.session.commit()


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return {"message": "invalid token or token expired"}, 401


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


def add_to_database(item: object):
    db.session.add(item)
    db.session.commit()


def delete_from_database(item: object):
    db.session.delete(item)
    db.session.commit()
