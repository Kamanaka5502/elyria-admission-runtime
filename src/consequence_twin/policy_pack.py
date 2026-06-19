from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, List


class PolicyPackError(ValueError):
    """Raised when a policy pack is invalid or cannot govern a movement."""


@dataclass(frozen=True)
class PolicyDecision:
    movement_id: str
    policy_pack_id: str
    policy_pack_hash: str
    verdict: str
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "movement_id": self.movement_id,
            "policy_pack_id": self.policy_pack_id,
            "policy_pack_hash": self.policy_pack_hash,
            "verdict": self.verdict,
            "reasons": list(self.reasons),
        }


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def policy_pack_hash(policy_pack: Dict[str, Any]) -> str:
    return sha256_json(policy_pack)


def require_policy_pack(policy_pack: Dict[str, Any]) -> None:
    required = [
        "policy_pack_id",
        "version",
        "allowed_movement_types",
        "allowed_authority_scopes",
        "required_evidence",
        "custody_required",
        "refusal_rules",
    ]
    missing = [field for field in required if field not in policy_pack]
    if missing:
        raise PolicyPackError(f"missing policy pack fields: {', '.join(missing)}")


def evidence_types(movement: Dict[str, Any]) -> set[str]:
    items = movement.get("evidence_items", []) or []
    return {str(item.get("type")) for item in items if item.get("status") == "accepted"}


def active_refusal_codes(movement: Dict[str, Any]) -> set[str]:
    return {str(code) for code in movement.get("active_refusal_codes", []) or []}


def evaluate_policy_pack(movement: Dict[str, Any], policy_pack: Dict[str, Any]) -> PolicyDecision:
    require_policy_pack(policy_pack)

    reasons: List[str] = []
    movement_id = str(movement.get("movement_id", "UNKNOWN"))
    pack_id = str(policy_pack["policy_pack_id"])
    pack_hash = policy_pack_hash(policy_pack)

    allowed_types = set(map(str, policy_pack.get("allowed_movement_types", [])))
    movement_type = str(movement.get("movement_type", ""))
    if movement_type not in allowed_types:
        reasons.append(f"movement type out of policy scope: {movement_type}")

    allowed_scopes = set(map(str, policy_pack.get("allowed_authority_scopes", [])))
    authority_scope = str(movement.get("authority_scope", ""))
    if not movement.get("authority_present", False):
        reasons.append("authority absent under policy pack")
    elif authority_scope not in allowed_scopes:
        reasons.append(f"authority scope invalid under policy pack: {authority_scope}")

    required_evidence = set(map(str, policy_pack.get("required_evidence", [])))
    accepted_evidence = evidence_types(movement)
    missing_evidence = sorted(required_evidence - accepted_evidence)
    for evidence_type in missing_evidence:
        reasons.append(f"required policy evidence missing: {evidence_type}")

    if policy_pack.get("custody_required", False) and not movement.get("custody_preserved", False):
        reasons.append("custody required by policy pack but not preserved")

    refusal_rules = policy_pack.get("refusal_rules", {}) or {}
    blocking_codes = set(map(str, refusal_rules.get("blocking_codes", [])))
    active_blocks = sorted(blocking_codes & active_refusal_codes(movement))
    for code in active_blocks:
        reasons.append(f"refusal rule overrides admission: {code}")

    verdict = "ADMIT" if not reasons else "REFUSE"
    return PolicyDecision(
        movement_id=movement_id,
        policy_pack_id=pack_id,
        policy_pack_hash=pack_hash,
        verdict=verdict,
        reasons=reasons or ["movement satisfies policy pack"],
    )
