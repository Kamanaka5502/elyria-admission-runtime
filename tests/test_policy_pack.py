from consequence_twin.policy_pack import evaluate_policy_pack, policy_pack_hash


POLICY_PACK = {
    "policy_pack_id": "basic_customer_corridor",
    "version": "1.0.0",
    "allowed_movement_types": ["governed_release", "proof_export"],
    "allowed_authority_scopes": ["customer_admin", "runtime_reviewer"],
    "required_evidence": ["authority_record", "standing_record", "custody_hash"],
    "custody_required": True,
    "refusal_rules": {"blocking_codes": ["blocked_code"]},
}


def movement(**overrides):
    payload = {
        "movement_id": "MOVE-001",
        "movement_type": "governed_release",
        "authority_present": True,
        "authority_scope": "customer_admin",
        "custody_preserved": True,
        "active_refusal_codes": [],
        "evidence_items": [
            {"type": "authority_record", "status": "accepted"},
            {"type": "standing_record", "status": "accepted"},
            {"type": "custody_hash", "status": "accepted"},
        ],
    }
    payload.update(overrides)
    return payload


def test_policy_pack_admits_valid_movement():
    result = evaluate_policy_pack(movement(), POLICY_PACK)
    assert result.verdict == "ADMIT"
    assert result.policy_pack_hash == policy_pack_hash(POLICY_PACK)


def test_missing_required_evidence_fails():
    result = evaluate_policy_pack(
        movement(evidence_items=[{"type": "authority_record", "status": "accepted"}]),
        POLICY_PACK,
    )
    assert result.verdict == "REFUSE"
    assert any("required policy evidence missing" in reason for reason in result.reasons)


def test_invalid_authority_scope_fails():
    result = evaluate_policy_pack(movement(authority_scope="outside_scope"), POLICY_PACK)
    assert result.verdict == "REFUSE"
    assert any("authority scope invalid" in reason for reason in result.reasons)


def test_out_of_scope_movement_fails():
    result = evaluate_policy_pack(movement(movement_type="unapproved_move"), POLICY_PACK)
    assert result.verdict == "REFUSE"
    assert any("out of policy scope" in reason for reason in result.reasons)


def test_blocking_code_overrides_admission():
    result = evaluate_policy_pack(
        movement(active_refusal_codes=["blocked_code"]),
        POLICY_PACK,
    )
    assert result.verdict == "REFUSE"
    assert any("overrides admission" in reason for reason in result.reasons)


def test_policy_pack_hash_appears_in_decision_record():
    result = evaluate_policy_pack(movement(), POLICY_PACK).to_dict()
    assert result["policy_pack_hash"] == policy_pack_hash(POLICY_PACK)
