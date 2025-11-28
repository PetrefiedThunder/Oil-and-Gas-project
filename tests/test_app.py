from fastapi.testclient import TestClient

from mlpe.app import app


client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ingest_scada():
    """Test SCADA ingestion endpoint."""
    payload = {
        "leak_id": "test-leak-1",
        "location": {
            "latitude": 29.7604,
            "longitude": -95.3698,
            "geohash": "9vk8p"
        },
        "detections": [
            {
                "source_type": "scada",
                "confidence": 0.85,
                "observed_at": "2024-01-15T10:30:00Z",
                "metadata": {}
            }
        ]
    }
    response = client.post("/ingest/scada", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["leak_id"] == "test-leak-1"


def test_ranked_leaks():
    """Test ranked leaks endpoint."""
    response = client.get("/leaks/ranked")
    assert response.status_code == 200
    data = response.json()
    assert "leaks" in data
    assert "generated_at" in data
