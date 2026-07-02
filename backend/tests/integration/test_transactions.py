from app.models import Transaction
from decimal import Decimal
from tests.helpers import create_transaction


def test_create(client):
    response = create_transaction(client=client, amount="200.00")

    assert response.status_code == 201

    response = client.get("/transactions")
    data = response.json()

    assert len(data["items"]) == 1

    assert data["items"][0]["amount"] == "200.00"


def test_multiple_create(client):
    create_transaction(client, amount=100)
    create_transaction(client, amount=200)
    create_transaction(client, amount=300)

    response = client.get("/transactions")
    data = response.json()

    assert len(data["items"]) == 3
    assert data["items"][0]["amount"] == "300.00"
    assert data["items"][1]["amount"] == "200.00"
    assert data["items"][2]["amount"] == "100.00"


def test_litst_transctions(client):
    create_transaction(client, amount="100.00")

    response = client.get("/transactions")
    data = response.json()

    item = data["items"][0]

    assert "id" in item
    assert "amount" in item
    assert "created_at" in item
    assert "transaction_type" in item


def test_get_transaction(client):
    pass


def test_update_transaction(client):
    create_response = create_transaction(client, amount="100.00")
    created = create_response.json()
    transaction_id = created["id"]

    update_payload = {
        "description": "Updated Salary",
        "amount": "250.00",
        "category": "income",
        "transaction_type": "income",
    }

    response = client.put(f"/transactions/{transaction_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == transaction_id
    assert data["description"] == "Updated Salary"
    assert data["amount"] == "250.00"


def test_delete_transaction():
    pass
