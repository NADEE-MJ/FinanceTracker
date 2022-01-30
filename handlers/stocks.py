from flask_login import current_user
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required, get_jwt
from app import stock_resource_fields
from models import StockModel
from handlers.user import get_current_user

class Stocks(Resource):
    @marshal_with(stock_resource_fields)
    @jwt_required()
    def get(self):
        current_user = get_current_user(get_jwt()['id'])
        stocks = StockModel.query.filter_by(owner=current_user.id).all()
        return stocks, 201