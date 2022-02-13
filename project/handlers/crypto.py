"""
crypto views for the following urls /crypto, /cryptos, this module can return all
cryptos that a user owns, get info on a single crypto a user owns, and add,
update, or delete cryptos for a user, please see readme.md for info on
how to use api
"""
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import CryptoModel, UserModel, delete_from_database, add_to_database

# ?fields for how crypto output should be formatted, this is how data will be
# ?returned when the crypto resource is called
RESOURCE_FIELDS = {
    "id": fields.Integer,
    "symbol": fields.String,
    "number_of_coins": fields.Float,
    "cost_per_coin": fields.Float,
}

"""
*argument parser for post args
*required args with examples are as follows:
{
    "symbol": "BTC",
    "number_of_coins": 33.2,
    "cost_per_coin": 34,000.23
}
"""
POST_ARGS = reqparse.RequestParser()
POST_ARGS.add_argument("symbol", type=str, help="Must Include a symbol", required=True)
POST_ARGS.add_argument(
    "number_of_coins", type=float, help="Must Include number_of_coins", required=True
)
POST_ARGS.add_argument(
    "cost_per_coin", type=float, help="Must Include number_of_coins", required=True
)

"""
*argument parser for get args
*required args with examples are as follows:
{
    "symbol": "BTC"
}
"""
GET_ARGS = reqparse.RequestParser()
GET_ARGS.add_argument("symbol", type=str, help="Must Include a symbol", required=True)

"""
*argument parser for patch args
*required args with examples are as follows:
{
    "symbol": "BTC",
    "new_number_of_coins": 31.5
}
"""
PATCH_ARGS = reqparse.RequestParser()
PATCH_ARGS.add_argument("symbol", type=str, help="Must Include a symbol", required=True)
PATCH_ARGS.add_argument(
    "new_number_of_coins",
    type=float,
    help="Must include new_number_of_coins",
    required=True,
)


class Cryptos(Resource):
    @marshal_with(RESOURCE_FIELDS)
    @jwt_required()
    def get(self) -> dict:
        """returns all cryptos that a user owns

        Args:
            access_token: FRESH or STALE

        Returns:
            dict: [{CryptoModel}, {CryptoModel}...]
                or {"message": "user does not exist"}
            int: status_code == 200 or 404
        """
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        if current_user:
            cryptos = CryptoModel.query.filter_by(owner_id=current_user.id).all()
            return cryptos, 200
        else:
            abort(404, message="user does not exist")


class Crypto(Resource):
    @marshal_with(RESOURCE_FIELDS)
    @jwt_required()
    def get(self) -> dict:
        """returns info on a certain crypto owned by a user

        Args:
            GET_ARGS
            access_token: FRESH or STALE

        Returns:
            dict: {CryptoModel} or {"message": "crypto not found" or
                "user does not exist"}
            int: status_code == 200 or 404
        """
        args = GET_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        if current_user:
            crypto = user_has_crypto(current_user.id, args["symbol"])
            if crypto:
                return crypto, 200
            else:
                abort(404, message="crypto not found")
        else:
            abort(404, message="user does not exist")

    @marshal_with(RESOURCE_FIELDS)
    @jwt_required(fresh=True)
    def post(self) -> dict:
        """add new crypto to database under current user

        Args:
            POST_ARGS
            access_token: FRESH

        Returns:
            dict: {CryptoModel} or {"message": "user already owns that crypto"
                or "user does not exist"}
            int: status_code == 201 or 400 or 404
        """
        args = POST_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        if current_user:
            crypto = user_has_crypto(current_user.id, args["symbol"])
            if crypto:
                abort(
                    400,
                    message=(
                        "user already owns that crypto, try a patch request"
                        "to update number of coins or delete to remove it"
                    ),
                )
            else:
                crypto = CryptoModel(
                    symbol=args["symbol"].upper(),
                    number_of_coins=args["number_of_coins"],
                    cost_per_coin=args["cost_per_coin"],
                    owner_id=current_user.id,
                )
                add_to_database(crypto)

                return crypto, 201
        else:
            abort(404, message="user does not exist")

    @marshal_with(RESOURCE_FIELDS)
    @jwt_required(fresh=True)
    def patch(self) -> dict:
        """updates values for a given crypto that a user owns

        Args:
            PATCH_ARGS
            access_token: FRESH

        Returns:
            dict: {CryptoModel} or {"message": "user does not own that crypto"
                or "user does not exist"}
            int: status_code == 200, 404
        """
        args = PATCH_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        if current_user:
            crypto = user_has_crypto(current_user.id, args["symbol"])

            if crypto:
                crypto.update_coins(args["new_number_of_coins"])
                return crypto, 200
            else:
                abort(404, message="user does not own that crypto")
        else:
            abort(404, message="user does not exist")

    @jwt_required(fresh=True)
    def delete(self) -> dict:
        """deletes a crypto that a user owns

        Args:
            GET_ARGS
            access_token: FRESH

        Returns:
            dict: {"message": "successfully deleted" or "user does not own that
                crypto" or "user does not exist"}
            int: status_code == 200, 404
        """
        args = GET_ARGS.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        if current_user:
            crypto = user_has_crypto(current_user.id, args["symbol"])

            if crypto:
                delete_from_database(crypto)

                return {"message": f"{crypto.symbol} successfully deleted"}
            else:
                abort(404, message="user does not own that crypto")
        else:
            abort(404, message="user does not exist")


def user_has_crypto(id: int, symbol: str) -> object or bool:
    """checks if user owns a certain crypto

    Args:
        id (int): id of the user
        symbol (str): symbol of crypto being looked up

    Returns:
        object or bool: CryptoModel or False
    """
    cryptos = CryptoModel.query.filter_by(owner_id=id).all()

    for crypto in cryptos:
        if crypto.symbol == symbol.upper():
            return crypto

    return False
