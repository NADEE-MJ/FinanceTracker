from flask.views import MethodView
from flask import abort, Response
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from webargs.flaskparser import use_args
from werkzeug.exceptions import HTTPException

from models import UserModel, add_to_database, TokenBlocklist
from schema import RegisterUserSchema, LoginUserSchema


class User(MethodView):
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
                raise HTTPException(
                    response=Response("Password is incorrect.", status=400)
                )
        else:
            raise HTTPException()

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
