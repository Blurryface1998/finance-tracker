"""List, filter, and read transaction integration tests."""

from decimal import Decimal

from tests.helpers import (TRANSACTIONS_URL, create_transaction,
                           create_transaction_json, transactions_url)


def test_get_transactions(client):
    create_transaction(client, amount="100.00")
    create_transaction(client, amount="200.00")

    response = client.get(TRANSACTIONS_URL)
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


def test_get_transactions_empty(client):
    response = client.get(TRANSACTIONS_URL)
    data = response.json()

    assert response.status_code == 200
    assert data["items"] == []
    assert data["next_cursor"] is None
    assert data["has_next"] is False


def test_get_transactions_default_limit(client):
    for i in range(25):
        create_transaction(client, amount="10.00")

    response = client.get(TRANSACTIONS_URL)
    data = response.json()

    assert len(data["items"]) <= 20


def test_get_transactions_limit_boundry(client):
    for i in range(10):
        create_transaction(client, amount="10.00")
    response = client.get(f"{TRANSACTIONS_URL}?limit=5")
    data = response.json()

    assert len(data["items"]) == 5


def test_get_transactions_invalid_limit(client):
    response = client.get(f"{TRANSACTIONS_URL}?limit=999")

    assert response.status_code == 422


def test_get_transactions_filter_by_category(client):
    create_transaction(client, category="food")
    create_transaction(client, category="travel")

    response = client.get(f"{TRANSACTIONS_URL}?category=food")
    data = response.json()

    assert all(item["category"] == "Food" for item in data["items"])


def test_get_transactions_filter_type(client):
    create_transaction(client, transaction_type="income", amount="100.00")
    create_transaction(client, transaction_type="expense", amount="50.00")

    response = client.get(f"{TRANSACTIONS_URL}?transaction_type=income")
    data = response.json()

    assert all(item["transaction_type"] == "income" for item in data["items"])


def test_get_transactions_amount_range(client):
    create_transaction(client, amount="10.00")
    create_transaction(client, amount="100.00")
    create_transaction(client, amount="200.00")

    response = client.get(f"{TRANSACTIONS_URL}?min_amount=50&max_amount=150")
    data = response.json()

    amounts = [Decimal(item["amount"]) for item in data["items"]]

    assert all(50 <= amount <= 150 for amount in amounts)


def test_get_trasactions_cursor_pagination(client):
    for i in range(10):
        create_transaction(client, amount=str(i + 1))
    first = client.get(f"{TRANSACTIONS_URL}?limit=5").json()
    cursor = first["next_cursor"]

    second = client.get(f"{TRANSACTIONS_URL}?limit=5&cursor={cursor}").json()

    assert len(first["items"]) == 5
    assert len(second["items"]) == 5
    assert first["items"][0]["id"] != second["items"][0]["id"]


def test_get_transaction(client):
    """Verify retrieval of a transaction by its ID."""
    created = create_transaction_json(client, amount="150.00")
    transaction_id = created["id"]

    response = client.get(transactions_url(transaction_id))

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


def test_get_transction_not_found(client):
    response = client.get(transactions_url(999))

    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found"}


def test_get_transaction_invalid_id(client):
    response = client.get(transactions_url("abc"))

    assert response.status_code == 422


def test_get_transaction_data_consistency(client):
    created = create_transaction_json(client, amount="250.00")
    transaction_id = created["id"]

    response = client.get(transactions_url(transaction_id))
    data = response.json()

    assert data == created
