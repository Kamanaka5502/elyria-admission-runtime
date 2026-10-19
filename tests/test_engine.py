import pytest

from consequence_twin import assess_movement, Verdict


def accepted_evidence():
    return [
        {
            "evidence_id": "EVID-001",
            "required": True,
            "status": "accepted",
            "source_system": "test-fixture",
            "custody_owner": "test-owner",
            "hash_reference": "sha256:fixture-placeholder",
        }
    ]


def base_payload(**overrides):
    payload = {
        "movement_id": "MOVE-001",
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
        "evidence_items": accepted_evidence(),
    }
    payload.update(overrides)
    return payload


def test_admit_when_configured_dimensions_and_structured_evidence_present():
    result = assess_movement(base_payload())
    assert result.verdict == Verdict.ADMIT
    assert result.color == "green"


def test_no_provable_admission_when_structured_evidence_is_empty():
    result = assess_movement(base_payload(evidence_items=[]))
    assert result.verdict == Verdict.NO_PROVABLE_ADMISSION
    assert result.color == "black"
    assert any("no structured evidence attachments" in reason for reason in result.reasons)


def test_caller_boolean_cannot_replace_empty_evidence_collection():
    payload = base_payload(evidence_items=[])
    payload["evidence_present"] = True
    payload["evidence_sufficient"] = True
    result = assess_movement(payload)
    assert result.verdict != Verdict.ADMIT


def test_refuse_when_authority_absent():
    result = assess_movement(base_payload(authority_present=False))
    assert result.verdict == Verdict.REFUSE
    assert result.color == "red"
    assert "authority absent" in result.reasons


def test_hold_or_black_when_evidence_missing_before_bind():
    result = assess_movement(base_payload(evidence_present=False))
    assert result.verdict == Verdict.NO_PROVABLE_ADMISSION
    assert result.color == "black"
    assert any("evidence" in reason for reason in result.reasons)


def test_black_when_receipt_or_replay_missing():
    result = assess_movement(base_payload(receipt_available=False, replay_available=False))
    assert result.verdict == Verdict.NO_PROVABLE_ADMISSION
    assert result.color == "black"


def test_refuse_overrides_hold():
    result = assess_movement(base_payload(refusal_condition_active=True, evidence_present=False))
    assert result.verdict == Verdict.REFUSE
    assert result.color == "red"


def test_missing_boolean_field_rejected():
    payload = base_payload()
    del payload["standing_active"]
    with pytest.raises(ValueError):
        assess_movement(payload)
