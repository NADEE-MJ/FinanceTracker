from flask_restful import Resource, reqparse, marshal_with, abort
from app import resource_fields, db
from models import StockModel
from stock_crypto_apis import get_current_stock_price

stock_post_args = reqparse.RequestParser()
stock_post_args.add_argument('ticker', type=str, help='Must Include a ticker', required=True)
stock_post_args.add_argument('number_of_shares', type=float, help='Must Include number_of_shares', required=True)

stock_get_args = reqparse.RequestParser()
stock_get_args.add_argument('id', type=int)
stock_get_args.add_argument('ticker', type=str)

stock_patch_args = reqparse.RequestParser()
stock_patch_args.add_argument('id', type=int)
stock_patch_args.add_argument('ticker', type=str)
stock_patch_args.add_argument('new_number_of_shares', type=float, help='must include new_number_of_shares', required=True)

class Stock(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = stock_get_args.parse_args()
        stock = exists_in_db(args)
        stock.update_stock()

        return stock

    @marshal_with(resource_fields)
    def post(self):
        args = stock_post_args.parse_args()
        post_check(args)

        current_price = get_current_stock_price(args['ticker'])
        market_value = args['number_of_shares'] * current_price
        stock = StockModel(ticker = args['ticker'].upper(), current_price = current_price, number_of_shares = args['number_of_shares'], market_value = market_value)

        db.session.add(stock)
        db.session.commit()

        return stock, 201

    @marshal_with(resource_fields)
    def patch(self):
        args = stock_patch_args.parse_args()
        stock = exists_in_db(args)

        stock.update_shares(args['new_number_of_shares'])

        return stock, 200

    def delete(self):
        args = stock_get_args.parse_args()
        stock = exists_in_db(args)

        db.session.delete(stock)
        db.session.commit()

        message = {'message' : '%s successfully deleted' % (stock.ticker)}

        return message

def post_check(args):
    stock = StockModel.query.filter_by(ticker=args['ticker'].upper()).first()
    if stock:
        if stock.ticker == args['ticker'].upper():
            abort(409, message='stock already in database use patch or delete to change')
    
    current_price = get_current_stock_price(args['ticker'])
    if not current_price:
        abort(404, message='not a valid stock ticker')
    
    return current_price

def exists_in_db(args):
    if args['id']:
        stock = StockModel.query.get_or_404(args['id'])
    elif args['ticker']:
        stock = StockModel.query.filter_by(ticker=args['ticker'].upper()).first_or_404()
    else:
        abort(400, message='please give a ticker or id to lookup stock')
    
    return stock