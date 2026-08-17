from tests.helpers import create_user, login_user


def test_register_user(client):
    """Verify that a user can register successfully and receives user details."""
    response = create_user(
        client=client,
        name="John",
        last_name="Doe",
        email="john_doe@example.com",
        password="Mypassword1234567",
    )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "john_doe@example.com"
    assert data["name"] == "John"
    assert data["last_name"] == "Doe"
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_email_fails(client):
    """Verify duplicate email registration returns a conflict error."""
    create_user(client=client, email="john_doe@example.com")

    response = create_user(client=client, email="john_doe@example.com")

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "email_registered"


def test_login_user(client):
    """Verify an existing user can log in successfully."""
    create_user(
        client=client,
        username="john_doe",
        email="john_doe@example.com",
        password="Mypassword1234567",
    )

    response = login_user(
        client=client,
        email="john_doe@example.com",
        password="Mypassword1234567",
    )

    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password_fails(client):
    """Verify invalid credentials are rejected with the proper error code."""
    create_user(client=client, email="john_doe@example.com")

    response = login_user(
        client=client,
        email="john_doe@example.com",
        password="wrongpassword",
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"


def test_register_invalid_password_fails(client):
    """Verify registration fails when password is too short."""
    response = create_user(
        client=client,
        username="john_doe",
        email="john_doe@example.com",
        password="short",
    )

    assert response.status_code == 422


def test_register_invalid_email_fails(client):
    """Verify registration fails with invalid email format."""
    response = create_user(
        client=client,
        username="john_doe",
        email="not-an-email",
        password="Mypassword1234567",
    )

    assert response.status_code == 422


def test_register_invalid_name_fails(client):
    """Verify registration fails when name contains invalid characters."""
    response = create_user(
        client=client,
        name="john1",
        last_name="doe",
        email="john_doe@example.com",
        password="Mypassword1234567",
    )

    assert response.status_code == 422


def test_register_invalid_last_name_fails(client):
    """Verify registration fails when last name coiants invalid characters."""
    response = create_user(
        client=client,
        name="john",
        last_name="doe1",
        email="john_doe@example.com",
        password="Mypassword1234567",
    )

    assert response.status_code == 422


def test_login_unknown_email_fails(client):
    """Verify login fails for an email that has not been registered."""
    response = login_user(
        client=client,
        email="unknown@example.com",
        password="Mypassword1234567",
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"
