"""Delete transaction integration tests."""

from tests.helpers import (create_transaction, create_transaction_json,
                           transactions_url)


def test_delete_transaction_not_found(client):
    response = client.delete(transactions_url(999))

    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found"}


def test_delete_transaction_removes_transaction(client):
    """Verify deleting a transaction removes it from the store."""
    created = create_transaction_json(client)
    transaction_id = created["id"]

    delete_response = client.delete(transactions_url(transaction_id))
    assert delete_response.status_code == 204

    get_response = client.get(transactions_url(transaction_id))

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Transaction not found"}


def test_delete_transaction_invalid_id(client):
    response = client.delete(transactions_url("abc"))

    assert response.status_code == 422


def test_delete_transaction_twice(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.delete(transactions_url(transaction_id))
    assert response.status_code == 204

    response = client.delete(transactions_url(transaction_id))
    assert response.status_code == 404
