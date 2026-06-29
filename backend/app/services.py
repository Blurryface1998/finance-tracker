from app.schemas import TransactionCreate, TransactionUpdate, CategorySummary
from app.models import Transaction
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from datetime import datetime, date

def create_transaction_service(db: Session, data: TransactionCreate):
    """Create and save a new transaction.

    Expenses are stored as negative values and incomes as positive values.

    Args:
        db: SQLAlchemy session instance.
        data: Validated transaction payload.

    Returns:
        The saved Transaction instance.
    """
    if data.type == "expense":
        amount = -data.amount
    else:
        amount = data.amount

    transaction = Transaction(
        description=data.description,
        amount=amount,
        category=data.category,
        type=data.type
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

def get_transactions_service(
        db: Session,
        type: str | None = None,
        category: str | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None
        ):
    """Retrieve transactions using optional filter criteria.

    Args:
        db: SQLAlchemy session instance.
        type: Filter by transaction type: 'income' or 'expense'.
        category: Partial case-insensitive category match.
        min_amount: Minimum amount filter.
        max_amount: Maximum amount filter.

    Returns:
        A list of Transaction instances.
    """
    query = db.query(Transaction)

    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category.ilike(f"%{category}%"))
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    
    return query.all()


def get_transaction_service(db: Session, transaction_id: int):
    """Retrieve a single transaction by ID.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.

    Returns:
        The Transaction instance, or None if not found.
    """
    return db.get(Transaction, transaction_id)

def update_transaction_service(
        db: Session, 
        transaction_id: int, 
        data: TransactionUpdate
):
    """Update an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.
        data: Validated transaction update payload.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    transaction = db.get(Transaction, transaction_id)

    if not transaction:
        return None
    
    amount = -data.amount if data.type == "expenses" else data.amount

    transaction.description = data.description
    transaction.amount = amount
    transaction.category = data.category
    transaction.type = data.type

    db.commit()
    db.refresh(transaction)

    return transaction

def delete_transaction_service(db:Session, transaction_id: int):
    """Delete a transaction by ID.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.

    Returns:
        The deleted Transaction instance, or None if not found.
    """
    transaction = db.get(Transaction, transaction_id)

    if not transaction:
        return None
    
    db.delete(transaction)
    db.commit()
    
    return transaction

def get_month_range(month: str):
    """Convert a month string into a date range.

    Args:
        month: Month string in format 'YYYY-m'.

    Returns:
        A tuple of (start_date, end_date) for the month.
    """
    start = datetime.strptime(month, "%Y-m%").date()

    if start.month == 12:
        end = date(start.year + 1, 1, 1)
    else:
        end = date(start.year, start.month + 1, 1)

    return start, end

def get_monthly_summary_service(db: Session, month: str):
    """Generate a monthly income and expense summary.

    Args:
        db: SQLAlchemy session instance.
        month: Month string in format 'YYYY-m'.

    Returns:
        A dictionary with month, income, expense, and balance.
    """
    start_date, end_date = get_month_range(month)
    income = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.type == "income",
        Transaction.created_at >= start_date,
        Transaction.created_at < end_date
    ).scalar()

    expense = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.type == "expense",
        Transaction.created_at >= start_date,
        Transaction.created_at < end_date
    ).scalar()

    expense = abs(expense)

    return {
        "month": month,
        "income": income,
        "expense": expense,
        "balance": income - expense
    }

def get_category_summary_service(db: Session):
    """Return transaction totals grouped by category.

    Args:
        db: SQLAlchemy session instance.

    Returns:
        A list of CategorySummary objects for each category.
    """
    query = db.query(Transaction.category, func.sum(Transaction.amount)).group_by(Transaction.category)
    
    # List comprehensions
    result = []

    for category, total in query:
        result.append(CategorySummary(category=category, total=total))

    return result