from app.core.exceptions.base import AppException


class DatabaseError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="A database error occured",
            status_code=500,
            error_code="database_error",
        )


class DuplicateEntryError(AppException):
    def __init__(self, entity: str) -> None:
        super().__init__(
            message=f"{entity} already exists",
            status_code=409,
            error_code="duplicate_entry",
        )
