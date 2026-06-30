from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas import (PaginatedResponse, TransactionCreate,
                         TransactionPatch, TransactionResponse,
                         TransactionType, TransactionUpdate)


# Helper function
def _get_transaction(db: Session, transaction_id: int) -> Transaction | None:
    """Return a transaction by ID, or None if it does not exist."""
    return db.get(Transaction, transaction_id)


def create_transaction(db: Session, data: TransactionCreate) -> Transaction:
    """Create and save a new transaction.

    Args:
        db: SQLAlchemy session instance.
        data: Validated transaction payload.

    Returns:
        The saved Transaction instance.
    """
    transaction = Transaction(
        description=data.description,
        amount=data.amount,
        category=data.category,
        transaction_type=data.transaction_type,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(
    db: Session,
    transaction_type: TransactionType | None = None,
    category: str | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    limit: int = 20,
    cursor: int | None = None,
) -> PaginatedResponse[TransactionResponse]:
    """Retrieve transactions with optional filters and cursor-based pagination.

    Args:
        db: SQLAlchemy session instance.
        transaction_type: Optional filter by transaction type: 'income' or 'expense'.
        category: Optional partial, case-insensitive category match.
        min_amount: Optional minimum amount filter.
        max_amount: Optional maximum amount filter.
        limit: Maximum number of transactions to return per page.
        cursor: The last transaction ID from the previous page; only records with a
            larger ID are returned.

    Returns:
        A paginated response containing the transactions and pagination metadata.
    """
    if limit < 1:
        raise ValueError("limit must be grater than 0")

    base_query = db.query(Transaction).order_by(Transaction.id.desc())

    if transaction_type:
        base_query = base_query.filter(Transaction.transaction_type == transaction_type)

    if category:
        base_query = base_query.filter(Transaction.category.ilike(f"%{category}%"))

    if min_amount is not None:
        base_query = base_query.filter(Transaction.amount >= min_amount)

    if max_amount is not None:
        base_query = base_query.filter(Transaction.amount <= max_amount)

    if cursor is not None:
        base_query = base_query.filter(Transaction.id > cursor)

    items = base_query.limit(limit + 1).all()
    has_next = len(items) > limit

    if has_next:
        items = items[:-1]

    next_cursor = items[-1].id if items else None

    return PaginatedResponse(
        items=items,
        next_cursor=next_cursor,
        has_next=has_next,
    )


def get_transaction(db: Session, transaction_id: int) -> Transaction | None:
    """Retrieve a single transaction by ID.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.

    Returns:
        The Transaction instance, or None if not found.
    """
    return db.get(Transaction, transaction_id)


def update_transaction(
    db: Session, transaction_id: int, data: TransactionUpdate
) -> Transaction | None:
    """Update an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.
        data: Validated transaction update payload.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    transaction = _get_transaction(db, transaction_id)

    if not transaction:
        return None

    transaction.description = data.description
    transaction.amount = data.amount
    transaction.category = data.category
    transaction.transaction_type = data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(db: Session, transaction_id: int) -> Transaction | None:
    """Delete a transaction by ID.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.

    Returns:
        The deleted Transaction instance, or None if not found.
    """
    transaction = _get_transaction(db, transaction_id)

    if not transaction:
        return None

    db.delete(transaction)
    db.commit()

    return transaction


def patch_transaction(
    db: Session, transaction_id: int, data: TransactionPatch
) -> Transaction | None:
    """Apply partial updates to an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction to modify.
        data: Partial transaction payload containing only the fields to update.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    transaction = _get_transaction(db, transaction_id)

    if not transaction:
        return None

    if data.description is not None:
        transaction.description = data.description.strip().title()
    if data.amount is not None:
        transaction.amount = data.amount
    if data.category is not None:
        transaction.category = data.category.strip().title()
    if data.transaction_type is not None:
        transaction.transaction_type = data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction
