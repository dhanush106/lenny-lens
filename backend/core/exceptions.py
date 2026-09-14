import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.core.logging import log_event

logger = logging.getLogger(__name__)


class ServiceUnavailableError(Exception):
    """A dependency needed to fulfill a request is unavailable."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceUnavailableError)
    async def service_unavailable_handler(
        request: Request, exc: ServiceUnavailableError
    ):
        return JSONResponse(
            status_code=503,
            content={"detail": {"code": exc.code, "message": exc.message}},
        )
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": exc.body},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log_event(
            logger,
            "unhandled_error",
            path=str(request.url.path),
            error_type=type(exc).__name__,
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": {
                    "code": "internal_server_error",
                    "message": "Internal Server Error",
                    "error_type": type(exc).__name__,
                    "error_detail": str(exc),
                }
            },
        )
