import pytest

from consequence_twin.receipt_runtime import create_receipt
from consequence_twin.receipt_store import (
    ReceiptStoreError,
    export_proof_packet,
    list_receipt_ids,
    read_receipt,
    verify_stored_receipt,
    write_once_receipt,
)


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


def test_receipt_can_be_written_once_and_retrieved(tmp_path):
    receipt = create_receipt(base_payload()).to_dict()
    stored = write_once_receipt(tmp_path, receipt)
    loaded = read_receipt(tmp_path, receipt["receipt_id"])
    assert stored.receipt_id == receipt["receipt_id"]
    assert loaded == receipt


def test_receipt_cannot_be_silently_overwritten(tmp_path):
    receipt = create_receipt(base_payload()).to_dict()
    write_once_receipt(tmp_path, receipt)
    with pytest.raises(ReceiptStoreError):
        write_once_receipt(tmp_path, receipt)


def test_receipt_can_be_verified_after_reload(tmp_path):
    receipt = create_receipt(base_payload()).to_dict()
    write_once_receipt(tmp_path, receipt)
    verification = verify_stored_receipt(tmp_path, receipt["receipt_id"])
    assert verification["input_hash_matches"] is True
    assert verification["verdict_matches"] is True
    assert verification["signature_matches"] is True


def test_receipt_can_be_exported_into_proof_packet(tmp_path):
    receipt = create_receipt(base_payload()).to_dict()
    write_once_receipt(tmp_path, receipt)
    packet = export_proof_packet(tmp_path, receipt["receipt_id"])
    assert packet["packet_type"] == "elyria_admission_runtime_receipt_proof_packet"
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["manifest"]["receipt.json"] == packet["receipt_hash"]


def test_receipt_ids_listed(tmp_path):
    first = create_receipt(base_payload(movement_id="MOVE-001")).to_dict()
    second = create_receipt(base_payload(movement_id="MOVE-002")).to_dict()
    write_once_receipt(tmp_path, first)
    write_once_receipt(tmp_path, second)
    assert list_receipt_ids(tmp_path) == sorted([first["receipt_id"], second["receipt_id"]])
