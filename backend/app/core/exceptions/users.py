from .base import AppException


class UserNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="User not found", status_code=404, error_code="user_not_found"
        )


class UserAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Email already registered",
            status_code=409,
            error_code="email_registered",
        )
