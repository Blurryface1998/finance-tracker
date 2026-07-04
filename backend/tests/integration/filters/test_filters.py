"""Filter-related transaction integration tests."""

from tests.helpers import TRANSACTIONS_URL, create_transaction


def test_filter_by_category(client):
    create_transaction(client, category="food")
    create_transaction(client, category="travel")

    response = client.get(f"{TRANSACTIONS_URL}?category=food")
    data = response.json()

    assert response.status_code == 200
    assert all(item["category"] == "Food" for item in data["items"])


def test_filter_by_transaction_type(client):
    create_transaction(client, transaction_type="income", amount="100.00")
    create_transaction(client, transaction_type="expense", amount="50.00")

    response = client.get(f"{TRANSACTIONS_URL}?transaction_type=income")
    data = response.json()

    assert response.status_code == 200
    assert all(item["transaction_type"] == "income" for item in data["items"])


def test_filter_by_min_amount(client):
    create_transaction(client, amount="10.00")
    create_transaction(client, amount="100.00")

    response = client.get(f"{TRANSACTIONS_URL}?min_amount=50")
    data = response.json()

    assert response.status_code == 200
    assert all(float(item["amount"]) >= 50 for item in data["items"])


def test_filter_by_max_amount(client):
    create_transaction(client, amount="10.00")
    create_transaction(client, amount="100.00")

    response = client.get(f"{TRANSACTIONS_URL}?max_amount=50")
    data = response.json()

    assert response.status_code == 200
    assert all(float(item["amount"]) <= 50 for item in data["items"])


def test_filter_invalid_min_amount(client):
    response = client.get(f"{TRANSACTIONS_URL}?min_amount=abc")

    assert response.status_code == 422


def test_filter_invalid_transaction_type(client):
    response = client.get(f"{TRANSACTIONS_URL}?transaction_type=bad")

    assert response.status_code == 422


def test_filter_by_category_case_insensitive(client):
    create_transaction(client, category="Food")
    create_transaction(client, category="Travel")

    response = client.get(f"{TRANSACTIONS_URL}?category=food")
    data = response.json()

    assert response.status_code == 200
    assert all(item["category"] == "Food" for item in data["items"])
