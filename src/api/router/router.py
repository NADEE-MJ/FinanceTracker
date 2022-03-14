from fastapi import APIRouter

from .endpoints import stocks, login, users, crypto

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
api_router.include_router(stocks.router, prefix="/stock", tags=["stock"])
api_router.include_router(crypto.router, prefix="/crypto", tags=["crypto"])
