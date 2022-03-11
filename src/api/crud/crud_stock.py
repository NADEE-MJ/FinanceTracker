from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.crud.base import CRUDBase
from api.db.models import Stock
from api.schema.stock import StockCreate, StockUpdate


class CRUDStock(CRUDBase[Stock, StockCreate, StockUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: StockCreate, owner_id: int
    ) -> Stock:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Stock]:
        return (
            db.query(self.model)
            .filter(Stock.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


stock = CRUDStock(Stock)
