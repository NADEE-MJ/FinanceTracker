from pydantic import BaseModel


# Shared properties
class CryptoBase(BaseModel):
    symbol: str | None = None


# Properties to receive on stock creation
class CryptoCreate(CryptoBase):
    symbol: str
    number_of_coins: int
    cost_per_coin: int


# Properties to receive on stock update
class CryptoUpdate(CryptoBase):
    number_of_coins: int


# Properties shared by models stored in DB
class CryptoInDBBase(CryptoBase):
    id: int
    symbol: str
    number_of_coins: int
    cost_per_coin: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Crypto(CryptoInDBBase):
    pass


# Properties properties stored in DB
class CryptoInDB(CryptoInDBBase):
    pass
