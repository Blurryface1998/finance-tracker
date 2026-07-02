"""Integration tests for transaction summary endpoints."""

from decimal import Decimal

from tests.helpers import create_transaction


def test_monthly_summary(client):
    """Verify monthly summary returns total income for the requested month."""
    create_transaction(client, amount="100")
    create_transaction(client, amount="200")

    response = client.get("/transactions/summary?month=2026-07")

    data = response.json()

    assert Decimal(data["income"]) == Decimal("300")


def test_summary_income_and_expenses(client):
    create_transaction(client, amount=2000, transaction_type="income")
    create_transaction(client, amount=500, transaction_type="expense")

    response = client.get("/transactions/summary?month=2026-07")

    data = response.json()

    assert Decimal(data["income"]) == Decimal("2000")


def test_yearly_summary(client):
    """Verify yearly summary includes the expected income for the current month."""
    create_transaction(client, amount="1000", transaction_type="income")
    create_transaction(client, amount="200", transaction_type="expense")

    response = client.get("/transactions/summary/yearly?year=2026")
    data = response.json()

    july_data = next(
        monthly_record
        for monthly_record in data["months"]
        if monthly_record["month"] == 7
    )
    assert Decimal(july_data["income"]) == Decimal("1000")


def test_summary_empty_month():
    """Placeholder for verifying an empty month returns zero totals."""
    pass


def test_summary_with_no_transactions():
    """Placeholder for verifying summary returns zero values when no transactions exist."""
    pass


def test_summary_with_no_expenses():
    """Placeholder for verifying summary handles months with only income."""
    pass


def test_summary_with_only_income():
    """Placeholder for verifying income-only summary calculations."""
    pass
