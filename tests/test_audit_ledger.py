from consequence_twin.audit_ledger import append_event, tamper_detected_event, verify_chain


def build_chain():
    chain = []
    first = append_event(
        chain,
        event_type="movement submitted",
        tenant_id="tenant-a",
        actor_id="operator-1",
        payload={"movement_id": "MOVE-1"},
    ).to_dict()
    chain.append(first)
    second = append_event(
        chain,
        event_type="verdict issued",
        tenant_id="tenant-a",
        actor_id="reviewer-1",
        payload={"verdict": "ADMIT"},
    ).to_dict()
    chain.append(second)
    third = append_event(
        chain,
        event_type="receipt signed",
        tenant_id="tenant-a",
        actor_id="runtime",
        payload={"receipt_id": "RCT-1"},
    ).to_dict()
    chain.append(third)
    return chain


def test_valid_chain_verifies():
    chain = build_chain()
    result = verify_chain(chain)
    assert result["valid"] is True
    assert result["event_count"] == 3


def test_deleting_event_breaks_chain():
    chain = build_chain()
    broken = [chain[0], chain[2]]
    result = verify_chain(broken)
    assert result["valid"] is False
    assert result["reason"] == "previous_hash mismatch"


def test_editing_event_breaks_chain():
    chain = build_chain()
    chain[1] = dict(chain[1], event_type="edited event")
    result = verify_chain(chain)
    assert result["valid"] is False
    assert result["reason"] == "event_hash mismatch"


def test_reordering_event_breaks_chain():
    chain = build_chain()
    reordered = [chain[1], chain[0], chain[2]]
    result = verify_chain(reordered)
    assert result["valid"] is False


def test_missing_previous_hash_fails_verification():
    chain = build_chain()
    del chain[1]["previous_hash"]
    result = verify_chain(chain)
    assert result["valid"] is False


def test_tamper_detection_event_can_be_emitted():
    chain = build_chain()
    chain[1] = dict(chain[1], event_type="edited event")
    verification = verify_chain(chain)
    event = tamper_detected_event(
        chain,
        tenant_id="tenant-a",
        actor_id="auditor-1",
        verification_result=verification,
    )
    assert event.event_type == "tamper detected"
    assert event.previous_hash == chain[-1]["event_hash"]
