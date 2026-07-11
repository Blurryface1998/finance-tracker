from datetime import datetime
from decimal import Decimal
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.core import TransactionType

ResponseItem = TypeVar("ResponseItem")


def normalize_text(value: str) -> str:
    """Normalize text values for description and category."""
    value = value.strip()

    if len(value) < 1 or len(value) > 50:
        raise ValueError("Must be between 1 and 50")
    return value.title()


def validate_amount(value: Decimal) -> Decimal:
    """Validate that the amount is greater than 0."""
    if value <= 0:
        raise ValueError("Amount must be more than 0")
    return value


class TransactionBase(BaseModel):
    """Base schema for transaction data shared across request and response models."""

    description: str
    amount: Decimal
    category: str

    @field_validator("description", "category", mode="before")
    @classmethod
    def normalize_text_validator(cls, value: str) -> str:
        return normalize_text(value)

    @field_validator("amount")
    @classmethod
    def validate_amount_validator(cls, value: Decimal) -> Decimal:
        return validate_amount(value)


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""

    transaction_type: TransactionType


class TransactionResponse(TransactionBase):
    """Schema returned by the API for transaction records."""

    id: int
    transaction_type: TransactionType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionUpdate(TransactionBase):
    """Schema used to update an existing transaction."""

    transaction_type: TransactionType


class TransactionPatch(BaseModel):
    """Schema for partial transaction updates."""

    description: str | None = None
    amount: Decimal | None = None
    category: str | None = None
    transaction_type: TransactionType | None = None

    @field_validator("description", "category", mode="before")
    @classmethod
    def normalize_text_validator(cls, value: str) -> str:
        return normalize_text(value)

    @field_validator("amount")
    @classmethod
    def validate_amount_validator(cls, value: Decimal) -> Decimal:
        return validate_amount(value)


class TransactionFilter(BaseModel):
    """Schema for filters for transactions."""

    transaction_type: TransactionType | None = NotImplemented
    category: str | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None

    @model_validator(mode="after")
    def validate_amount_range(self):
        if (
            self.min_amount is not None
            and self.max_amount is not None
            and self.min_amount > self.max_amount
        ):
            raise ValueError("min_amount cannot exceed max_amount")
        return self


class PaginationCursor(BaseModel):
    "Cursor payload used for cursor-based pagination."

    created_at: datetime
    cursor_id: int

    @model_validator(mode="after")
    def validate_cursor(self):
        """Ensure the cursor contains the required pagination values."""
        if self.created_at is None or self.cursor_id is None:
            raise ValueError("Invalid pagination cursor: cursor must not be empty")
        return self


class PaginationResult(BaseModel, Generic[ResponseItem]):
    """Container for paginated query results before the are serialized."""

    items: list[ResponseItem]
    next_cursor: PaginationCursor | None
    has_next: bool


class PaginatedResponse(BaseModel, Generic[ResponseItem]):
    """Generic paginated response payload for list endpoints."""

    items: list[ResponseItem]
    next_cursor: str | None
    has_next: bool

    model_config = ConfigDict(from_attributes=True)
