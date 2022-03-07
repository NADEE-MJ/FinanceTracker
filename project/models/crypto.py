from config import DB


class CryptoModel(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    symbol = DB.Column(DB.String(20))
    number_of_coins = DB.Column(DB.Float)
    cost_per_coin = DB.Column(DB.Float)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey("user_model.id", ondelete="CASCADE"))
    owner = DB.relationship("UserModel", back_populates="cryptos")

    def __repr__(self) -> str:
        return f"Crypto(symbol = {self.symbol}, number_of_coins = {self.number_of_coins}, cost_per_coin = {self.cost_per_coin})"

    def update_coins(self, new_coins: float) -> None:
        """updates number of coins the database

        Args:
            new_coins (float): new number of coins the user owns of that crypto
        """
        self.number_of_coins = new_coins
        DB.session.commit()

    @classmethod
    def get_all_by_owner_id(cls, id):
        return cls.query.filter_by(owner_id=id).all()

    @classmethod
    def get_by_owner_id(cls, id):
        return cls.query.filter_by(owner_id=id).first()
