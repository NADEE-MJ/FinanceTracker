"""
stock views for the following urls /stock, /stocks, this module can return all
stocks that a user owns, get info on a single stock a user owns, and add,
update, or delete existing stocks a user owns, please see readme.md for info on
how to use api
"""
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models import StockModel, UserModel, add_to_database, delete_from_database

# ?fields for how stock output should be formatted, this is how data will be
# ?formatted, returned when the stock resource is called
RESOURCE_FIELDS = {
    "id": fields.Integer,
    "ticker": fields.String,
    "number_of_shares": fields.Float,
    "cost_per_share": fields.Float,
}

"""
*argument parser for post args
*required args with examples are as follows:
{
    "ticker": "AAPL",
    "number_of_shares": 100.5,
    "cost_per_share": 70.32
}
"""
POST_ARGS = reqparse.RequestParser()
POST_ARGS.add_argument("ticker", type=str, help="Must Include a ticker", required=True)
POST_ARGS.add_argument(
    "number_of_shares", type=float, help="Must Include number_of_shares", required=True
)
POST_ARGS.add_argument(
    "cost_per_share", type=float, help="Must Include number_of_shares", required=True
)

"""
*argument parser for get args
*required args with examples are as follows:
{
"ticker": "AAPL"
}
"""
GET_ARGS = reqparse.RequestParser()
GET_ARGS.add_argument("ticker", type=str, help="Must Include a ticker", required=True)

"""
*argument parser for patch args
*required args with examples are as follows:
{
    "ticker": "AAPL",
    "new_number_of_shares": 40
}
"""
PATCH_ARGS = reqparse.RequestParser()
PATCH_ARGS.add_argument("ticker", type=str, help="Must Include a ticker", required=True)
PATCH_ARGS.add_argument(
    "new_number_of_shares",
    type=float,
    help="Must include new_number_of_shares",
    required=True,
)


class Stocks(Resource):
    @marshal_with(RESOURCE_FIELDS)
    @jwt_required()
    def get(self) -> dict:
        """returns all stocks that a user owns, gets username from jwt payload,
        and queries database for all stocks owned by that user, no args required

        Returns:
            dict: [{stockModel}, {stockModel}...]
            int: status_code == 200
        """
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        stocks = StockModel.query.filter_by(owner_id=current_user.id).all()
        return stocks, 200


class Stock(Resource):
    @marshal_with(RESOURCE_FIELDS)
    @jwt_required()
    def get(self) -> dict:
        """returns info on a certain stock owned by a user, takes GET_ARGS and
        will return info on the stock if the user owns it, otherwise returns
        stock not found

        Returns:
            dict: {stockModel} or {"message": "stock not found"}
            int: status_code == 200 or 404
        """
        args = GET_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        stock = user_has_stock(current_user.id, args["ticker"])
        if stock:
            return stock, 200
        else:
            abort(404, message="stock not found")

    @marshal_with(RESOURCE_FIELDS)
    @jwt_required(fresh=True)
    def post(self) -> dict:
        """add new stock to database under current user, given POST_ARGS first
        check if user already owns that stock, or create new stockModel and
        add it to the database

        Returns:
            dict: {stockModel} or {"message": "user already owns that stock"}
            int: status_code == 201 or 400
        """
        args = POST_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        stock = user_has_stock(current_user.id, args["ticker"])

        if stock:
            abort(
                400,
                message="user already owns that stock, try a patch request to update number of shares or delete to remove it",
            )
        else:
            stock = StockModel(
                ticker=args["ticker"].upper(),
                number_of_shares=args["number_of_shares"],
                cost_per_share=args["cost_per_share"],
                owner_id=current_user.id,
            )

            add_to_database(stock)

            return stock, 201

    @marshal_with(RESOURCE_FIELDS)
    @jwt_required(fresh=True)
    def patch(self) -> dict:
        """updates values for a given stock that a user owns, given PATCH_ARGS
        check if the user owns that stock, if so update number_of_shares, else
        say user does not own that stock

        Returns:
            dict: {stockModel} or {"message": "user does not own that stock"}
            int: status_code == 200, 404
        """
        args = PATCH_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        stock = user_has_stock(current_user.id, args["ticker"])

        if stock:
            stock.update_shares(args["new_number_of_shares"])
            return stock, 200
        else:
            abort(404, message="user does not own that stock")

    @jwt_required(fresh=True)
    def delete(self):
        """deletes a stock that a user owns, given GET_ARGS check if the user
        owns that stock, if so delete it, else say user does not own that stock

        Returns:
            dict: {"message": "successfully deleted" or "user does not own that
            stock"}
            int: status_code == 200, 404
        """
        args = GET_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        stock = user_has_stock(current_user.id, args["ticker"])
        if stock:
            delete_from_database(stock)

            return {"message": f"{stock.ticker} successfully deleted"}
        else:
            abort(404, message="user does not own that stock")


def user_has_stock(id: int, ticker: str) -> object or bool:
    """checks if user owns a certain stock, if they do return that stockModel
    or return false

    Args:
        id (int): id of the user
        ticker (str): ticker of stock being looked up

    Returns:
        object or bool: stockModel or False
    """
    stocks = StockModel.query.filter_by(owner_id=id).all()

    for stock in stocks:
        if stock.ticker == ticker.upper():
            return stock

    return False
