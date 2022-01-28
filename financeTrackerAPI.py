from inspect import ArgSpec
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import yfinance as yf

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), unique=True)
    currentPrice = db.Column(db.Float)
    numberOfShares = db.Column(db.Float)
    marketValue = db.Column(db.Float)

    def __repr__(self):
        return f"Stock(ticker = {self.ticker}, currentPrice = {self.currentPrice}, numberOfShares = {self.numberOfShares}, marketValue = {self.marketValue})"

#Run the following line the first time you run the script to create the database file then comment it out again
# db.create_all()

stockPostArgs = reqparse.RequestParser()
stockPostArgs.add_argument("ticker", type=str, help="Must Include a ticker", required=True)
stockPostArgs.add_argument("numberOfShares", type=float, help="Must Include numberOfShares", required=True)

stockGetArgs = reqparse.RequestParser()
stockGetArgs.add_argument("id", type=int)
stockGetArgs.add_argument("ticker", type=str)

resourceFields = {
    'id': fields.Integer,
    'ticker': fields.String,
    'currentPrice': fields.Float,
    'numberOfShares': fields.Float,
    'marketValue': fields.Float
}

class Stocks(Resource):
    @marshal_with(resourceFields)
    def get(self):
        stocks = StockModel.query.all()

        return stocks

class Stock(Resource):
    @marshal_with(resourceFields)
    def get(self):
        args = stockGetArgs.parse_args()
        stock = existsInDB(args)

        return stock

    @marshal_with(resourceFields)
    def post(self):
        args = stockPostArgs.parse_args()
        tempStock = StockModel.query.filter_by(ticker=args['ticker'].upper()).first()
        if tempStock:
            if tempStock.ticker.lower() == args['ticker'].lower():
                abort(409, message="stock already in database use patch or delete to change")

        currentPrice = yf.Ticker(args['ticker']).info.get('regularMarketPrice', {})
        marketValue = args['numberOfShares'] * currentPrice
        stock = StockModel(ticker = args['ticker'].upper(), currentPrice = currentPrice, numberOfShares = args['numberOfShares'], marketValue = marketValue)

        db.session.add(stock)
        db.session.commit()

        return stock, 201

    def delete(self):
        args = stockGetArgs.parse_args()
        stock = existsInDB(args)

        db.session.delete(stock)
        db.session.commit()

        message = {"message" : "%s successfully deleted" % (stock.ticker)}

        return message

def existsInDB(args):
    if args['id']:
        stock = StockModel.query.get_or_404(args['id'])
    elif args['ticker']:
        stock = StockModel.query.filter_by(ticker=args['ticker'].upper()).first_or_404()
    else:
        abort(400, message="please give a ticker or id to lookup stock")
    
    return stock

api.add_resource(Stocks, "/stocks", methods=["GET"])
api.add_resource(Stock, "/stock", methods=["GET", "POST", "DELETE"])

@app.route("/", methods=["GET"])
def index():
    return "Finance Tracker API"

if __name__ == "__main__":
    # app.run(debug=True) #LocalHost
    app.run(debug=True, host="0.0.0.0") #host on Network
    # app.run(host="0.0.0.0") #host on network no debug