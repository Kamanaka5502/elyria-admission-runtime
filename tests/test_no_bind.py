import pytest

from consequence_twin.no_bind import NoBindError, create_no_bind_proof, validate_no_bind_proof


def movement(**overrides):
    payload = {
        "movement_id": "MOVE-001",
        "authority_present": False,
        "authority_scope_valid": False,
        "standing_active": True,
    }
    payload.update(overrides)
    return payload


def test_non_admitted_movement_emits_no_bind_proof():
    proof = create_no_bind_proof(
        movement=movement(),
        admission_result={"verdict": "REFUSE", "reasons": ["admission failed"]},
        receipt_reference="RCT-001",
        replay_reference="REPLAY-001",
    ).to_dict()
    assert proof["proof_type"] == "elyria_no_bind_proof"
    assert proof["route_closure_state"] == "closed"
    assert proof["downstream_effect_status"] == "not_activated"
    assert validate_no_bind_proof(proof)["valid"] is True


def test_no_bind_proof_records_standing_condition():
    proof = create_no_bind_proof(
        movement=movement(standing_active=False),
        admission_result={"verdict": "REFUSE", "reasons": ["standing inactive"]},
    ).to_dict()
    assert proof["missing_or_invalid_standing_condition"] == "standing inactive or expired"


def test_admitted_movement_cannot_emit_no_bind_proof():
    with pytest.raises(NoBindError):
        create_no_bind_proof(
            movement=movement(authority_present=True, authority_scope_valid=True),
            admission_result={"verdict": "ADMIT", "reasons": ["complete"]},
        )


def test_invalid_no_bind_proof_fails_validation():
    proof = create_no_bind_proof(
        movement=movement(),
        admission_result={"verdict": "REFUSE", "reasons": ["admission failed"]},
    ).to_dict()
    proof["downstream_effect_status"] = "activated"
    assert validate_no_bind_proof(proof)["valid"] is False
