from __future__ import annotations

import os

os.environ.setdefault("API_KEYS", "test-key")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest
from flask import Flask

from email_marketing_backend import create_app
from email_marketing_backend.extensions import db


@pytest.fixture()
def app() -> Flask:
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "admin@admin.com",
            "password": "secret",
            "organization": "test-org",
        },
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@admin.com", "password": "secret"},
    )
    data = response.get_json()
    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def internal_headers():
    return {"X-API-Key": "test-key"}
