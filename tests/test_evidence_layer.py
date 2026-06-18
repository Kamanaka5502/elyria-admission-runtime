from fastapi.testclient import TestClient

from apps.api.main import app
from consequence_twin.evidence import summarize_evidence
from consequence_twin.receipt_runtime import create_receipt, verify_receipt


PAYLOAD_WITH_EVIDENCE = {
    "movement_id": "CLIENT-EVIDENCE-001",
    "source_node": "client.workflow",
    "target_node": "protected.action",
    "authority_present": True,
    "authority_scope_valid": True,
    "standing_active": True,
    "evidence_present": True,
    "evidence_sufficient": True,
    "custody_preserved": True,
    "refusal_condition_active": False,
    "revalidation_required": False,
    "receipt_available": True,
    "replay_available": True,
    "notes": "Client movement with attached evidence reference.",
    "evidence_items": [
        {
            "evidence_id": "EV-001",
            "evidence_type": "policy_record",
            "source_system": "client.governance.registry",
            "custody_owner": "operations.owner",
            "hash_reference": "sha256:demo-reference",
            "required": True,
            "status": "accepted",
            "notes": "Required evidence reference.",
        }
    ],
}


def test_evidence_summary_marks_supporting_evidence():
    summary = summarize_evidence(PAYLOAD_WITH_EVIDENCE)
    assert summary["status"] == "supporting"
    assert summary["required"] == 1
    assert summary["accepted"] == 1
    assert summary["missing"] == 0
    assert summary["custody_gaps"] == 0
    assert summary["hash_references"] == 1


def test_signed_receipt_includes_evidence_summary_and_replay_verifies_it():
    receipt = create_receipt(PAYLOAD_WITH_EVIDENCE).to_dict()
    assert receipt["engine_version"] == "0.3.0"
    assert receipt["evidence_summary"]["status"] == "supporting"
    check = verify_receipt(receipt)
    assert check["signature_matches"] is True
    assert check["evidence_summary_matches"] is True


def test_api_accepts_evidence_items_in_movement_intake(monkeypatch, tmp_path):
    monkeypatch.setenv("ELYRIA_MODE", "demo")
    monkeypatch.setenv("ELYRIA_DB_PATH", str(tmp_path / "evidence.db"))
    client = TestClient(app)
    response = client.post("/movements/assess", json=PAYLOAD_WITH_EVIDENCE)
    assert response.status_code == 200
    receipt = response.json()
    assert receipt["evidence_summary"]["status"] == "supporting"
    assert receipt["original_input"]["evidence_items"][0]["evidence_id"] == "EV-001"
