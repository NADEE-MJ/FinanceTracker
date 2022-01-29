from flask_restful import Resource, reqparse, marshal_with, abort
from app import resourceFields, db
from stock_model import StockModel
from stock_crypto_apis import get_current_stock_price

stockPostArgs = reqparse.RequestParser()
stockPostArgs.add_argument("ticker", type=str, help="Must Include a ticker", required=True)
stockPostArgs.add_argument("numberOfShares", type=float, help="Must Include numberOfShares", required=True)

stockGetArgs = reqparse.RequestParser()
stockGetArgs.add_argument("id", type=int)
stockGetArgs.add_argument("ticker", type=str)

stockPatchArgs = reqparse.RequestParser()
stockPatchArgs.add_argument("id", type=int)
stockPatchArgs.add_argument("ticker", type=str)
stockPatchArgs.add_argument("newNumberOfShares", type=float, help="must include newNumberOfShares", required=True)

class Stock(Resource):
    @marshal_with(resourceFields)
    def get(self):
        args = stockGetArgs.parse_args()
        stock = existsInDB(args)
        stock.updateStock()

        return stock

    @marshal_with(resourceFields)
    def post(self):
        args = stockPostArgs.parse_args()
        postCheck(args)

        currentPrice = get_current_stock_price(args['ticker'])
        marketValue = args['numberOfShares'] * currentPrice
        stock = StockModel(ticker = args['ticker'].upper(), currentPrice = currentPrice, numberOfShares = args['numberOfShares'], marketValue = marketValue)

        db.session.add(stock)
        db.session.commit()

        return stock, 201

    @marshal_with(resourceFields)
    def patch(self):
        args = stockPatchArgs.parse_args()
        stock = existsInDB(args)

        stock.updateShares(args['newNumberOfShares'])

        return stock, 200

    def delete(self):
        args = stockGetArgs.parse_args()
        stock = existsInDB(args)

        db.session.delete(stock)
        db.session.commit()

        message = {"message" : "%s successfully deleted" % (stock.ticker)}

        return message

def postCheck(args):
    stock = StockModel.query.filter_by(ticker=args['ticker'].upper()).first()
    if stock:
        if stock.ticker == args['ticker'].upper():
            abort(409, message="stock already in database use patch or delete to change")
    
    currentPrice = get_current_stock_price(args['ticker'])
    if not currentPrice:
        abort(404, message="not a valid stock ticker")
    
    return currentPrice

def existsInDB(args):
    if args['id']:
        stock = StockModel.query.get_or_404(args['id'])
    elif args['ticker']:
        stock = StockModel.query.filter_by(ticker=args['ticker'].upper()).first_or_404()
    else:
        abort(400, message="please give a ticker or id to lookup stock")
    
    return stock