from pydantic import BaseModel


# Shared properties
class StockBase(BaseModel):
    title: str | None = None
    description: str | None = None


# Properties to receive on stock creation
class StockCreate(StockBase):
    title: str


# Properties to receive on stock update
class StockUpdate(StockBase):
    pass


# Properties shared by models stored in DB
class StockInDBBase(StockBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Stock(StockInDBBase):
    pass


# Properties properties stored in DB
class StockInDB(StockInDBBase):
    pass
