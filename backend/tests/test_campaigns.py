from __future__ import annotations

from types import SimpleNamespace


def test_campaign_send_to_all_contacts(client, auth_headers, monkeypatch):
    me = client.get("/api/auth/me", headers=auth_headers).get_json()
    org_id = me["user"]["organization_id"]

    client.post(
        f"/api/organizations/{org_id}/contacts",
        json={"email": "one@example.com", "first_name": "One"},
        headers=auth_headers,
    )
    client.post(
        f"/api/organizations/{org_id}/contacts",
        json={"email": "two@example.com", "first_name": "Two"},
        headers=auth_headers,
    )

    sent = []

    def fake_send_html_email(*, to_email: str, subject: str, html: str) -> None:
        sent.append({"to": to_email, "subject": subject, "html": html})

    monkeypatch.setattr("email_marketing_backend.tasks.campaigns.send_html_email", fake_send_html_email)

    template = client.post(
        "/api/templates",
        json={"name": "Welcome", "subject": "Hello", "html": "<h1>Hi</h1>"},
        headers=auth_headers,
    ).get_json()["data"]

    campaign = client.post(
        "/api/campaigns",
        json={"name": "Launch", "template_id": template["id"], "audience_type": "all_contacts"},
        headers=auth_headers,
    )
    assert campaign.status_code == 201
    campaign_id = campaign.get_json()["data"]["id"]

    from email_marketing_backend.tasks.campaigns import send_campaign

    def eager_delay(campaign_id_arg: int):
        send_campaign(campaign_id_arg)
        return SimpleNamespace(id="eager-task")

    monkeypatch.setattr("email_marketing_backend.api.campaigns.send_campaign_task.delay", eager_delay)

    queued = client.post(f"/api/campaigns/{campaign_id}/send", headers=auth_headers)
    assert queued.status_code == 202
    assert len(sent) == 2

    sends = client.get(f"/api/campaigns/{campaign_id}/sends", headers=auth_headers)
    assert sends.status_code == 200
    assert len(sends.get_json()["data"]) == 2
