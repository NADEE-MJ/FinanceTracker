from pydantic import BaseModel


# Shared properties
class StockBase(BaseModel):
    ticker: str | None = None
    company_name: str | None = None


# Properties to receive on stock creation
class StockCreate(StockBase):
    ticker: str
    company_name: str
    number_of_shares: int
    cost_per_share: int


# Properties to receive on stock update
class StockUpdate(StockBase):
    number_of_shares: int


# Properties shared by models stored in DB
class StockInDBBase(StockBase):
    id: int
    ticker: str
    company_name: str
    number_of_shares: int
    cost_per_share: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Stock(StockInDBBase):
    pass


# Properties properties stored in DB
class StockInDB(StockInDBBase):
    pass
