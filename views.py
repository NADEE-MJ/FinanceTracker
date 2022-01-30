from app import api, app
from handlers.crypto import Crypto, Cryptos
from handlers.stock import Stock, Stocks
from handlers.user import User, Refresh

api.add_resource(Stocks, '/stocks', methods=['GET'])
api.add_resource(Stock, '/stock', methods=['POST', 'GET', 'PATCH', 'DELETE'])
api.add_resource(User, '/user', methods=['POST', 'PUT', 'DELETE'])
api.add_resource(Refresh, '/user/refresh', methods=['PUT'])

@app.route('/', methods=['GET'])
def index():
    return 'Finance Tracker API'