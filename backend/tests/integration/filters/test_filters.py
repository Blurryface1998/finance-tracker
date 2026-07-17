"""Filter-related transaction integration tests."""

from tests.helpers import TRANSACTIONS_URL, create_transaction


def test_filter_by_category(authenticated_client):
    create_transaction(authenticated_client, category="food")
    create_transaction(authenticated_client, category="travel")

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?category=food")
    data = response.json()

    assert response.status_code == 200
    assert all(item["category"] == "Food" for item in data["items"])


def test_filter_by_transaction_type(authenticated_client):
    """Ensure filtering by transaction type returns only matching items."""
    create_transaction(authenticated_client, transaction_type="income", amount="100.00")
    create_transaction(authenticated_client, transaction_type="expense", amount="50.00")

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?transaction_type=income")
    data = response.json()

    assert response.status_code == 200
    assert all(item["transaction_type"] == "income" for item in data["items"])


def test_filter_by_min_amount(authenticated_client):
    """Ensure min amount filtering returns only larger transactions."""
    create_transaction(authenticated_client, amount="10.00")
    create_transaction(authenticated_client, amount="100.00")

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?min_amount=50")
    data = response.json()

    assert response.status_code == 200
    assert all(float(item["amount"]) >= 50 for item in data["items"])


def test_filter_by_max_amount(authenticated_client):
    """Ensure max amount filtering returns only smaller transactions."""
    create_transaction(authenticated_client, amount="10.00")
    create_transaction(authenticated_client, amount="100.00")

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?max_amount=50")
    data = response.json()

    assert response.status_code == 200
    assert all(float(item["amount"]) <= 50 for item in data["items"])


def test_filter_invalid_min_amount(authenticated_client):
    """Ensure non-numeric min amount values are rejected."""
    response = authenticated_client.get(f"{TRANSACTIONS_URL}?min_amount=abc")

    assert response.status_code == 422


def test_filter_invalid_transaction_type(authenticated_client):
    """Ensure invalid transaction types are rejected by the filter endpoint."""
    response = authenticated_client.get(f"{TRANSACTIONS_URL}?transaction_type=bad")

    assert response.status_code == 422


def test_filter_by_category_case_insensitive(authenticated_client):
    """Ensure category filters are case-insensitive."""
    create_transaction(authenticated_client, category="Food")
    create_transaction(authenticated_client, category="Travel")

    response = authenticated_client.get(f"{TRANSACTIONS_URL}?category=food")
    data = response.json()

    assert response.status_code == 200
    assert all(item["category"] == "Food" for item in data["items"])
