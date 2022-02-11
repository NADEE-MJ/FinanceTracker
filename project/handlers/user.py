"""
user views, for the following urls /user, /refresh, /user/delete
this module include user registration, login, logout, deletion, and access_token
refreshing, please see readme.md for info on how to use api
"""
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

from models import UserModel, TokenBlocklist, add_to_database, delete_from_database

"""
?@jwt_required() decorator means that the json file passed to the api needs to
?include a valid access_token with the format -> "access_token": str

?@jwt_required(fresh=true) decorator means that the json file passed to the api
?must include a fresh access_token with the format -> "access_token": str, this
?can only be acquired through a fresh login, not through using a refresh_token

?@jwt_required(refresh=true) decorator means that the json file passed to the api
?must include a refresh token with the format -> "refresh_token": str, this can
?only be acquired through a fresh login
"""

"""
*argument parser for login args
*required args are as follows:
{
    "email": "example@example.com",
    "password": "examplePassword"
}
"""
LOGIN_ARGS = reqparse.RequestParser()
LOGIN_ARGS.add_argument("email", type=str, help="Must Include an email", required=True)
LOGIN_ARGS.add_argument(
    "password", type=str, help="Must Include a password", required=True
)

"""
*argument parser for registering args
*required args are as follows:
{
    "email": "example@example.com",
    "username": "exampleUsername",
    "password1": "examplePassword",
    "password2": "examplePassword"
}
"""
REGISTER_ARGS = reqparse.RequestParser()
REGISTER_ARGS.add_argument(
    "email", type=str, help="Must Include an email", required=True
)
REGISTER_ARGS.add_argument(
    "username", type=str, help="Must Include a username", required=True
)
REGISTER_ARGS.add_argument(
    "password1", type=str, help="Must Include a password1", required=True
)
REGISTER_ARGS.add_argument(
    "password2", type=str, help="Must Include a password2", required=True
)


class User(Resource):
    def put(self) -> tuple(dict, int):
        """login user, if user exists, checks if password is correct, if correct
        creates fresh access_token and refresh_token and sends them to user,
        if password incorrect or the user doesn't exist then error

        Returns:
            dict: {"message": "login success" or "wrong password" or "email not found",
                "access_token": "str",
                "refresh_token": "str"}
            int: status_code == 200 or 400 or 404
        """
        args = LOGIN_ARGS.parse_args()
        user = UserModel.query.filter_by(email=args["email"]).first()

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

    def post(self) -> tuple(dict, int):
        """register user, checks if email or username are already in database,
        then checks password1 and password2 are equal, then checks username and
        password length, then checks email for validation, if all checks pass
        create a new user and add them to database

        Returns:
            dict: {"message": "user created" or "email in use" or "username in user"
            or "passwords don't match" or "username too short" or "password too short"
            or "email is invalid"}
            int: status_code == 200 or 400 or 409
        """

        args = REGISTER_ARGS.parse_args()
        email = UserModel.query.filter_by(email=args["email"]).first()
        username = UserModel.query.filter_by(username=args["username"]).first()

        if email:
            abort(409, message="Email is already in use.")
        elif username:
            abort(409, message="Username is already in use.")
        elif args["password1"] != args["password2"]:
            abort(400, message="Passwords don't match!")
        elif len(args["username"]) < 2:
            abort(400, message="Username is too short.")
        elif len(args["password1"]) < 6:
            abort(400, message="Password is too short.")
        elif len(args["email"]) < 4:
            abort(400, message="Email is invalid.")  # !do regex/email validation here
        else:
            new_user = UserModel(
                email=args["email"],
                username=args["username"],
                password=generate_password_hash(args["password1"], method="sha256"),
            )

            add_to_database(new_user)

            return {"message": "the user has been created"}

    @jwt_required()
    def delete(self) -> tuple(dict, int):
        """log out user, gets username from jwt payload, adds access token to
        token blocklist with the token id and time revoked and returns logged
        out to user

        Returns:
            dict: {"message": "user logged out"}
            int: status_code == 200
        """
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        add_to_database(TokenBlocklist(jti=jti, revoked_at=now))

        return {"message": "user logged out, access token revoked"}


class DeleteUser(Resource):
    @jwt_required(fresh=True)
    def delete(self) -> tuple(dict, int):
        """delete user account, gets username from jwt payload, if user in
        database then delete user from database and all related assets, otherwise
        return error

        Returns:
            dict: {"message": "user deleted successfully" or "user does not exist"}
            int: status_code == 200 or 404
        """
        username = get_jwt_identity()
        current_user = UserModel.query.filter_by(username=username).first()

        if current_user:
            delete_from_database(current_user)

            return {"message": "user deleted successfully"}

        abort(404, message="user does not exist")


class Refresh(Resource):
    @jwt_required(refresh=True)
    def put(self) -> tuple(dict, int):
        """refresh access_token, gets username from jwt payload, gets user from
        database and creates a stale access_token

        Returns:
            dict: {"access_token": str}
            int: status_code == 200
        """
        username = get_jwt_identity()
        current_user = UserModel.query.filter_by(username=username).first()
        token = current_user.stale_login()

        return {"access_token": token}
