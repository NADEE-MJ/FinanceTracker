from flask.views import MethodView
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import CryptoModel, UserModel


class Cryptos(MethodView):
    # returns all cryptos that a user owns
    @jwt_required()
    def get(self) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            cryptos = CryptoModel.get_all_by_owner_id(current_user.id)
            return cryptos, 200
        else:
            abort(404, message="user does not exist")
