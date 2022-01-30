from flask_restful import Resource, marshal_with
from app import crypto_resource_fields
from models import CryptoModel

class Cryptos(Resource):
    @marshal_with(crypto_resource_fields)
    def get(self):
        cryptos = CryptoModel.query.all()

        return cryptos