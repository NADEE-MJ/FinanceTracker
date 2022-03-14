from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from api.db.base_class import Base


class Crypto(Base):
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    number_of_coins = Column(Float)
    cost_per_coin = Column(Float)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="cryptos")
