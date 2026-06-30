from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (CategorySummary, PaginatedResponse, TransactionCreate,
                         TransactionPatch, TransactionResponse,
                         TransactionType, TransactionUpdate)
from app.services.analytics_services import (get_category_summary,
                                             get_monthly_summary)
from app.services.transaction_services import (create_transaction,
                                               delete_transaction,
                                               get_transaction,
                                               get_transactions,
                                               patch_transaction,
                                               update_transaction)

router = APIRouter()


@router.get("/transactions", response_model=PaginatedResponse[TransactionResponse])
async def get_transactions_route(
    transaction_type: TransactionType | None = None,
    category: str | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    limit: int = 20,
    cursor: int | None = None,
    db: Session = Depends(get_db),
):
    """Return paginated transactions with optional filters and cursor-based paging."""
    return get_transactions(
        db=db,
        transaction_type=transaction_type,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
        limit=limit,
        cursor=cursor,
    )


@router.get("/transactions/summary")
async def get_monthly_summary_route(
    month: Annotated[str, Query(pattern=r"\d{4}-\d{2}")], db: Session = Depends(get_db)
):
    """Return a monthly summary for income and expenses."""
    return get_monthly_summary(db=db, month=month)


@router.get("/transactions/category-breakdown", response_model=list[CategorySummary])
def get_category_summary_route(db: Session = Depends(get_db)):
    return get_category_summary(db)


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    """Return a single transaction by ID."""
    transaction = get_transaction(db=db, transaction_id=transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction


@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction_route(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    """Create a new transaction."""
    return create_transaction(db, transaction)


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
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


@router.patch("/transactions/{transaction_id}", response_model=TransactionResponse)
async def patch_transaction_route(
    transaction_id: int, transaction: TransactionPatch, db: Session = Depends(get_db)
):
    updated = patch_transaction(db=db, transaction_id=transaction_id, data=transaction)

    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return updated


@router.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    """Delete an existing transaction by ID."""
    transaction = delete_transaction(db=db, transaction_id=transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return None
