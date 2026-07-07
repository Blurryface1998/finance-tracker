"""Exception handlers for returning consistent API error responses."""

from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions.base import AppException
from app.core.logging import logger


async def app_exception_handler(request: Request, exc: AppException):
    """Convert application exceptions into structured JSON API error responses."""
    logger.warning(
        "Handled application exception: %s",
        exc.message,
        extra={"path": str(request.url.path), "method": request.method},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "status_code": exc.status_code,
                "path": str(request.url.path),
                "method": request.method,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        },
    )
