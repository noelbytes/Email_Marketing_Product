from __future__ import annotations


def register_user(client, email="user@example.com", password="pw", organization="alpha"):
    return client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "organization": organization},
    )


def test_register_and_login_flow(client):
    register = register_user(client, "admin@admin.com", "secret", "alpha")
    assert register.status_code == 201

    resp = client.post(
        "/api/auth/login",
        json={"email": "admin@admin.com", "password": "secret"},
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body
    assert "org-admin" in body["roles"]


def test_me_endpoint_requires_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401

    register_user(client, "user@example.com", "pw")
    login = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "pw"},
    )
    token = login.get_json()["access_token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    payload = me.get_json()
    assert payload["user"]["email"] == "user@example.com"
