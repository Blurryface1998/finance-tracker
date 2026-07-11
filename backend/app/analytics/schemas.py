from decimal import Decimal

from pydantic import BaseModel


class MonthlySummary(BaseModel):
    """Schema for monthly income, expense and balance summary data."""

    month: int
    income: Decimal
    expense: Decimal
    balance: Decimal


class YearlySummary(BaseModel):
    """Schema from a yearly summary containing monthly totals."""

    year: int
    months: list[MonthlySummary]


class CategorySummary(BaseModel):
    """Schema for reporting category totals."""

    category: str
    total: Decimal
