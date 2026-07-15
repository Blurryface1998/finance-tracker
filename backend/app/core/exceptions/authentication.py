from app.core.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Email already registered",
            status_code=403,
            error_code="email_registered",
        )
