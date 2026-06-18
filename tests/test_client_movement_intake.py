from fastapi.testclient import TestClient

from apps.api.main import app


CUSTOM_BLACK_PATH = {
    "movement_id": "CLIENT-BLACK-001",
    "source_node": "client.evidence.check",
    "target_node": "client.payment.release",
    "authority_present": True,
    "authority_scope_valid": True,
    "standing_active": True,
    "evidence_present": False,
    "evidence_sufficient": False,
    "custody_preserved": False,
    "refusal_condition_active": False,
    "revalidation_required": False,
    "receipt_available": False,
    "replay_available": False,
    "notes": "Client-entered black path.",
}


def test_client_movement_intake_emits_signed_receipt_and_updates_current_graph(monkeypatch, tmp_path):
    monkeypatch.setenv("ELYRIA_MODE", "demo")
    monkeypatch.setenv("ELYRIA_DB_PATH", str(tmp_path / "intake.db"))
    client = TestClient(app)

    receipt_response = client.post("/movements/assess", json=CUSTOM_BLACK_PATH)
    assert receipt_response.status_code == 200
    receipt = receipt_response.json()
    assert receipt["movement_id"] == "CLIENT-BLACK-001"
    assert receipt["verdict"] == "NO_PROVABLE_ADMISSION"
    assert receipt["signature_algorithm"] == "HMAC-SHA256"
    assert receipt["signature"]

    graph_response = client.get("/exposures/current")
    assert graph_response.status_code == 200
    graph = graph_response.json()
    assert graph["graph_id"] == "CURRENT-GRAPH"
    assert graph["summary"]["black_paths"] == 1
    assert graph["edges"][0]["id"] == "CLIENT-BLACK-001"
