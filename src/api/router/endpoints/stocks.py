from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import crud, schema
from api.db.models import User
from api.core import dependencies as deps

router = APIRouter()


@router.get("/", response_model=List[schema.Stock])
def read_stocks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve stocks.
    """
    if crud.user.is_superuser(current_user):
        stocks = crud.stock.get_multi(db, skip=skip, limit=limit)
    else:
        stocks = crud.stock.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return stocks


@router.post("/", response_model=schema.Stock)
def create_stock(
    *,
    db: Session = Depends(deps.get_db),
    stock_in: schema.StockCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new stock.
    """
    stock = crud.stock.create_with_owner(db=db, obj_in=stock_in, owner_id=current_user.id)
    return stock


@router.put("/{id}", response_model=schema.Stock)
def update_stock(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    stock_in: schema.StockUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an stock.
    """
    stock = crud.stock.get(db=db, id=id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    if not crud.user.is_superuser(current_user) and (stock.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    stock = crud.stock.update(db=db, db_obj=stock, obj_in=stock_in)
    return stock


@router.get("/{id}", response_model=schema.Stock)
def read_stock(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get stock by ID.
    """
    stock = crud.stock.get(db=db, id=id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    if not crud.user.is_superuser(current_user) and (stock.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return stock


@router.delete("/{id}", response_model=schema.Stock)
def delete_stock(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an stock.
    """
    stock = crud.stock.get(db=db, id=id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    if not crud.user.is_superuser(current_user) and (stock.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    stock = crud.stock.remove(db=db, id=id)
    return stock
