from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import UserModel


class Refresh(Resource):
    # refresh access_token, creates a stale access_token
    @jwt_required(refresh=True)
    def put(self) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())
        if current_user:
            token = current_user.stale_login()

            return token
        else:
            abort(404, message="user does not exist")
