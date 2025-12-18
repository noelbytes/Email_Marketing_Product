from __future__ import annotations


def test_health_endpoint(client):
    response = client.get("/api/healthz")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["service"] == "email-marketing-api"
