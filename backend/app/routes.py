"""API route definitions for transaction endpoints and summaries."""

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    CategorySummary,
    MonthlySummary,
    PaginatedResponse,
    TransactionCreate,
    TransactionFilter,
    TransactionPatch,
    TransactionResponse,
    TransactionType,
    TransactionUpdate,
    YearlySummary,
)
from app.services.analytics_services import (
    get_category_summary,
    get_monthly_summary,
    get_yearly_summary,
)
from app.services.transaction_services import (
    create_transaction,
    delete_transaction,
    get_transaction,
    get_transactions,
    patch_transaction,
    update_transaction,
)

from app.utils.cursor import decode_cursor

router = APIRouter(prefix="/transactions")


@router.get("", response_model=PaginatedResponse[TransactionResponse])
async def get_transactions_route(
    transaction_type: TransactionType | None = None,
    category: str | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    limit: int = Query(20, ge=1, le=50),
    cursor: str | None = None,
    db: Session = Depends(get_db),
):
    """Return paginated transactions with optional filters and cursor-based paging."""
    cursors_obj = decode_cursor(cursor) if cursor else None

    filters = TransactionFilter(
        transaction_type=transaction_type,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
    )

    return get_transactions(db=db, limit=limit, cursor=cursors_obj, filters=filters)


@router.get("/summary", response_model=MonthlySummary)
async def get_monthly_summary_route(
    month: Annotated[str, Query(pattern=r"\d{4}-\d{2}")], db: Session = Depends(get_db)
) -> MonthlySummary:
    """Return a monthly summary for income and expenses."""
    return get_monthly_summary(db=db, month=month)


@router.get("/summary/yearly", response_model=YearlySummary)
async def get_yearly_summary_route(
    year: Annotated[str, Query(pattern=r"\d{4}")], db: Session = Depends(get_db)
) -> YearlySummary:
    """Return a yearly summary grouped by month."""
    return get_yearly_summary(db=db, year=year)


@router.get("/summary/category", response_model=list[CategorySummary])
def get_category_summary_route(db: Session = Depends(get_db)):
    """Return a summary of totals grouped by category."""
    return get_category_summary(db)


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
async def get_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    """Return a single transaction by ID."""
    transaction = get_transaction(db=db, transaction_id=transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction_route(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    """Create a new transaction."""
    return create_transaction(db, transaction)


@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
async def update_transaction_route(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing transaction by ID."""
    updated_transaction = update_transaction(
        db=db, transaction_id=transaction_id, data=transaction
    )

    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return updated_transaction


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
async def patch_transaction_route(
    transaction_id: int, transaction: TransactionPatch, db: Session = Depends(get_db)
):
    """Apply a partial update to a transaction."""
    updated = patch_transaction(db=db, transaction_id=transaction_id, data=transaction)

    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return updated


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    """Delete an existing transaction by ID."""
    transaction = delete_transaction(db=db, transaction_id=transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return None
