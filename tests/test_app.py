from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_mock_ingestion_flow():
    response = client.post("/api/ingest")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ingested"
    assert payload["record_count"] >= 1
