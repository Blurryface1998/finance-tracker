
from app.core.exceptions.base import AppException


class TransactionNotFoundError(AppException):
    def __init__(self, transaction_id: int) -> None:
        self.transaction_id = transaction_id
        super().__init__(
            message=f"Transaction with id {transaction_id} not found",
            status_code=404,
            error_code="transaction_not_found",
        )
