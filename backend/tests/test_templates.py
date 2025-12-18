from __future__ import annotations


def test_template_crud_and_send_test(client, auth_headers, monkeypatch):
    sent = {}

    def fake_send_html_email(*, to_email: str, subject: str, html: str) -> None:
        sent["to"] = to_email
        sent["subject"] = subject
        sent["html"] = html

    monkeypatch.setattr("email_marketing_backend.api.templates.send_html_email", fake_send_html_email)

    create = client.post(
        "/api/templates",
        json={"name": "Welcome", "subject": "Hello", "html": "<h1>Hi</h1>", "css": "h1{color:red;}"},
        headers=auth_headers,
    )
    assert create.status_code == 201
    template = create.get_json()["data"]
    assert template["name"] == "Welcome"

    list_resp = client.get("/api/templates", headers=auth_headers)
    assert list_resp.status_code == 200
    items = list_resp.get_json()["data"]
    assert any(item["id"] == template["id"] for item in items)

    update = client.put(
        f"/api/templates/{template['id']}",
        json={"subject": "Updated subject"},
        headers=auth_headers,
    )
    assert update.status_code == 200
    assert update.get_json()["data"]["subject"] == "Updated subject"

    send_test = client.post(
        f"/api/templates/{template['id']}/send-test",
        json={"to": "test@example.com"},
        headers=auth_headers,
    )
    assert send_test.status_code == 200
    assert sent["to"] == "test@example.com"
    assert "Updated subject" in sent["subject"]

