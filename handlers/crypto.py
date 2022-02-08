from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import CryptoModel, UserModel, delete_from_database, add_to_database

crypto_resource_fields = {
    "id": fields.Integer,
    "symbol": fields.String,
    "number_of_coins": fields.Float,
    "cost_per_coin": fields.Float,
}

crypto_post_args = reqparse.RequestParser()
crypto_post_args.add_argument(
    "symbol", type=str, help="Must Include a symbol", required=True
)
crypto_post_args.add_argument(
    "number_of_coins", type=float, help="Must Include number_of_coins", required=True
)
crypto_post_args.add_argument(
    "cost_per_coin", type=float, help="Must Include number_of_coins", required=True
)

crypto_get_args = reqparse.RequestParser()
crypto_get_args.add_argument(
    "symbol", type=str, help="Must Include a symbol", required=True
)

crypto_patch_args = reqparse.RequestParser()
crypto_patch_args.add_argument(
    "symbol", type=str, help="Must Include a symbol", required=True
)
crypto_patch_args.add_argument(
    "new_number_of_coins",
    type=float,
    help="must include new_number_of_coins",
    required=True,
)


class Cryptos(Resource):
    @marshal_with(crypto_resource_fields)
    @jwt_required()
    def get(self):
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        cryptos = CryptoModel.query.filter_by(owner=current_user.id).all()
        return cryptos, 201


class Crypto(Resource):
    @marshal_with(crypto_resource_fields)
    @jwt_required()
    def get(self):
        args = crypto_get_args.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        crypto = user_has_crypto(current_user.id, args["symbol"])
        if crypto:
            return crypto, 200

        abort(404, message="crypto not found")

    @marshal_with(crypto_resource_fields)
    @jwt_required(fresh=True)
    def post(self):
        args = crypto_post_args.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        crypto = user_has_crypto(current_user.id, args["symbol"])
        if crypto:
            abort(
                400,
                message="user already owns that crypto, try a patch request to update number of coins or delete to remove it",
            )

        crypto = CryptoModel(
            symbol=args["symbol"].upper(),
            number_of_coins=args["number_of_coins"],
            cost_per_coin=args["cost_per_coin"],
            owner=current_user.id,
        )

        add_to_database(crypto)

        return crypto, 201

    @marshal_with(crypto_resource_fields)
    @jwt_required(fresh=True)
    def patch(self):
        args = crypto_patch_args.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        crypto = user_has_crypto(current_user.id, args["symbol"])
        if crypto:
            crypto.update_coins(args["new_number_of_coins"])
            return crypto, 200

        abort(404, message="user does not own that crypto")

    @jwt_required(fresh=True)
    def delete(self):
        args = crypto_get_args.parse_args()
        current_user = UserModel.query.filter_by(username=get_jwt_identity()).first()
        crypto = user_has_crypto(current_user.id, args["symbol"])
        if crypto:
            delete_from_database(crypto)

            return {"message": f"{crypto.symbol} successfully deleted"}

        abort(404, message="user does not own that crypto")


def user_has_crypto(id, symbol):
    cryptos = CryptoModel.query.filter_by(owner=id).all()
    for crypto in cryptos:
        if crypto.symbol == symbol.upper():
            return crypto
    return False
