from datetime import date, datetime, MINYEAR, MAXYEAR
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas import CategorySummary, MonthlySummary, TransactionType, YearlySummary


def get_total_of_type(
    db: Session,
    transaction_type: TransactionType,
    start_date: date,
    end_date: date,
) -> Decimal:
    """Return the total amount for a transaction type within a date range."""
    return (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.transaction_type == transaction_type,
            Transaction.created_at >= start_date,
            Transaction.created_at < end_date,
        )
        .scalar()
    )


def get_month_range(month: str) -> tuple:
    """Convert a month string into a date range.

    Args:
        month: Month string in format 'YYYY-m'.

    Returns:
        A tuple of (start_date, end_date) for the month.
    """
    start = datetime.strptime(month, "%Y-%m").date()

    if start.month == 12:
        end = date(start.year + 1, 1, 1)
    else:
        end = date(start.year, start.month + 1, 1)

    return start, end


def get_monthly_summary(db: Session, month: str) -> MonthlySummary:
    """Generate a monthly income and expense summary.

    Args:
        db: SQLAlchemy session instance.
        month: Month string in format 'YYYY-m'.

    Returns:
        A dictionary with month, income, expense, and balance.
    """
    start_date, end_date = get_month_range(month)
    income = get_total_of_type(db, TransactionType.income, start_date, end_date)

    expense = get_total_of_type(db, TransactionType.expense, start_date, end_date)

    return MonthlySummary(
        month=start_date.month, income=income, expense=expense, balance=income - expense
    )


def get_yearly_summary(db: Session, year: str) -> YearlySummary:
    order_year = int(year)

    if order_year <= 2000 or order_year >= 2100:
        raise ValueError("Year must be between 2000 and 2100 ")

    months = []

    for month in range(1, 13):
        month_string = f"{year}-{month:02d}"
        summary = get_monthly_summary(db=db, month=month_string)
        months.append(summary)

    return YearlySummary(year=order_year, months=months)


def get_category_summary(db: Session) -> list[CategorySummary]:
    """Return total transaction amounts grouped by category.

    Args:
        db: SQLAlchemy session instance.

    Returns:
        A list of CategorySummary objects for each category.
    """
    rows = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .group_by(Transaction.category)
        .all()
    )

    # List comprehensions
    return [CategorySummary(category=category, total=total) for category, total in rows]
