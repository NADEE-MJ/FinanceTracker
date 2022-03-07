from flask.views import MethodView
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import CryptoModel, UserModel, delete_from_database, add_to_database


class DeleteUser(MethodView):
    # delete user account
    @jwt_required(fresh=True)
    def delete(self) -> dict:
        current_user = UserModel.get_by_username(get_jwt_identity())

        if current_user:
            delete_from_database(current_user)

            return {"message": "user deleted successfully"}
        else:
            abort(404, message="user does not exist")
