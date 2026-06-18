import pytest

from consequence_twin import assess_movement, Verdict


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
    }
    payload.update(overrides)
    return payload


def test_admit_when_all_dimensions_hold():
    result = assess_movement(base_payload())
    assert result.verdict == Verdict.ADMIT
    assert result.color == "green"


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
