from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from backend.db.session import async_session_maker
from backend.models import User

from backend.core.config import settings
from backend.core.exceptions import add_exception_handlers
from backend.api.router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url="/api/v1/openapi.json"
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        # Content Security Policy to prevent XSS in artifact rendering
        response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'none'; object-src 'none';"
        return response

    # Add exception handlers
    add_exception_handlers(app)

    # Include routers
    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup_event():
        async with async_session_maker() as session:
            # Check if user 1 exists
            result = await session.execute(select(User).filter_by(id=1))
            user = result.scalar_one_or_none()
            if not user:
                # Create default user
                user = User(username="admin", email="admin@example.com")
                session.add(user)
                await session.commit()

    return app

app = create_app()
