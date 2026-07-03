"""Pagination-related transaction integration tests."""

from tests.helpers import TRANSACTIONS_URL, create_transaction


def test_first_page(client):
    for i in range(10):
        create_transaction(client, amount=str(i + 1))

    response = client.get(f"{TRANSACTIONS_URL}?limit=5")
    data = response.json()

    assert response.status_code == 200
    assert len(data["items"]) == 5
    assert data["has_next"] is True


def test_next_page(client):
    for i in range(10):
        create_transaction(client, amount=str(i + 1))

    first = client.get(f"{TRANSACTIONS_URL}?limit=5").json()
    cursor = first["next_cursor"]
    second = client.get(f"{TRANSACTIONS_URL}?limit=5&cursor={cursor}").json()

    assert len(first["items"]) == 5
    assert len(second["items"]) == 5
    assert first["items"][0]["id"] != second["items"][0]["id"]


def test_invalid_cursor(client):
    response = client.get(f"{TRANSACTIONS_URL}?limit=5&cursor=invalid")

    assert response.status_code == 422


def test_limit(client):
    for i in range(10):
        create_transaction(client, amount=str(i + 1))

    response = client.get(f"{TRANSACTIONS_URL}?limit=3")
    data = response.json()

    assert response.status_code == 200
    assert len(data["items"]) == 3
