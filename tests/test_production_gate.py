from fastapi.testclient import TestClient

from apps.api.main import app
from consequence_twin.demo_data import DEMO_ASSESSMENTS
from consequence_twin.receipt_runtime import create_receipt, verify_receipt


def test_signed_receipt_verifies_signature():
    receipt = create_receipt(DEMO_ASSESSMENTS[0]).to_dict()
    check = verify_receipt(receipt)
    assert check["input_hash_matches"] is True
    assert check["verdict_matches"] is True
    assert check["signature_matches"] is True
    assert check["signature_algorithm"] == "HMAC-SHA256"


def test_client_mode_requires_auth(monkeypatch, tmp_path):
    monkeypatch.setenv("ELYRIA_MODE", "client")
    monkeypatch.setenv("ELYRIA_API_TOKEN", "test-token")
    monkeypatch.setenv("ELYRIA_DB_PATH", str(tmp_path / "client.db"))
    client = TestClient(app)
    response = client.get("/receipts")
    assert response.status_code == 401


def test_client_mode_protects_sandbox_reset(monkeypatch, tmp_path):
    monkeypatch.setenv("ELYRIA_MODE", "client")
    monkeypatch.setenv("ELYRIA_API_TOKEN", "test-token")
    monkeypatch.setenv("ELYRIA_DB_PATH", str(tmp_path / "client.db"))
    client = TestClient(app)
    response = client.post("/sandbox/reset")
    assert response.status_code == 401


def test_client_mode_accepts_bearer_token(monkeypatch, tmp_path):
    monkeypatch.setenv("ELYRIA_MODE", "client")
    monkeypatch.setenv("ELYRIA_API_TOKEN", "test-token")
    monkeypatch.setenv("ELYRIA_DB_PATH", str(tmp_path / "client.db"))
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-token"}
    reset = client.post("/sandbox/reset", headers=headers)
    assert reset.status_code == 200
    response = client.get("/receipts", headers=headers)
    assert response.status_code == 200
    assert "items" in response.json()


def test_demo_mode_remains_open(monkeypatch, tmp_path):
    monkeypatch.setenv("ELYRIA_MODE", "demo")
    monkeypatch.setenv("ELYRIA_DB_PATH", str(tmp_path / "demo.db"))
    client = TestClient(app)
    client.post("/sandbox/reset")
    response = client.get("/receipts")
    assert response.status_code == 200
