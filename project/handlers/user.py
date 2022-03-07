from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from webargs.flaskparser import use_args

from models import UserModel, add_to_database, TokenBlocklist
from schema import RegisterUserSchema, LoginUserSchema


class User(Resource):
    # Login user
    @use_args(LoginUserSchema())
    def put(self, args) -> dict:
        user = UserModel.get_by_email(args["email"])

        if user:
            if check_password_hash(user.password, args["password"]):
                tokens = user.fresh_login()
                return {
                    "message": "successfully logged in",
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                }
            else:
                abort(400, message="Password is incorrect.")
        else:
            abort(404, message="Email not found")

    # Register User
    @use_args(RegisterUserSchema())
    def post(self, args) -> dict:

        new_user = UserModel(
            email=args["email"],
            username=args["username"],
            password=generate_password_hash(args["password1"], method="sha256"),
        )

        add_to_database(new_user)

        return {"message": "the user has been created"}

    # Logout User
    @jwt_required()
    def delete(self) -> dict:
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        add_to_database(TokenBlocklist(jti=jti, revoked_at=now))

        return {"message": "user logged out, access token revoked"}
