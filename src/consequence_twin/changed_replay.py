from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from .receipt_runtime import create_receipt, sha256_json, verify_receipt


class ChangedReplayError(ValueError):
    """Raised when changed-condition replay violates receipt integrity."""


@dataclass(frozen=True)
class ChangedConditionReplay:
    replay_type: str
    original_receipt_id: str
    original_input_hash: str
    original_verdict: str
    changed_input_hash: str
    changed_verdict: str
    changed_fields: List[str]
    reason_for_difference: List[str]
    new_receipt: Dict[str, Any]
    old_receipt_preserved: bool
    timestamp_utc: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def changed_fields(original: Dict[str, Any], changed: Dict[str, Any]) -> List[str]:
    keys = sorted(set(original) | set(changed))
    return [key for key in keys if original.get(key) != changed.get(key)]


def same_condition_replay(original_receipt: Dict[str, Any]) -> Dict[str, Any]:
    verification = verify_receipt(original_receipt)
    return {
        "replay_type": "same_condition_replay",
        "receipt_id": original_receipt["receipt_id"],
        "same_conditions": True,
        "verification": verification,
    }


def changed_condition_replay(
    *,
    original_receipt: Dict[str, Any],
    changed_input: Dict[str, Any],
) -> ChangedConditionReplay:
    original_input = dict(original_receipt.get("original_input", {}))
    changed = dict(changed_input)
    changed["prior_receipt_id"] = original_receipt["receipt_id"]
    changed["changed_condition_replay"] = True

    fields = changed_fields(original_input, changed_input)
    if not fields:
        raise ChangedReplayError("changed-condition replay requires a material change")

    new_receipt = create_receipt(changed).to_dict()
    new_receipt["prior_receipt_id"] = original_receipt["receipt_id"]
    new_receipt["changed_condition_replay"] = True

    reasons = [f"changed field: {field}" for field in fields]
    if original_receipt.get("verdict") != new_receipt.get("verdict"):
        reasons.append(
            f"verdict changed from {original_receipt.get('verdict')} to {new_receipt.get('verdict')}"
        )

    return ChangedConditionReplay(
        replay_type="changed_condition_replay",
        original_receipt_id=original_receipt["receipt_id"],
        original_input_hash=original_receipt["input_hash"],
        original_verdict=original_receipt["verdict"],
        changed_input_hash=sha256_json(changed_input),
        changed_verdict=new_receipt["verdict"],
        changed_fields=fields,
        reason_for_difference=reasons,
        new_receipt=new_receipt,
        old_receipt_preserved=True,
        timestamp_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )
