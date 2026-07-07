"""Exceptions raised when transaction resources are missing or invalid."""

from app.core.exceptions.base import AppException


class TransactionNotFoundError(AppException):
    """Raised when a transaction cannot be found by its identifier."""

    def __init__(self, transaction_id: int) -> None:
        """Store the requested transaction identifier for debugging and responses."""
        self.transaction_id = transaction_id
        super().__init__(
            message=f"Transaction with id {transaction_id} not found",
            status_code=404,
            error_code="transaction_not_found",
        )
