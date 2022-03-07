from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args

from schema import GetCryptoSchema, PostCryptoSchema, PatchCryptoSchema
from models import CryptoModel, UserModel, delete_from_database, add_to_database


SCHEMA = GetCryptoSchema()


class Crypto(Resource):
    #returns info on a certain crypto owned by a user
    @use_args(GetCryptoSchema())
    @jwt_required()
    def get(self, args) -> dict:

        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            crypto = current_user.owns_crypto(args["symbol"])
            if crypto:
                return SCHEMA.dump(crypto), 200
            else:
                abort(404, message="crypto not found")
        else:
            abort(404, message="user does not exist")

    # adds new crypto to database under current user
    @use_args(PostCryptoSchema())
    @jwt_required(fresh=True)
    def post(self, args) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            crypto = current_user.owns_crypto(args["symbol"])
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

                return SCHEMA.dump(crypto), 201
        else:
            abort(404, message="user does not exist")

    # updates values for a given crypto that a user owns
    @use_args(PatchCryptoSchema())
    @jwt_required(fresh=True)
    def patch(self, args) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            crypto = current_user.owns_crypto(args["symbol"])

            if crypto:
                crypto.update_coins(args["new_number_of_coins"])
                return SCHEMA.dump(crypto), 200
            else:
                abort(404, message="user does not own that crypto")
        else:
            abort(404, message="user does not exist")

    # deletes a crypto that a user owns
    @use_args(GetCryptoSchema())
    @jwt_required(fresh=True)
    def delete(self, args) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            crypto = current_user.owns_crypto(args["symbol"])

            if crypto:
                delete_from_database(crypto)

                return {"message": f"{crypto.symbol} successfully deleted"}
            else:
                abort(404, message="user does not own that crypto")
        else:
            abort(404, message="user does not exist")
