from decimal import Decimal
from typing import TypeVar

from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, or_

from app.models import Transaction
from app.utils.cursor import encode_cursor
from app.services.pagination import paginate
from app.schemas import (
    PaginatedResponse,
    TransactionCreate,
    TransactionPatch,
    TransactionResponse,
    TransactionType,
    TransactionUpdate,
    PaginationCursor,
    TransactionFilter,
    OrderSpec,
    OrderField,
)


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


"""
def apply_transaction_cursor(query, cursor):
    return query.filter(
        or_(
            Transaction.created_at < cursor.created_at,
            and_(
                Transaction.created_at == cursor.created_at,
                Transaction.id < cursor.id,
            ),
        )
    )


def build_transaction_cursor(item):
    return PaginationCursor(
        created_at=item.created_at,
        id=item.id,
    )
"""


def get_transactions(
    db: Session,
    limit: int = 20,
    cursor: PaginationCursor | None = None,
    filters: TransactionFilter | None = None,
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

    query = db.query(Transaction).order_by(
        Transaction.created_at.desc(), Transaction.id.desc()
    )

    filters = filters or TransactionFilter()

    if filters.transaction_type:
        query = query.filter(Transaction.transaction_type == filters.transaction_type)

    if filters.category:
        query = query.filter(Transaction.category.ilike(f"%{filters.category}%"))

    if filters.min_amount is not None:
        query = query.filter(Transaction.amount >= filters.min_amount)

    if filters.max_amount is not None:
        query = query.filter(Transaction.amount <= filters.max_amount)

    if cursor:
        query = query.filter(
            (Transaction.created_at, Transaction.id) < (cursor.created_at, cursor.id)
        )
    rows = query.limit(limit + 1).all()

    has_next = len(rows) > limit
    items = rows[:limit]

    last = items[-1] if items else None

    next_cursor = (
        PaginationCursor(created_at=last.created_at, id=last.id)
        if has_next and last
        else None
    )

    return PaginatedResponse(
        items=items,
        next_cursor=encode_cursor(next_cursor) if next_cursor else None,
        has_next=has_next,
    )

    """
    order_spec = OrderSpec(
        fields=[
            OrderField(name="created_at", direction="desc"),
            OrderField(name="id", direction="desc"),
        ]
    )

    result = paginate(
        query=query,
        limit=limit,
        cursor=cursor,
        order_spec=order_spec,
        apply_cursor_filter=apply_transaction_cursor,
        build_cursor=build_transaction_cursor,
    )

    items = [
        TransactionResponse.model_validate(transaction_entity)
        for transaction_entity in result.items
    ]

    next_cursor = encode_cursor(result.next_cursor) if result.next_cursor else None

    return PaginatedResponse(
        items=items,
        next_cursor=next_cursor,
        has_next=result.has_next,
    )"""


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
