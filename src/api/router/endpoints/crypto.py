from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import crud, schema
from api.db.models import User
from api.core import dependencies as deps

router = APIRouter()


@router.get("/", response_model=List[schema.Crypto])
def read_cryptos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cryptos.
    """
    if crud.user.is_superuser(current_user):
        cryptos = crud.crypto.get_multi(db, skip=skip, limit=limit)
    else:
        cryptos = crud.crypto.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return cryptos


@router.post("/", response_model=schema.Crypto)
def create_crypto(
    *,
    db: Session = Depends(deps.get_db),
    crypto_in: schema.CryptoCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new crypto.
    """
    crypto = crud.crypto.create_with_owner(
        db=db, obj_in=crypto_in, owner_id=current_user.id
    )
    return crypto


@router.put("/{id}", response_model=schema.Crypto)
def update_crypto(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    crypto_in: schema.CryptoUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an crypto.
    """
    crypto = crud.crypto.get(db=db, id=id)
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    if not crud.user.is_superuser(current_user) and (
        crypto.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crypto = crud.crypto.update(db=db, db_obj=crypto, obj_in=crypto_in)
    return crypto


@router.get("/{id}", response_model=schema.Crypto)
def read_crypto(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get crypto by ID.
    """
    crypto = crud.crypto.get(db=db, id=id)
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    if not crud.user.is_superuser(current_user) and (
        crypto.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crypto


@router.delete("/{id}", response_model=schema.Crypto)
def delete_crypto(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an crypto.
    """
    crypto = crud.crypto.get(db=db, id=id)
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    if not crud.user.is_superuser(current_user) and (
        crypto.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crypto = crud.crypto.remove(db=db, id=id)
    return crypto
