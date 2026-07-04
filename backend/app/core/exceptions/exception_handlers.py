from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions.base import AppException


async def app_exception_handler(request: Request, exc: AppException):
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
