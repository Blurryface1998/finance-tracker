"""List, filter, and read transaction integration tests."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.core.exceptions.transactions import TransactionNotFoundError
from app.transactions.services import get_transaction
from tests.helpers import (TRANSACTIONS_URL, create_transaction,
                           create_transaction_json, transactions_url)


def test_get_transactions(authenticated_client):
    create_transaction(authenticated_client, amount="100.00")
    create_transaction(authenticated_client, amount="200.00")

    response = authenticated_client.get(TRANSACTIONS_URL)
    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "next_cursor" in data
    assert "has_next" in data

    assert len(data["items"]) == 2

    required_fields = {
        "id",
        "description",
        "amount",
        "category",
        "transaction_type",
        "created_at",
    }

    for item in data["items"]:
        assert required_fields.issubset(item.keys())

    assert data["items"][0]["amount"] == "200.00"
    assert data["items"][1]["amount"] == "100.00"


def test_get_transactions_empty(authenticated_client):
    """Ensure the list endpoint returns an empty payload when no transactions exist."""
    response = authenticated_client.get(TRANSACTIONS_URL)
    data = response.json()

    assert response.status_code == 200
    assert data["items"] == []
    assert data["next_cursor"] is None
    assert data["has_next"] is False


def test_get_transactions_default_limit(authenticated_client):
    """Ensure the default page size is capped correctly."""
    for i in range(25):
        create_transaction(authenticated_client, amount="10.00")

    response = authenticated_client.get(TRANSACTIONS_URL)
    data = response.json()

    assert len(data["items"]) <= 20


def test_get_transactions_limit_boundry(authenticated_client):
    """Ensure the requested limit is respected for list responses."""
    for i in range(10):
        create_transaction(authenticated_client, amount="10.00")
    response = authenticated_client.get(f"{TRANSACTIONS_URL}?limit=5")
    data = response.json()

    assert len(data["items"]) == 5


def test_get_transactions_invalid_limit(authenticated_client):
    """Ensure limits above the maximum are rejected."""
    response = authenticated_client.get(f"{TRANSACTIONS_URL}?limit=999")

    assert response.status_code == 422


def test_get_transactions_filter_by_category(authenticated_client):
    """Ensure category filtering returns only matching transactions."""
    create_transaction(authenticated_client, category="food")
    create_transaction(authenticated_client, category="travel")

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?category=food")
    data = response.json()

    assert all(item["category"] == "Food" for item in data["items"])


def test_get_transactions_filter_type(authenticated_client):
    """Ensure transaction type filtering works as expected."""
    create_transaction(authenticated_client, transaction_type="income", amount="100.00")
    create_transaction(authenticated_client, transaction_type="expense", amount="50.00")

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?transaction_type=income")
    data = response.json()

    assert all(item["transaction_type"] == "income" for item in data["items"])


def test_get_transactions_amount_range(authenticated_client):
    """Ensure amount range filtering returns matching transactions."""
    create_transaction(authenticated_client, amount="10.00")
    create_transaction(authenticated_client, amount="100.00")
    create_transaction(authenticated_client, amount="200.00")

    response = authenticated_client.get(
        f"{TRANSACTIONS_URL}?min_amount=50&max_amount=150"
    )
    data = response.json()

    amounts = [Decimal(item["amount"]) for item in data["items"]]

    assert all(50 <= amount <= 150 for amount in amounts)


def test_get_transactions_combined_filters(authenticated_client):
    """Ensure multiple filters can be combined successfully."""
    create_transaction(
        authenticated_client,
        transaction_type="income",
        category="food",
        amount="100.00",
    )
    create_transaction(
        authenticated_client,
        transaction_type="expense",
        category="food",
        amount="50.00",
    )
    create_transaction(
        authenticated_client,
        transaction_type="income",
        category="travel",
        amount="200.00",
    )

    response = authenticated_client.get(
        f"{TRANSACTIONS_URL}?transaction_type=income&category=food"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["items"][0]["transaction_type"] == "income"
    assert data["items"][0]["category"] == "Food"


def test_get_transactions_min_and_max_amount_together(authenticated_client):
    """Ensure min/max amount filters work together correctly."""
    create_transaction(authenticated_client, amount="30.00")
    create_transaction(authenticated_client, amount="70.00")
    create_transaction(authenticated_client, amount="120.00")

    response = authenticated_client.get(
        f"{TRANSACTIONS_URL}?min_amount=20&max_amount=100"
    )
    data = response.json()

    amounts = [Decimal(item["amount"]) for item in data["items"]]

    assert all(20 <= amount <= 100 for amount in amounts)


def test_get_transactions_last_page_has_no_cursor(authenticated_client):
    """Ensure the last page does not include a next cursor."""
    for i in range(5):
        create_transaction(authenticated_client, amount=str(i + 1))

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?limit=5")
    data = response.json()

    assert data["has_next"] is False
    assert data["next_cursor"] is None


def test_get_transactions_same_created_at_maintains_id_order(authenticated_client, db):
    """Ensure transactions with the same timestamp stay ordered by ID."""
    same_time = datetime(2026, 7, 1, 12, 0, 0, tzinfo=UTC)

    create_transaction(
        authenticated_client, db=db, amount="100.00", created_at=same_time
    )
    create_transaction(
        authenticated_client, db=db, amount="200.00", created_at=same_time
    )
    create_transaction(
        authenticated_client, db=db, amount="300.00", created_at=same_time
    )

    response = authenticated_client.get(f"{TRANSACTIONS_URL}")
    data = response.json()

    ids = [item["id"] for item in data["items"]]

    assert ids == sorted(ids, reverse=True)


def test_get_trasactions_cursor_pagination(authenticated_client):
    """Ensure cursor-based pagination returns a second page of results."""
    for i in range(10):
        create_transaction(authenticated_client, amount=str(i + 1))
    first = authenticated_client.get(f"{TRANSACTIONS_URL}?limit=5").json()
    cursor = first["next_cursor"]

    second = authenticated_client.get(
        f"{TRANSACTIONS_URL}?limit=5&cursor={cursor}"
    ).json()

    assert len(first["items"]) == 5
    assert len(second["items"]) == 5
    assert first["items"][0]["id"] != second["items"][0]["id"]


def test_get_transaction(authenticated_client):
    """Verify retrieval of a transaction by its ID."""
    created = create_transaction_json(authenticated_client, amount="150.00")
    transaction_id = created["id"]

    response = authenticated_client.get(transactions_url(transaction_id))

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "id": transaction_id,
        "description": "Salary",
        "amount": "150.00",
        "category": "Income",
        "transaction_type": "income",
        "created_at": data["created_at"],
    }


def test_get_transaction_raises_when_missing(db, test_user):
    """Ensure the service raises a not-found error for a missing transaction."""
    with pytest.raises(TransactionNotFoundError) as exc_info:
        get_transaction(db=db, transaction_id=999, current_user=test_user)

    assert "Transaction with id 999 not found" in str(exc_info.value)


def test_get_transaction_not_found(authenticated_client):
    """Ensure a missing transaction returns the expected API error."""
    response = authenticated_client.get(transactions_url(999))

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "transaction_not_found"
    assert "Transaction with id 999 not found" in response.json()["error"]["message"]


def test_get_transaction_invalid_id(authenticated_client):
    """Ensure invalid transaction IDs are rejected by validation."""
    response = authenticated_client.get(transactions_url("abc"))

    assert response.status_code == 422


def test_get_transaction_data_consistency(authenticated_client):
    """Ensure a fetched transaction matches the created payload."""
    created = create_transaction_json(authenticated_client, amount="250.00")
    transaction_id = created["id"]

    response = authenticated_client.get(transactions_url(transaction_id))
    data = response.json()

    assert data == created
