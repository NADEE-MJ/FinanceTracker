from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime, timezone
from models import UserModel, TokenBlocklist
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, jwt

login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, help='Must Include an email', required=True)
login_args.add_argument('password', type=str, help='Must Include a password', required=True)

register_args = reqparse.RequestParser()
register_args.add_argument('email', type=str, help='Must Include an email', required=True)
register_args.add_argument('username', type=str, help='Must Include a username', required=True)
register_args.add_argument('password1', type=str, help='Must Include a password1', required=True)
register_args.add_argument('password2', type=str, help='Must Include a password2', required=True)


class User(Resource):
    #login method
    def put(self):
        args = login_args.parse_args()

        user = UserModel.query.filter_by(email=args['email']).first()
        if user:
            if check_password_hash(user.password, args['password']):
                tokens = user.fresh_login()
                return {'message': 'succesfully logged in',
                        'access_token': tokens['access_token'],
                        'refresh_token': tokens['refresh_token']}
            else:
                abort(400, message='Password is incorrect.')
        else:
            abort(404, message='Email not found')

    #register method
    def post(self):
        args = register_args.parse_args()

        email_exists = UserModel.query.filter_by(email=args['email']).first()
        username_exists = UserModel.query.filter_by(username=args['username']).first()

        if email_exists:
            abort(409, message='Email is already in use.')
        elif username_exists:
            abort(409, message='Username is already in use.')
        elif args['password1'] != args['password2']:
            abort(400, message='Password don\'t match!')
        elif len(args['username']) < 2:
            abort(400, message='Username is too short.')
        elif len(args['password1']) < 6:
            abort(400, message='Password is too short.')
        elif len(args['email']) < 4:
            abort(400, message='Email is invalid.') #CAN DO REGEX VALIDATION HERE IN THE FUTURE
        else:
            new_user = UserModel(email=args['email'], username=args['username'], password=generate_password_hash(args['password1'], method='sha256'))

            db.session.add(new_user)
            db.session.commit()
            
            return {'message': 'the user hase been created'}

    #logoff
    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, revoked_at=now))
        db.session.commit()
        return {'message': 'user logged out, access token revoked'}

class Refresh(Resource):
    #refresh access_token
    @jwt_required(refresh=True)
    def put(self):
        username = get_jwt_identity()
        current_user = UserModel.query.filter_by(username=username).first()
        token = current_user.stale_login()

        return {'access_token': token}

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return {'code': 'dave', 'error': 'I can\'t let you do that'}, 401

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


