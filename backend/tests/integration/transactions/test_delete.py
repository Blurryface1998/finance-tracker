"""Delete transaction integration tests."""

import pytest

from app.core.exceptions.transactions import TransactionNotFoundError
from app.services.transaction_services import delete_transaction
from tests.helpers import (create_transaction, create_transaction_json,
                           transactions_url)


def test_delete_transaction_raises_missing(db):
    """Ensure deleting a missing transaction raises a not-found error."""
    with pytest.raises(TransactionNotFoundError) as exc_info:
        delete_transaction(db=db, transaction_id=999)
    assert "Transaction with id 999 not found" in str(exc_info.value)


def test_delete_transaction_not_found(client):
    """Ensure deleting a missing transaction returns the expected API error."""
    response = client.delete(transactions_url(999))

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "transaction_not_found"
    assert "Transaction with id 999 not found" in response.json()["error"]["message"]


def test_delete_transaction_removes_transaction(client):
    """Verify deleting a transaction removes it from the store."""
    created = create_transaction_json(client)
    transaction_id = created["id"]

    delete_response = client.delete(transactions_url(transaction_id))
    assert delete_response.status_code == 204

    get_response = client.get(transactions_url(transaction_id))

    assert get_response.status_code == 404
    assert get_response.json()["error"]["code"] == "transaction_not_found"
    assert (
        f"Transaction with id {transaction_id} not found"
        in get_response.json()["error"]["message"]
    )


def test_delete_transaction_invalid_id(client):
    """Ensure invalid transaction IDs are rejected for deletes."""
    response = client.delete(transactions_url("abc"))

    assert response.status_code == 422


def test_delete_transaction_twice(client):
    """Ensure deleting the same transaction twice returns a not-found error."""
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.delete(transactions_url(transaction_id))
    assert response.status_code == 204

    response = client.delete(transactions_url(transaction_id))
    assert response.status_code == 404
