import pytest

from consequence_twin.changed_replay import (
    ChangedReplayError,
    changed_condition_replay,
    same_condition_replay,
)
from consequence_twin.receipt_runtime import create_receipt


def base_payload(**overrides):
    payload = {
        "movement_id": "MOVE-001",
        "authority_present": True,
        "authority_scope_valid": True,
        "standing_active": True,
        "evidence_present": False,
        "evidence_sufficient": False,
        "custody_preserved": True,
        "refusal_condition_active": False,
        "revalidation_required": False,
        "receipt_available": True,
        "replay_available": True,
    }
    payload.update(overrides)
    return payload


def test_same_condition_replay_verifies_original_receipt():
    receipt = create_receipt(base_payload()).to_dict()
    replay = same_condition_replay(receipt)
    assert replay["same_conditions"] is True
    assert replay["verification"]["input_hash_matches"] is True
    assert replay["verification"]["verdict_matches"] is True


def test_changed_conditions_create_new_linked_receipt_not_mutation():
    original = create_receipt(base_payload()).to_dict()
    changed = base_payload(evidence_present=True, evidence_sufficient=True)
    replay = changed_condition_replay(original_receipt=original, changed_input=changed).to_dict()
    assert replay["old_receipt_preserved"] is True
    assert replay["original_receipt_id"] == original["receipt_id"]
    assert replay["new_receipt"]["receipt_id"] != original["receipt_id"]
    assert replay["new_receipt"]["prior_receipt_id"] == original["receipt_id"]
    assert replay["new_receipt"]["changed_condition_replay"] is True


def test_changed_replay_explains_difference():
    original = create_receipt(base_payload()).to_dict()
    changed = base_payload(evidence_present=True, evidence_sufficient=True)
    replay = changed_condition_replay(original_receipt=original, changed_input=changed).to_dict()
    assert "evidence_present" in replay["changed_fields"]
    assert "evidence_sufficient" in replay["changed_fields"]
    assert replay["reason_for_difference"]


def test_changed_condition_replay_requires_material_change():
    original_input = base_payload()
    original = create_receipt(original_input).to_dict()
    with pytest.raises(ChangedReplayError):
        changed_condition_replay(original_receipt=original, changed_input=original_input)
