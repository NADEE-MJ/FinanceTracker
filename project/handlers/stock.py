from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from schema import GetStockSchema, PostStockSchema, PatchStockSchema
from webargs.flaskparser import use_args

from models import StockModel, UserModel, add_to_database, delete_from_database


SCHEMA = GetStockSchema()


class Stock(Resource):
    # returns info on a certain stock owned by a user
    @use_args(GetStockSchema())
    @jwt_required()
    def get(self, args) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            stock = current_user.owns_stock(args["ticker"])
            if stock:
                return SCHEMA.dump(stock), 200
            else:
                abort(404, message="stock not found")
        else:
            abort(404, message="user does not exist")

    # adds new stock to database for current user
    @use_args(PostStockSchema())
    @jwt_required(fresh=True)
    def post(self, args) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            stock = current_user.owns_stock(args["ticker"])

            if stock:
                abort(
                    400,
                    message=(
                        "user already owns that stock, try a patch request"
                        "to update number of shares or delete to remove it"
                    ),
                )
            else:
                stock = StockModel(
                    ticker=args["ticker"].upper(),
                    number_of_shares=args["number_of_shares"],
                    cost_per_share=args["cost_per_share"],
                    owner_id=current_user.id,
                )

                add_to_database(stock)

                return SCHEMA.dump(stock), 201
        else:
            abort(404, message="user does not exist")

    # updates number_of_shares for a given stock that a user owns
    @use_args(PatchStockSchema())
    @jwt_required(fresh=True)
    def patch(self, args) -> dict:
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        if current_user:
            stock = current_user.owns_stock(args["ticker"])

            if stock:
                stock.update_shares(args["new_number_of_shares"])
                return SCHEMA.dump(stock), 200
            else:
                abort(404, message="user does not own that stock")
        else:
            abort(404, message="user does not exist")

    # deletes a stock that a user owns
    @use_args(GetStockSchema())
    @jwt_required(fresh=True)
    def delete(self, args):
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            stock = current_user.owns_stock(args["ticker"])
            if stock:
                delete_from_database(stock)

                return {"message": f"{stock.ticker} successfully deleted"}
            else:
                abort(404, message="user does not own that stock")
        else:
            abort(404, message="user does not exist")
