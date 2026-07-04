from app.core.exceptions.base import AppException


class UnauthorizedError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Authentication required",
            status_code=401,
            error_code="unauthorized",
        )


class ForbiddenError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="You do not have permission to access this resource",
            status_code=403,
            error_code="forbidden",
        )
