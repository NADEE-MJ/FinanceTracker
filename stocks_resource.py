from flask_restful import Resource, marshal_with
from app import resource_fields
from models import StockModel

class Stocks(Resource):
    @marshal_with(resource_fields)
    def get(self):
        update_all_stocks()
        stocks = StockModel.query.all()

        return stocks

def update_all_stocks():
    all_stocks = StockModel.query.all()

    for stock in all_stocks:
        stock.update_stock()