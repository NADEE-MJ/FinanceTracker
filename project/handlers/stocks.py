from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import StockModel, UserModel
from schema import GetStockSchema


class Stocks(Resource):
    # returns all stocks that a user owns
    @jwt_required()
    def get(self) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            stocks = StockModel.get_all_by_owner_id(current_user.id)
            stocksSchema = GetStockSchema(many=True)
            return stocksSchema.dump(stocks), 200
        else:
            abort(404, message="user does not exist")
