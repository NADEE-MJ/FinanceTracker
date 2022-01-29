from app import api, app
from stocks_resource import Stocks
from stock_resource import Stock

api.add_resource(Stocks, '/stocks', methods=['GET'])
api.add_resource(Stock, '/stock', methods=['GET', 'POST', 'DELETE', 'PATCH'])

@app.route('/', methods=['GET'])
def index():
    return 'Finance Tracker API'