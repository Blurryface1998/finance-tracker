"""Integration tests for transaction CRUD operations and listing."""


from tests.helpers import create_transaction


def test_create(client):
    """Verify creating a transaction returns HTTP 201 and the transaction is listed."""
    response = create_transaction(client=client, amount="200.00")

    assert response.status_code == 201

    data = client.get("/transactions").json()

    assert len(data["items"]) == 1

    assert data["items"][0]["amount"] == "200.00"


def test_multiple_create(client):
    """Verify multiple transactions are created and returned in descending order."""
    create_transaction(client, amount="100.00")
    create_transaction(client, amount="200.00")
    create_transaction(client, amount="300.00")

    data = client.get("/transactions").json()

    assert len(data["items"]) == 3

    amounts = [item["amount"] for item in data["items"]]

    assert amounts == ["300.00", "200.00", "100.00"]


def test_litst_transctions(client):
    """Verify transaction list responses include all expected fields."""
    create_transaction(client, amount="100.00")

    data = client.get("/transactions").json()
    item = data["items"][0]

    assert all(
        key in item for key in ["id", "amount", "created_at", "transaction_type"]
    )


def test_get_transaction(client):
    """Placeholder for verifying retrieval of a single transaction by ID."""
    pass


def test_update_transaction(client):
    create_response = create_transaction(client, amount="100.00")
    created = create_response.json()
    transaction_id = created["id"]

    response = client.put(
        f"/transactions/{transaction_id}",
        json={
            "description": "Updated Salary",
            "amount": "250.00",
            "category": "income",
            "transaction_type": "income",
        },
    )
    assert response.status_code == 200
    data = response.json()

    get_response = client.get(f"/transactions/{transaction_id}")
    assert get_response.json()["amount"] == "250.00"


def test_delete_transaction():
    """Placeholder for verifying deletion of an existing transaction."""
    pass
