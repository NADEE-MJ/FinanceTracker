from app import db
from flask_login import UserMixin
from os.path import exists
from sqlalchemy.sql import func
from flask_jwt_extended import create_access_token, create_refresh_token

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=False)

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    log_in = db.Column(db.Boolean, default=False)
    stocks = db.relationship('StockModel', backref='usermodel', passive_deletes=True)
    cryptos = db.relationship('CryptoModel', backref='usermodel', passive_deletes=True)

    def __repr__(self):
        return f'User(email ={self.email}, username = {self.username}, date_created = {self.date_created}, log_in = {self.log_in})'

    def login(self):
        self.log_in = True
        db.session.commit()

        additional_claims = {'email': self.email,
                            'id': self.id}

        tokens = {'access_token': create_access_token(identity=self.username, additional_claims=additional_claims), 
                'refresh_token': create_refresh_token(identity=self.username)}

        return tokens

    def logoff(self):
        self.log_in = False
        db.session.commit()

class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20))
    number_of_shares = db.Column(db.Float)
    cost_per_share = db.Column(db.Float)
    owner = db.Column(db.Integer, db.ForeignKey('user_model.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'Stock(ticker = {self.ticker}, number_of_shares = {self.number_of_shares}, cost_per_share = {self.cost_per_share})'

    def update_shares(self, new_shares):
        self.number_of_shares = new_shares
        db.session.commit()

class CryptoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20))
    number_of_coins = db.Column(db.Float)
    cost_per_coin = db.Column(db.Float)
    owner = db.Column(db.Integer, db.ForeignKey('user_model.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'Stock(symbol = {self.symbol}, number_of_coins = {self.number_of_coins}, cost_per_coin = {self.cost_per_coin})'

    def update_coins(self, new_coins):
        self.number_of_coins = new_coins
        db.session.commit()

if __name__ == '__main__':
    if not exists('database.db'):
        print('Creating database tables...')
        db.create_all()
        print('Done!')