def test_stats_empty(client):
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total_tests"] == 0
    assert data["total_pass"] == 0
    assert data["total_fail"] == 0
    assert data["total_pending"] == 0
    assert data["success_rate"] == 0.0
    assert data["total_templates"] == 0


def test_stats_with_templates(client, sample_template_data):
    client.post("/api/templates", json=sample_template_data)
    resp = client.get("/api/stats")
    data = resp.json()["data"]
    assert data["total_templates"] == 1
