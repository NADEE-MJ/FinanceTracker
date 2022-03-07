from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema

from models import StockModel


class GetStockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StockModel

    id = auto_field(load_only=True)
    ticker = auto_field(
        required=True, error_messages={"required": "You must include a 'ticker' field"}
    )


class PostStockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StockModel

    id = auto_field(load_only=True)
    ticker = auto_field(
        required=True, error_messages={"required": "You must include a 'ticker' field"}
    )
    number_of_shares = auto_field(
        required=True,
        error_messages={"required": "You must include a 'number_of_shares' field"},
    )
    cost_per_share = auto_field(
        required=True,
        error_messages={"required": "You must include a 'cost_per_share' field"},
    )


class PatchStockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StockModel

    id = auto_field(load_only=True)
    ticker = auto_field(
        required=True, error_messages={"required": "You must include a 'ticker' field"}
    )
    number_of_shares = auto_field(
        required=True,
        error_messages={"required": "You must include a 'number_of_shares' field"},
    )
