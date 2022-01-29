import imp
from app import db
from os.path import exists
from stock_crypto_apis import get_current_stock_price

class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), unique=True)
    current_price = db.Column(db.Float)
    number_of_shares = db.Column(db.Float)
    market_value = db.Column(db.Float)

    def __repr__(self):
        return f'Stock(ticker = {self.ticker}, current_price = {self.current_price}, number_of_shares = {self.number_of_shares}, market_value = {self.market_value})'

    def update_stock(self):
        self.current_price = get_current_stock_price(self.ticker)
        self.market_value = self.current_price * self.number_of_shares
        db.session.commit()

    def update_shares(self, new_shares):
        self.number_of_shares = new_shares
        self.update_stock()

if not exists('database.db'):
    print('Creating database tables...')
    db.create_all()
    print('Done!')