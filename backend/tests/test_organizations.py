from __future__ import annotations

from flask.testing import FlaskClient
from email_marketing_backend.extensions import db
from email_marketing_backend.db.models import Organization, Contact


def test_unauthorized_without_token(client: FlaskClient):
    response = client.get("/api/organizations")
    assert response.status_code == 401


def test_create_and_list_organization(client: FlaskClient, internal_headers):
    response = client.post(
        "/api/organizations",
        json={"name": "Acme Corp", "slug": "acme"},
        headers=internal_headers,
    )
    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["name"] == "Acme Corp"

    list_response = client.get("/api/organizations", headers=internal_headers)
    assert list_response.status_code == 200
    items = list_response.get_json()["data"]
    assert any(item["slug"] == "acme" for item in items)


def test_create_contact_for_org(client: FlaskClient, auth_headers):
    me = client.get("/api/auth/me", headers=auth_headers).get_json()
    org_id = me["user"]["organization_id"]

    create_response = client.post(
        f"/api/organizations/{org_id}/contacts",
        json={"email": "user@example.com", "first_name": "Nova"},
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    contact_payload = create_response.get_json()["data"]
    assert contact_payload["email"] == "user@example.com"

    list_response = client.get(f"/api/organizations/{org_id}/contacts", headers=auth_headers)
    assert list_response.status_code == 200
    contacts = list_response.get_json()["data"]
    assert len(contacts) == 1
    assert contacts[0]["first_name"] == "Nova"


def test_duplicate_contact_returns_conflict(client: FlaskClient, auth_headers):
    me = client.get("/api/auth/me", headers=auth_headers).get_json()
    org_id = me["user"]["organization_id"]

    contact = Contact(email="dup@example.com", organization_id=org_id)
    db.session.add(contact)
    db.session.commit()

    response = client.post(
        f"/api/organizations/{org_id}/contacts",
        json={"email": "dup@example.com"},
        headers=auth_headers,
    )
    assert response.status_code == 409
