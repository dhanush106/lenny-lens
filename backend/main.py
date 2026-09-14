from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from backend.db.session import async_session_maker
from backend.models import User

from backend.core.config import settings
from backend.core.exceptions import add_exception_handlers
from backend.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        result = await session.execute(select(User).filter_by(id=1))
        user = result.scalar_one_or_none()
        if not user:
            session.add(
                User(
                    id=1,
                    email="local-demo@example.invalid",
                    hashed_password="local-demo-account-not-for-authentication",
                )
            )
            await session.commit()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        # Vite can move to a different port when its preferred port is busy, and
        # users commonly open the local app through either loopback hostname.
        # Keep this deliberately limited to local HTTP development origins.
        allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:80", "http://127.0.0.1:80"],
        allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    add_exception_handlers(app)
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
