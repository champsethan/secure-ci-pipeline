import pytest
from app import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(main, "DB_PATH", str(test_db))
    main.init_db()
    main.app.config["TESTING"] = True
    with main.app.test_client() as client:
        yield client


def test_existing_user_returns_200(client):
    response = client.get("/users/john_doe")
    assert response.status_code == 200
    assert response.get_json()["email"] == "john@example.com"


def test_missing_user_returns_404(client):
    response = client.get("/users/nobody")
    assert response.status_code == 404


def test_invalid_characters_return_400(client):
    response = client.get("/users/bad!name")
    assert response.status_code == 400


@pytest.mark.parametrize("payload", [
    "' OR 1=1 --",
    "john_doe' --",
    "x' UNION SELECT id, username, email FROM users --",
    "admin'; DROP TABLE users; --",
])
def test_sql_injection_is_blocked(client, payload):
    response = client.get(f"/users/{payload}")
    assert response.status_code in (400, 404)
    assert b"@example.com" not in response.data