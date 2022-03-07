from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema

from models import CryptoModel


class GetCryptoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CryptoModel

    id = auto_field(load_only=True)
    symbol = auto_field(
        required=True, error_messages={"required": "You must include a 'symbol' field"}
    )


class PostCryptoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CryptoModel

    id = auto_field(load_only=True)
    symbol = auto_field(
        required=True, error_messages={"required": "You must include a 'symbol' field"}
    )
    number_of_coins = auto_field(
        required=True,
        error_messages={"required": "You must include a 'number_of_coins' field"},
    )
    cost_per_coin = auto_field(
        required=True,
        error_messages={"required": "You must include a 'cost_per_coin' field"},
    )


class PatchCryptoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CryptoModel

    id = auto_field(load_only=True)
    symbol = auto_field(
        required=True, error_messages={"required": "You must include a 'symbol' field"}
    )
    number_of_coins = auto_field(
        required=True,
        error_messages={"required": "You must include a 'number_of_coins' field"},
    )
