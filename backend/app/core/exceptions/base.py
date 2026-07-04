class AppException(Exception):
    """Base exception for all aplication-level errors."""

    def __init__(
        self, message: str, status_code: int = 500, error_code: str = "app_error"
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)
