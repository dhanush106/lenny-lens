from fastapi import APIRouter
from backend.api import health, sessions

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
