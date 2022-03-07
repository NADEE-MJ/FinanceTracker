from config import DB


class StockModel(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    ticker = DB.Column(DB.String(20))
    number_of_shares = DB.Column(DB.Float)
    cost_per_share = DB.Column(DB.Float)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey("user_model.id", ondelete="CASCADE"))
    owner = DB.relationship("UserModel", back_populates="stocks")

    def __repr__(self) -> str:
        return f"Stock(ticker = {self.ticker}, number_of_shares = {self.number_of_shares}, cost_per_share = {self.cost_per_share})"

    def update_shares(self, new_shares: float) -> None:
        """updates number of shares in the database

        Args:
            new_shares (float): new number of shares the user owns of that stock
        """
        self.number_of_shares = new_shares
        DB.session.commit()

    @classmethod
    def get_all_by_owner_id(cls, id):
        return cls.query.filter_by(owner_id=id).all()

    @classmethod
    def get_by_owner_id(cls, id):
        return cls.query.filter_by(owner_id=id).first()
