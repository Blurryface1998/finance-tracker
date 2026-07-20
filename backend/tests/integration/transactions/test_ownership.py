
from tests.helpers import (create_transaction, create_user, get_auth_headers,
                           transactions_url)


def test_user_cannot_get_another_user_transaction(client):
    create_user(client=client)
    create_user(client=client, username="jhane_doe", email="jhane_doe@example.com")

    user_one_headers = get_auth_headers(client=client)
    user_two_headers = get_auth_headers(client=client, email="jhane_doe@example.com")

    create_response = create_transaction(client, headers=user_one_headers)
    transaction_id = create_response.json()["id"]

    response = client.get(transactions_url(transaction_id), headers=user_two_headers)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "transaction_not_found"


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


def test_user_cannot_delete_another_user_transaction(client):
    create_user(client=client)
    create_user(client=client, username="jhane_doe", email="jhane_doe@example.com")

    user_one_headers = get_auth_headers(client=client)
    user_two_headers = get_auth_headers(client=client, email="jhane_doe@example.com")

    create_response = create_transaction(client, headers=user_two_headers)
    transaction_id = create_response.json()["id"]

    response = client.delete(transactions_url(transaction_id), headers=user_one_headers)
    assert response.status_code == 404
