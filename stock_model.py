from app import db
from stock_crypto_apis import get_current_stock_price

class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), unique=True)
    currentPrice = db.Column(db.Float)
    numberOfShares = db.Column(db.Float)
    marketValue = db.Column(db.Float)

    def __repr__(self):
        return f"Stock(ticker = {self.ticker}, currentPrice = {self.currentPrice}, numberOfShares = {self.numberOfShares}, marketValue = {self.marketValue})"

    def updateStock(self):
        self.currentPrice = get_current_stock_price(self.ticker)
        self.marketValue = self.currentPrice * self.numberOfShares
        db.session.commit()

    def updateShares(self, newShares):
        self.numberOfShares = newShares
        self.updateStock()