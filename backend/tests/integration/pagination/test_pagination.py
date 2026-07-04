"""Pagination-related transaction integration tests."""

from datetime import UTC, datetime

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


def test_exact_limit_no_more_pages(client):
    for i in range(5):
        create_transaction(client, amount=str(i + 1))

    response = client.get(f"{TRANSACTIONS_URL}?limit=5")
    data = response.json()

    assert response.status_code == 200
    assert len(data["items"]) == 5
    assert data["has_next"] is False
    assert data["next_cursor"] is None


def test_limit_boundary_values(client):
    create_transaction(client, amount="10.00")

    response = client.get(f"{TRANSACTIONS_URL}?limit=1")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1

    for i in range(50):
        create_transaction(client, amount=str(i + 1))

    response = client.get(f"{TRANSACTIONS_URL}?limit=50")
    assert response.status_code == 200
    assert len(response.json()["items"]) <= 50


def test_cursor_pagination_with_same_created_at(client, db):
    same_time = datetime(2026, 7, 1, 12, 0, 0, tzinfo=UTC)
    for i in range(6):
        create_transaction(client, db=db, amount=str(i + 1), created_at=same_time)

    first = client.get(f"{TRANSACTIONS_URL}?limit=3").json()
    second = client.get(
        f"{TRANSACTIONS_URL}?limit=3&cursor={first['next_cursor']}"
    ).json()

    first_ids = [item["id"] for item in first["items"]]
    second_ids = [item["id"] for item in second["items"]]

    assert first_ids == sorted(first_ids, reverse=True)
    assert second_ids == sorted(second_ids, reverse=True)
    assert set(first_ids).isdisjoint(second_ids)
