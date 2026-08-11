from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from consequence_twin.continuity_runtime import (
    GENESIS,
    IdentityRegistry,
    admit_continuation,
    build_continuity_record,
    verify_continuity_record,
)


def payload():
    return {
        "movement_id": "M-CONT-001",
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
        "evidence_items": [
            {
                "evidence_id": "E-1",
                "status": "accepted",
                "required": True,
                "custody_owner": "node-A",
                "hash_reference": "sha256:demo",
            }
        ],
    }


def test_pre_post_final_and_continuation():
    key_a = Ed25519PrivateKey.generate()
    key_b = Ed25519PrivateKey.generate()
    registry = IdentityRegistry()
    registry.register("A", key_a.public_key())
    registry.register("B", key_b.public_key())

    record = build_continuity_record(
        payload(),
        "A",
        key_a,
        registry,
        previous_final_seal=GENESIS,
        quorum_keys={"A": key_a, "B": key_b},
    )

    checks = verify_continuity_record(record.to_dict(), registry)
    assert checks["continuity_valid"] is True
    assert record.pre_seal
    assert record.post_seal
    assert record.final_seal

    continuation = admit_continuation(
        record.to_dict(),
        {**payload(), "movement_id": "M-CONT-002"},
        registry,
        "A",
        key_a,
    )
    assert continuation["status"] == "ADMITTED"
    assert continuation["predecessor_final_seal"] == record.final_seal


def test_tampered_post_state_is_rejected():
    key = Ed25519PrivateKey.generate()
    registry = IdentityRegistry()
    registry.register("A", key.public_key())
    record = build_continuity_record(payload(), "A", key, registry)

    tampered = record.to_dict()
    tampered["post_state"]["outcome"]["status"] = "ALTERED"
    checks = verify_continuity_record(tampered, registry)
    assert checks["post_valid"] is False
    assert checks["continuity_valid"] is False


def test_revoked_origin_cannot_continue():
    key = Ed25519PrivateKey.generate()
    registry = IdentityRegistry()
    registry.register("A", key.public_key())
    record = build_continuity_record(payload(), "A", key, registry)
    registry.revoke("A")

    checks = verify_continuity_record(record.to_dict(), registry)
    assert checks["continuity_valid"] is False
