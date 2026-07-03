"""Update and patch transaction integration tests."""

from tests.helpers import create_transaction, transactions_url


def test_update_transaction(client):
    create_response = create_transaction(client, amount="100.00")
    created = create_response.json()
    transaction_id = created["id"]

    update_response = client.put(
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

    get_response = client.get(transactions_url(transaction_id))
    assert get_response.json()["amount"] == "250.00"


def test_update_transaction_not_found(client):
    response = client.put(
        transactions_url(9999),
        json={
            "description": "Food Purchase",
            "amount": "100.00",
            "category": "food",
            "transaction_type": "expense",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found"}


def test_update_transaction_invalid_id(client):
    response = client.put(
        transactions_url("abc"),
        json={
            "description": "Food Purchase",
            "amount": "100.00",
            "category": "food",
            "transaction_type": "income",
        },
    )

    assert response.status_code == 422


def test_update_transaction_invalid_payload(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.put(
        transactions_url(transaction_id),
        json={
            "description": "",
            "amount": "-50",
            "category": "food",
            "transaction_type": "expense",
        },
    )

    assert response.status_code == 422


def test_update_transaction_normalization(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.put(
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


def test_update_transaction_id_unchanged(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.put(
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


def test_patch_transaction(client):
    create_response = create_transaction(client, amount="100.00")
    created = create_response.json()
    transaction_id = created["id"]

    patch_payload = {"amount": "250.00"}

    patch_response = client.patch(transactions_url(transaction_id), json=patch_payload)
    assert patch_response.status_code == 200

    data = patch_response.json()

    assert data["id"] == transaction_id
    assert data["amount"] == "250.00"
    assert data["description"] == "Salary"
    assert data["transaction_type"] == "income"


def test_patch_transaction_multiple_fields(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.patch(
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


def test_patch_transaction_not_found(client):
    response = client.patch(transactions_url(9999), json={"amount": "200.00"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found"}


def test_patch_transaction_invalid_id(client):
    response = client.patch(transactions_url("abc"), json={"amount": "200.00"})

    assert response.status_code == 422


def test_patch_transaction_invalid_amount(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.patch(transactions_url(transaction_id), json={"amount": "-10"})

    assert response.status_code == 422


def test_patch_transaction_zero_amount(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.patch(transactions_url(transaction_id), json={"amount": "0"})

    assert response.status_code == 422


def test_patch_transaction_normalizes_text(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.patch(
        transactions_url(transaction_id),
        json={"description": "  gaming pc  ", "category": "  entertainment  "},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "Gaming Pc"
    assert data["category"] == "Entertainment"


def test_patch_transaction_empty_payload(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.patch(transactions_url(transaction_id), json={})

    assert response.status_code == 200


def test_patch_transaction_preserves_unmodified_fields(client):
    create_response = create_transaction(client)
    created = create_response.json()
    transaction_id = created["id"]

    response = client.patch(
        transactions_url(transaction_id),
        json={"amount": "300.00"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "Salary"
    assert data["category"] == "Income"
    assert data["transaction_type"] == "income"
    assert data["amount"] == "300.00"
