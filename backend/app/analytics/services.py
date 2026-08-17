"""Analytics service function for transaction summaries and category totals."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.analytics import CategorySummary, MonthlySummary, YearlySummary
from app.core import TransactionType
from app.core.exceptions import InvalidMonthError, InvalidYearError
from app.models import Transaction, User


def get_transaction_total(
    db: Session,
    transaction_type: TransactionType,
    start_date: date,
    end_date: date,
    current_user: User,
) -> Decimal:
    """Return the total amount for one transaction type within a date range."""
    return (
        db.query(func.coalesce(func.sum(Transaction.amount), Decimal("0.00")))
        .filter(
            Transaction.transaction_type == transaction_type,
            Transaction.created_at >= start_date,
            Transaction.created_at < end_date,
            Transaction.user_id == current_user.id,
        )
        .scalar()
    )


def get_month_range(month: str) -> tuple[date, date]:
    """Convert a month string into a start/end date range.
    Args:
        month: Month string in format 'YYYY-MM'

    Returns:
        A tuple containing the first and alst day of the requested month.
    """
    try:
        start = datetime.strptime(month, "%Y-%m").date()
    except ValueError as exc:
        raise InvalidMonthError(month=month) from exc

    if start.month == 12:
        end = date(start.year + 1, 1, 1)
    else:
        end = date(start.year, start.month + 1, 1)
    return start, end


def get_monthly_summary(db: Session, month: str, current_user: User) -> MonthlySummary:
    """Generate a monthly income and expense summary.

    Args:
        db: SQLAlchemy session instance.
        month: Month string in format 'YYYY-mm'.

    Returns:
        A MonthlySummary containing income, expense, and balance values.
    """
    start_date, end_date = get_month_range(month)

    income = get_transaction_total(
        db=db,
        transaction_type=TransactionType.income,
        start_date=start_date,
        end_date=end_date,
        current_user=current_user,
    )
    expense = get_transaction_total(
        db=db,
        transaction_type=TransactionType.expense,
        start_date=start_date,
        end_date=end_date,
        current_user=current_user,
    )

    return MonthlySummary(
        month=start_date.month, income=income, expense=expense, balance=income - expense
    )


def get_yearly_summary(db: Session, year: str, current_user: User) -> YearlySummary:
    """Generate a yearly summary of monthly income and expenses.

    Args:
        db: SQLAlchemy session instance.
        year: Year string in format 'YYYY'.

    Returns:
        A YearlySummary with all 12 monthly summaries.
    """
    order_year = int(year)

    if order_year <= 2000 or order_year >= 2100:
        raise InvalidYearError(year=year)
    months = []
    for month in range(1, 13):
        month_string = f"{year}-{month:02d}"
        summary = get_monthly_summary(
            db=db, month=month_string, current_user=current_user
        )
        months.append(summary)
    return YearlySummary(year=order_year, months=months)


def get_category_summary(db: Session, current_user: User) -> list[CategorySummary]:
    """Return total transaction amounts grouped by category.

    Args:
        db: SQLAlchemy session instance.

    Returns:
        A list of CategorySummary objects for each category.
    """
    rows = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .filter(Transaction.user_id == current_user.id)
        .group_by(Transaction.category)
        .all()
    )

    # Normalize categories: strip whitespace and title-case
    normalized_summary = {}
    for category, total in rows:
        normalized_category = category.strip().title() if category else category
        if normalized_category in normalized_summary:
            normalized_summary[normalized_category] += total
        else:
            normalized_summary[normalized_category] = total

    return [
        CategorySummary(category=cat, total=total)
        for cat, total in normalized_summary.items()
    ]
