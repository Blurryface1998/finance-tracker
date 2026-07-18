"""Update and patch transaction integration tests."""

import pytest

from app.core.exceptions.transactions import TransactionNotFoundError
from app.transactions.services import patch_transaction, update_transaction
from tests.helpers import (
    create_transaction,
    transactions_url,
    create_user,
    get_auth_headers,
)


def test_update_transaction(authenticated_client):
    create_response = create_transaction(authenticated_client, amount="100.00")
    created = create_response.json()
    transaction_id = created["id"]

    update_response = authenticated_client.put(
        transactions_url(transaction_id),
        json={
            "description": "Updated Salary",
            "amount": "250.00",
            "category": "income",
            "transaction_type": "income",
        },
    )
    assert update_response.status_code == 200
    update_response.json()

    get_response = authenticated_client.get(transactions_url(transaction_id))
    assert get_response.json()["amount"] == "250.00"


def test_udpate_raises_missing(db, test_user):
    """Ensure updating a missing transaction raises a not-found error."""
    with pytest.raises(TransactionNotFoundError) as exc_info:
        update_transaction(
            db=db,
            transaction_id=999,
            data={
                "description": "Food Purchase",
                "amount": "100.00",
                "category": "food",
                "transaction_type": "expense",
            },
            current_user=test_user,
        )

    assert "Transaction with id 999 not found" in str(exc_info.value)


def test_update_transaction_not_found(authenticated_client):
    """Ensure updating a missing transaction returns the expected API error."""
    response = authenticated_client.put(
        transactions_url(999),
        json={
            "description": "Food Purchase",
            "amount": "100.00",
            "category": "food",
            "transaction_type": "expense",
        },
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "transaction_not_found"
    assert "Transaction with id 999 not found" in response.json()["error"]["message"]


def test_update_transaction_invalid_id(authenticated_client):
    """Ensure invalid transaction IDs are rejected by the update endpoint."""
    response = authenticated_client.put(
        transactions_url("abc"),
        json={
            "description": "Food Purchase",
            "amount": "100.00",
            "category": "food",
            "transaction_type": "income",
        },
    )

    assert response.status_code == 422


def test_update_transaction_invalid_payload(authenticated_client):
    """Ensure invalid update payloads are rejected with validation errors."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.put(
        transactions_url(transaction_id),
        json={
            "description": "",
            "amount": "-50",
            "category": "food",
            "transaction_type": "expense",
        },
    )

    assert response.status_code == 422


def test_update_transaction_normalization(authenticated_client):
    """Ensure update requests normalize text fields correctly."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.put(
        transactions_url(transaction_id),
        json={
            "description": " updated salary  ",
            "amount": "250.00",
            "category": "income  ",
            "transaction_type": "income",
        },
    )

    data = response.json()

    assert data["description"] == "Updated Salary"
    assert data["category"] == "Income"


def test_update_transaction_id_unchanged(authenticated_client):
    """Ensure the transaction ID remains unchanged after an update."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.put(
        transactions_url(transaction_id),
        json={
            "description": "Updated",
            "amount": "250.00",
            "category": "Income",
            "transaction_type": "income",
        },
    )

    data = response.json()

    assert data["id"] == transaction_id


def test_user_cannot_update_another_user_transaction(client):
    create_user(
        client=client,
    )
    create_user(
        client=client,
        username="jhane_doe",
        email="jhane_doe@example.com",
    )

    user_one_headers = get_auth_headers(client=client)
    user_two_headers = get_auth_headers(client=client, email="jhane_doe@example.com")

    create_response = create_transaction(
        client=client,
        headers=user_one_headers,
    )
    transaction_id = create_response.json()["id"]

    response = client.put(
        transactions_url(transaction_id),
        json={
            "description": "Updated",
            "amount": "100.00",
            "category": "Income",
            "transaction_type": "income",
        },
        headers=user_two_headers,
    )
    assert response.status_code == 404


def test_patch_transaction(authenticated_client):
    """Ensure patch updates a single field successfully."""
    create_response = create_transaction(authenticated_client, amount="100.00")
    created = create_response.json()
    transaction_id = created["id"]

    patch_payload = {"amount": "250.00"}

    patch_response = authenticated_client.patch(
        transactions_url(transaction_id), json=patch_payload
    )
    assert patch_response.status_code == 200

    data = patch_response.json()

    assert data["id"] == transaction_id
    assert data["amount"] == "250.00"
    assert data["description"] == "Salary"
    assert data["transaction_type"] == "income"


def test_patch_transaction_multiple_fields(authenticated_client):
    """Ensure patch requests can update multiple fields at once."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id),
        json={
            "description": "Gaming",
            "category": "Entertainment",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "Gaming"
    assert data["category"] == "Entertainment"
    assert data["amount"] == "100.00"


def test_patch_transaction_type_only(authenticated_client):
    """Ensure patch requests can update the transaction type alone."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id),
        json={"transaction_type": "expense"},
    )

    assert response.status_code == 200
    assert response.json()["transaction_type"] == "expense"


def test_patch_transaction_invalid_description_length(authenticated_client):
    """Ensure patch requests reject invalid description lengths."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id),
        json={"description": "a" * 51},
    )

    assert response.status_code == 422


def test_patch_transaction_invalid_category_length(authenticated_client):
    """Ensure patch requests reject invalid category lengths."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id),
        json={"category": "b" * 51},
    )

    assert response.status_code == 422


def test_patch_transaction_preserves_created_at(authenticated_client):
    """Ensure patch requests do not modify the original creation timestamp."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]
    original_created_at = created["created_at"]

    response = authenticated_client.patch(
        transactions_url(transaction_id), json={"amount": "200.00"}
    )

    assert response.status_code == 200
    assert response.json()["created_at"] == original_created_at


def test_patch_transaction_raises_missing(db, test_user):
    """Ensure patching a missing transaction raises a not-found error."""
    with pytest.raises(TransactionNotFoundError) as exc_info:
        patch_transaction(
            db=db, transaction_id=999, data={"amount": "200.00"}, current_user=test_user
        )
    assert "Transaction with id 999 not found" in str(exc_info.value)


def test_patch_transaction_not_found(authenticated_client):
    """Ensure patching a missing transaction returns the expected API error."""
    response = authenticated_client.patch(
        transactions_url(999), json={"amount": "200.00"}
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "transaction_not_found"
    assert "Transaction with id 999 not found" in response.json()["error"]["message"]


def test_patch_transaction_invalid_id(authenticated_client):
    """Ensure invalid transaction IDs are rejected by the patch endpoint."""
    response = authenticated_client.patch(
        transactions_url("abc"), json={"amount": "200.00"}
    )

    assert response.status_code == 422


def test_patch_transaction_invalid_amount(authenticated_client):
    """Ensure patch requests reject negative amounts."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id), json={"amount": "-10"}
    )

    assert response.status_code == 422


def test_patch_transaction_zero_amount(authenticated_client):
    """Ensure patch requests reject zero amounts."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id), json={"amount": "0"}
    )

    assert response.status_code == 422


def test_patch_transaction_normalizes_text(authenticated_client):
    """Ensure patch requests normalize text fields correctly."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id),
        json={"description": "  gaming pc  ", "category": "  entertainment  "},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "Gaming Pc"
    assert data["category"] == "Entertainment"


def test_patch_transaction_empty_payload(authenticated_client):
    """Ensure an empty patch payload is accepted without changing the transaction."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(transactions_url(transaction_id), json={})

    assert response.status_code == 200


def test_patch_transaction_preserves_unmodified_fields(authenticated_client):
    """Ensure patch requests leave other fields unchanged."""
    create_response = create_transaction(authenticated_client)
    created = create_response.json()
    transaction_id = created["id"]

    response = authenticated_client.patch(
        transactions_url(transaction_id),
        json={"amount": "300.00"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "Salary"
    assert data["category"] == "Income"
    assert data["transaction_type"] == "income"
    assert data["amount"] == "300.00"


def test_user_cannot_patch_another_user_transaction(client):
    create_user(
        client=client,
    )
    create_user(
        client=client,
        username="jhane_doe",
        email="jhane_doe@example.com",
    )

    user_one_headers = get_auth_headers(client=client)
    user_two_headers = get_auth_headers(client=client, email="jhane_doe@example.com")

    create_response = create_transaction(
        client=client,
        headers=user_one_headers,
    )
    transaction_id = create_response.json()["id"]

    response = client.patch(
        transactions_url(transaction_id),
        json={"amount": "250.00"},
        headers=user_two_headers,
    )

    assert response.status_code == 404

    check = client.get(transactions_url(transaction_id), headers=user_one_headers)

    assert check.json()["amount"] == "100.00"
