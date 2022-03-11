from fastapi import FastAPI

from api.router import api_router
from api.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_VERSION_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_VERSION_STR)
