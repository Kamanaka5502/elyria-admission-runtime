from __future__ import annotations

import hashlib
import hmac
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from .engine import assess_movement
from .evidence import summarize_evidence
from .settings import get_settings

ENGINE_VERSION = "0.3.0"
SIGNATURE_ALGORITHM = "HMAC-SHA256"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sign_payload(value: Dict[str, Any], secret: str | None = None) -> str:
    signing_secret = secret or get_settings().receipt_signing_secret
    return hmac.new(
        signing_secret.encode("utf-8"),
        canonical_json(value).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


@dataclass(frozen=True)
class ReceiptRecord:
    receipt_id: str
    movement_id: str
    verdict: str
    color: str
    reasons: List[str]
    timestamp_utc: str
    input_hash: str
    engine_version: str
    original_input: Dict[str, Any]
    evidence_summary: Dict[str, Any]
    signature_algorithm: str
    signature: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def receipt_signing_material(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "receipt_id": record["receipt_id"],
        "movement_id": record["movement_id"],
        "verdict": record["verdict"],
        "color": record["color"],
        "reasons": record["reasons"],
        "timestamp_utc": record["timestamp_utc"],
        "input_hash": record["input_hash"],
        "engine_version": record["engine_version"],
        "original_input": record["original_input"],
        "evidence_summary": record.get("evidence_summary", summarize_evidence(record["original_input"])),
    }


def create_receipt(payload: Dict[str, Any]) -> ReceiptRecord:
    result = assess_movement(payload)
    evidence_summary = summarize_evidence(payload)
    unsigned = {
        "receipt_id": f"RCT-{uuid.uuid4().hex[:16].upper()}",
        "movement_id": result.movement_id,
        "verdict": result.verdict.value,
        "color": result.color,
        "reasons": result.reasons,
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "input_hash": sha256_json(payload),
        "engine_version": ENGINE_VERSION,
        "original_input": dict(payload),
        "evidence_summary": evidence_summary,
    }
    return ReceiptRecord(
        **unsigned,
        signature_algorithm=SIGNATURE_ALGORITHM,
        signature=sign_payload(unsigned),
    )


def verify_receipt(record: Dict[str, Any]) -> Dict[str, Any]:
    payload = record["original_input"]
    result = assess_movement(payload).to_dict()
    verdict_matches = (
        result["movement_id"] == record["movement_id"]
        and result["verdict"] == record["verdict"]
        and result["color"] == record["color"]
        and result["reasons"] == record["reasons"]
    )
    expected_signature = sign_payload(receipt_signing_material(record))
    signature_matches = hmac.compare_digest(record.get("signature", ""), expected_signature)
    evidence_summary_matches = record.get("evidence_summary") == summarize_evidence(payload)
    return {
        "receipt_id": record["receipt_id"],
        "input_hash_matches": sha256_json(payload) == record["input_hash"],
        "verdict_matches": verdict_matches,
        "signature_matches": signature_matches,
        "signature_algorithm": record.get("signature_algorithm"),
        "evidence_summary_matches": evidence_summary_matches,
        "actual": result,
    }
