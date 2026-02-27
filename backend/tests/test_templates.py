def test_list_templates_empty(client):
    resp = client.get("/api/templates")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"] == []


def test_create_template(client, sample_template_data):
    resp = client.post("/api/templates", json=sample_template_data)
    assert resp.status_code == 201
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["name"] == sample_template_data["name"]
    assert body["data"]["category"] == "prompt_injection"
    assert body["data"]["language"] == "en"
    assert "id" in body["data"]


def test_get_template(client, sample_template_data):
    create_resp = client.post("/api/templates", json=sample_template_data)
    template_id = create_resp.json()["data"]["id"]

    resp = client.get(f"/api/templates/{template_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == sample_template_data["name"]


def test_get_template_not_found(client):
    resp = client.get("/api/templates/nonexistent-id")
    assert resp.status_code == 404


def test_update_template(client, sample_template_data):
    create_resp = client.post("/api/templates", json=sample_template_data)
    template_id = create_resp.json()["data"]["id"]

    resp = client.put(
        f"/api/templates/{template_id}",
        json={"name": "Updated Name", "severity": "critical"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["name"] == "Updated Name"
    assert data["severity"] == "critical"
    assert data["category"] == "prompt_injection"  # unchanged


def test_delete_template(client, sample_template_data):
    create_resp = client.post("/api/templates", json=sample_template_data)
    template_id = create_resp.json()["data"]["id"]

    resp = client.delete(f"/api/templates/{template_id}")
    assert resp.status_code == 200
    assert resp.json()["success"] is True

    resp = client.get(f"/api/templates/{template_id}")
    assert resp.status_code == 404


def test_filter_by_category(client, sample_template_data):
    client.post("/api/templates", json=sample_template_data)
    client.post(
        "/api/templates",
        json={**sample_template_data, "name": "Bias Test", "category": "bias"},
    )

    resp = client.get("/api/templates?category=bias")
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["category"] == "bias"


def test_filter_by_language(client, sample_template_data):
    client.post("/api/templates", json=sample_template_data)
    client.post(
        "/api/templates",
        json={**sample_template_data, "name": "ZH Test", "language": "zh"},
    )

    resp = client.get("/api/templates?language=zh")
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["language"] == "zh"


def test_search_templates(client, sample_template_data):
    client.post("/api/templates", json=sample_template_data)
    client.post(
        "/api/templates",
        json={**sample_template_data, "name": "Jailbreak DAN"},
    )

    resp = client.get("/api/templates?q=DAN")
    data = resp.json()["data"]
    assert len(data) == 1
    assert "DAN" in data[0]["name"]
