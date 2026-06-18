from fastapi.testclient import TestClient

from apps.api.main import app


def test_demo_proof_endpoint_returns_graph_and_claim():
    client = TestClient(app)
    client.post("/sandbox/reset")
    response = client.get("/demo/proof")
    assert response.status_code == 200
    data = response.json()
    assert data["service"]["status"] == "ok"
    assert data["graph"]["summary"]["black_paths"] == 1
    assert "proof_claim" in data
    assert len(data["receipts"]) >= 3
