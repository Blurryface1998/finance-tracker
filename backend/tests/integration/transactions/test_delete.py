"""Delete transaction integration tests."""

import pytest

from app.core.exceptions.transactions import TransactionNotFoundError
from app.transactions.services import delete_transaction
from tests.helpers import (
    create_transaction,
    create_transaction_json,
    transactions_url,
    create_user,
    login_user,
    get_auth_headers,
)


def test_delete_transaction_raises_missing(db, test_user):
    """Ensure deleting a missing transaction raises a not-found error."""
    with pytest.raises(TransactionNotFoundError) as exc_info:
        delete_transaction(db=db, transaction_id=999, current_user=test_user)
    assert "Transaction with id 999 not found" in str(exc_info.value)


def test_delete_transaction_not_found(authenticated_client):
    """Ensure deleting a missing transaction returns the expected API error."""
    response = authenticated_client.delete(transactions_url(999))

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "transaction_not_found"
    assert "Transaction with id 999 not found" in response.json()["error"]["message"]


def test_delete_transaction_removes_transaction(authenticated_client):
    """Verify deleting a transaction removes it from the store."""
    created = create_transaction_json(authenticated_client)
    transaction_id = created["id"]

    delete_response = authenticated_client.delete(transactions_url(transaction_id))
    assert delete_response.status_code == 204

    get_response = authenticated_client.get(transactions_url(transaction_id))

    assert get_response.status_code == 404
    assert get_response.json()["error"]["code"] == "transaction_not_found"
    assert (
        f"Transaction with id {transaction_id} not found"
        in get_response.json()["error"]["message"]
    )


def test_delete_transaction_invalid_id(authenticated_client):
    """Ensure invalid transaction IDs are rejected for deletes."""
    response = authenticated_client.delete(transactions_url("abc"))

    assert response.status_code == 422


def test_delete_transaction_twice(authenticated_client):
    """Ensure deleting the same transaction twice returns a not-found error."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.delete(transactions_url(transaction_id))
    assert response.status_code == 204

    response = authenticated_client.delete(transactions_url(transaction_id))
    assert response.status_code == 404


def test_user_cannot_delete_another_user_transaction(client):
    create_user(client=client)
    create_user(client=client, username="jhane_doe", email="jhane_doe@example.com")

    user_one_headers = get_auth_headers(client=client)
    user_two_headers = get_auth_headers(client=client, email="jhane_doe@example.com")

    create_response = create_transaction(client, headers=user_two_headers)
    transaction_id = create_response.json()["id"]

    response = client.delete(transactions_url(transaction_id), headers=user_one_headers)
    assert response.status_code == 404
