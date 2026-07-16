from .base import AppException


class InvalidCredentialsError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid credentials",
            status_code=401,
            error_code="invalid_credentials",
        )
