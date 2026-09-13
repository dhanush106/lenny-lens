from fastapi import APIRouter
from backend.schemas.health import HealthResponse
from backend.core.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Verify the API process is alive.
    """
    return HealthResponse(
        status="ok",
        environment=settings.ENVIRONMENT
    )
