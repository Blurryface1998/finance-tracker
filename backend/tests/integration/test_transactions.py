"""Integration tests for transaction CRUD operations and listing."""

from decimal import Decimal

from tests.helpers import (
    TRANSACTIONS_URL,
    create_transaction,
    create_transaction_json,
    transactions_url,
)


def test_create(client):
    """Verify creating a transaction returns HTTP 201 and the transaction is listed."""
    response = create_transaction(client=client, amount="200.00")

    assert response.status_code == 201

    data = client.get(TRANSACTIONS_URL).json()

    assert len(data["items"]) == 1

    assert data["items"][0]["amount"] == "200.00"


def test_create_amount_zero_fails(client):
    """Verify zero amounts are rejected with validation errors."""
    response = create_transaction(client, amount="0")

    assert response.status_code == 422


def test_create_negative_amount_fails(client):
    """Verify negative amounts are rejected with validation errors."""
    response = create_transaction(client, amount="-100")

    assert response.status_code == 422


def test_create_empty_description_fails(client):
    """Verify empty descriptions are rejected with validation errors."""
    response = create_transaction(client, description="")

    assert response.status_code == 422


def test_create_invalid_type_fails(client):
    """Verify invalid transaction types are rejected with validation errors."""
    response = create_transaction(client, transaction_type="invalid")

    assert response.status_code == 422


def test_create_normalization(client):
    response = create_transaction(
        client, description="  salary payment  ", category="  income  "
    )

    data = response.json()

    assert data["description"] == "Salary Payment"
    assert data["category"] == "Income"


def test_create_accepts_integer_amount(client):
    response = create_transaction(client, amount=100)

    assert response.status_code == 201
    assert response.json()["amount"] == "100.00"


def test_create_keeps_decimal_precision(client):
    response = create_transaction(client, amount="100.5")

    assert response.json()["amount"] == "100.50"


def test_create_missing_fields_fails(client):
    response = client.post(TRANSACTIONS_URL, json={})

    assert response.status_code == 422


def test_multiple_create(client):
    """Verify multiple transactions are created and returned in descending order."""
    create_transaction(client, amount="100.00")
    create_transaction(client, amount="200.00")
    create_transaction(client, amount="300.00")

    data = client.get(TRANSACTIONS_URL).json()

    assert len(data["items"]) == 3

    amounts = [item["amount"] for item in data["items"]]

    assert amounts == ["300.00", "200.00", "100.00"]


def test_multiple_create_ids_unique(client):
    create_transaction(client, amount="100.00")
    create_transaction(client, amount="200.00")
    create_transaction(client, amount="300.00")

    data = client.get(TRANSACTIONS_URL).json()
    ids = [item["id"] for item in data["items"]]

    assert len(ids) == len(set(ids))


def test_multiple_create_fields_present(client):
    create_transaction(client, amount="100.00")

    data = client.get(TRANSACTIONS_URL).json()
    item = data["items"][0]

    required_fields = {
        "id",
        "description",
        "amount",
        "category",
        "transaction_type",
        "created_at",
    }

    assert required_fields.issubset(item.keys())


def test_multiple_create_decimal_formats(client):
    create_transaction(client, amount="100")
    create_transaction(client, amount="200.5")

    data = client.get(TRANSACTIONS_URL).json()
    amounts = [item["amount"] for item in data["items"]]

    assert "100.00" in amounts
    assert "200.50" in amounts


def test_multiple_create_many_items(client):
    for i in range(20):
        create_transaction(client, amount=str(i + 1))

    data = client.get(f"{TRANSACTIONS_URL}?limit=50").json()

    assert len(data["items"]) == 20


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
    resonse = client.get(f"{TRANSACTIONS_URL}?limit=999")

    assert resonse.status_code == 422


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

    amounts = [Decimal(i["amount"]) for i in data["items"]]

    assert all(50 <= a <= 150 for a in amounts)


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
    data = update_response.json()

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


def trst_udpate_transaction_invalid_id(client):
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
