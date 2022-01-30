from flask_login import current_user
from flask_restful import Resource, reqparse, marshal_with, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy import false
from app import stock_resource_fields, db, jwt
from models import StockModel, TokenBlocklist
from handlers.user import get_current_user

stock_post_args = reqparse.RequestParser()
stock_post_args.add_argument('ticker', type=str, help='Must Include a ticker', required=True)
stock_post_args.add_argument('number_of_shares', type=float, help='Must Include number_of_shares', required=True)
stock_post_args.add_argument('cost_per_share', type=float, help='Must Include number_of_shares', required=True)

stock_get_args = reqparse.RequestParser()
stock_get_args.add_argument('ticker', type=str, help='Must Include a ticker', required=True)

stock_patch_args = reqparse.RequestParser()
stock_patch_args.add_argument('ticker', type=str, help='Must Include a ticker', required=True)
stock_patch_args.add_argument('new_number_of_shares', type=float, help='must include new_number_of_shares', required=True)

class Stock(Resource):
    @marshal_with(stock_resource_fields)
    @jwt_required()
    def get(self):
        args = stock_get_args.parse_args()
        stock = user_has_stock(get_jwt()['id'], args['ticker'])
        if stock:
            return stock, 200
        
        abort(404, message="stock not found")
        
    @marshal_with(stock_resource_fields)
    @jwt_required()
    def post(self):
        args = stock_post_args.parse_args()
        stock = user_has_stock(get_jwt()['id'], args['ticker'])
        if stock:
            abort(400, message='user already owns that stock, try a patch request to update number of shares or delete to remove it')

        stock = StockModel(ticker=args['ticker'].upper(), number_of_shares=args['number_of_shares'], cost_per_share=args['cost_per_share'], owner=get_jwt()['id'])

        db.session.add(stock)
        db.session.commit()

        return stock, 201

    @marshal_with(stock_resource_fields)
    @jwt_required()
    def patch(self):
        current_user = get_jwt_identity()
        print(current_user)
        args = stock_patch_args.parse_args()
        stock = user_has_stock(get_jwt()['id'], args['ticker'])
        if stock:
            stock.update_shares(args['new_number_of_shares'])
            return stock, 200
        
        abort(404, message='user does not own that stock')

    @jwt_required()
    def delete(self):
        args = stock_get_args.parse_args()
        stock = user_has_stock(get_jwt()['id'], args['ticker'])
        if stock:
            db.session.delete(stock)
            db.session.commit()

            return {'message' : f'{stock.ticker} successfully deleted'}

        abort(404, message='user does not own that stock')

def user_has_stock(id, ticker):
    current_user = get_current_user(id)
    stocks = StockModel.query.filter_by(owner=current_user.id).all()
    for stock in stocks:
        if stock.ticker == ticker.upper():
            return stock
    return False