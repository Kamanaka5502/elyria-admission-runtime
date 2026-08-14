from consequence_twin.harmonics import resolve_harmonics


def valid_inputs():
    return {
        "intent": {"scope": "sandbox", "action": "deploy"},
        "evidence_items": [
            {
                "evidence_id": "E1",
                "required": True,
                "status": "accepted",
                "source_system": "test",
                "custody_owner": "owner",
                "hash_reference": "sha256:e1",
                "signature": "sig:e1",
            }
        ],
        "authority": {
            "participants": ["A", "B"],
            "threshold": 2,
            "nullifiers": ["N1", "N2"],
        },
        "context": {
            "required_intent_fields": ["scope", "action"],
            "allowed_scopes": ["sandbox"],
            "standing_active": True,
            "continuity_valid": True,
            "state_current": True,
            "rollback_available": True,
        },
        "before_state_hash": "before",
        "delta_hash": "delta",
        "evaluation_time": "2026-08-14T15:00:00Z",
    }


def test_harmonics_are_deterministic():
    kwargs = valid_inputs()
    first = resolve_harmonics(**kwargs).to_dict()
    second = resolve_harmonics(**kwargs).to_dict()
    assert first == second
    assert first["alignment_score"] == 1.0
    assert first["conflicts"] == []


def test_inconsistent_evidence_fails_closed():
    kwargs = valid_inputs()
    kwargs["evidence_items"] = [
        {
            "evidence_id": "E1",
            "status": "accepted",
            "custody_owner": "owner",
            "hash_reference": "sha256:e1",
            "signature": "sig:e1",
            "claim": "alpha",
        },
        {
            "evidence_id": "E2",
            "status": "accepted",
            "custody_owner": "owner",
            "hash_reference": "sha256:e2",
            "signature": "sig:e2",
            "claim": "beta",
        },
    ]
    result = resolve_harmonics(**kwargs)
    assert result.alignment_score == 0.0
    assert "inconsistent_evidence:claim" in result.conflicts


def test_expired_authority_fails_closed():
    kwargs = valid_inputs()
    kwargs["authority"] = {
        "participants": ["A", "B"],
        "threshold": 2,
        "nullifiers": ["N1", "N2"],
        "expiry": "2026-08-14T14:59:00Z",
    }
    result = resolve_harmonics(**kwargs)
    assert result.alignment_score == 0.0
    assert "authority_expired" in result.conflicts


def test_consumed_authority_fails_closed():
    kwargs = valid_inputs()
    kwargs["authority"] = {
        "participants": ["A", "B"],
        "threshold": 2,
        "nullifiers": ["N1", "N2"],
        "consumed": True,
    }
    result = resolve_harmonics(**kwargs)
    assert result.alignment_score == 0.0
    assert "authority_already_consumed" in result.conflicts
