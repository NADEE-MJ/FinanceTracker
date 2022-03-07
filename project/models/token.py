from config import JWT
from config import DB


class TokenBlocklist(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    jti = DB.Column(DB.String(36), nullable=False)
    revoked_at = DB.Column(DB.DateTime, nullable=False)


# the following two functions with the @JWT decorators run everytime the @jwt_required
# decorator is on a view
@JWT.expired_token_loader
def my_expired_token_callback(JWT_header, JWT_payload) -> dict:
    return {"message": "invalid token or token expired"}, 401


@JWT.token_in_blocklist_loader
def check_if_token_revoked(JWT_header, JWT_payload: dict) -> bool:
    jti = JWT_payload["jti"]
    token = DB.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None