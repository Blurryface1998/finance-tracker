from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services import create_transaction_service, get_transactions_service, get_transaction_service, update_transaction_service, delete_transaction_service, get_monthly_summary_service
from app.database import get_db
from decimal import Decimal

router = APIRouter()

@router.get("/transactions", response_model=list[TransactionResponse])
async def get_transactions(
    type: str | None = None,
    category: str | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    db: Session = Depends(get_db),
):
    """Return a list of transactions filtered by optional query parameters."""
    return get_transactions_service(db, type, category, min_amount, max_amount)


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    """Return a single transaction by ID."""
    transaction = get_transaction_service(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction
@router.get("/transactions/summary")
async def get_monthly_summary(month: str, db: Session = Depends(get_db)):
    """Return a monthly summary for income and expenses."""
    return get_monthly_summary_service(db, month)


@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    """Create a new transaction."""
    return create_transaction_service(db, transaction)

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing transaction by ID."""
    updated_transaction = update_transaction_service(
        db,
        transaction_id,
        transaction,
    )

    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return updated_transaction


@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    """Delete an existing transaction by ID."""
    transaction = delete_transaction_service(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)