from flask_restful import Resource, marshal_with
from app import resourceFields
from stock_model import StockModel

class Stocks(Resource):
    @marshal_with(resourceFields)
    def get(self):
        updateAllStocks()
        stocks = StockModel.query.all()

        return stocks

def updateAllStocks():
    allStocks = StockModel.query.all()

    for stock in allStocks:
        stock.updateStock()