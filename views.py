from re import U
from app import api, app
from handlers.stocks import Stocks
from handlers.cryptos import Cryptos
from handlers.stock import Stock
from handlers.user import User

api.add_resource(Stocks, '/stocks', methods=['GET'])
api.add_resource(Stock, '/stock', methods=['POST', 'GET', 'PATCH', 'DELETE'])
api.add_resource(User, '/user', methods=['POST', 'PUT', 'DELETE'])

@app.route('/', methods=['GET'])
def index():
    return 'Finance Tracker API'