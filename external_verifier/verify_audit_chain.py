from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


class VerificationError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def event_material(event: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "event_id",
        "event_type",
        "tenant_id",
        "actor_id",
        "timestamp_utc",
        "payload_hash",
        "previous_hash",
    ]
    missing = [field for field in required if field not in event]
    if missing:
        raise VerificationError(f"audit event missing fields: {', '.join(missing)}")
    return {field: event[field] for field in required}


def compute_event_hash(event: Dict[str, Any]) -> str:
    return sha256_json(event_material(event))


def verify_audit_chain(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    event_list: List[Dict[str, Any]] = list(events)
    previous_hash = "GENESIS"
    for index, event in enumerate(event_list):
        if event.get("previous_hash") != previous_hash:
            raise VerificationError(f"audit previous_hash mismatch at index {index}")
        expected = compute_event_hash(event)
        if event.get("event_hash") != expected:
            raise VerificationError(f"audit event_hash mismatch at index {index}")
        previous_hash = event["event_hash"]
    return {"valid": True, "event_count": len(event_list), "tip_hash": previous_hash}


def verify_audit_chain_file(path: str | Path) -> Dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return verify_audit_chain(payload.get("events", []))


if __name__ == "__main__":
    import sys

    result = verify_audit_chain_file(sys.argv[1])
    print(json.dumps(result, indent=2, sort_keys=True))
