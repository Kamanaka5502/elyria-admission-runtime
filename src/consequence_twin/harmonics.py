from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


UTC = timezone.utc
WEIGHTS = {
    "intent_context": 0.25,
    "evidence": 0.30,
    "authority": 0.25,
    "state": 0.20,
}


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def stable_hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _epoch(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp())
    except ValueError:
        return None


def _now(payload: Mapping[str, Any] | None = None) -> int:
    if payload and payload.get("evaluation_time") is not None:
        parsed = _epoch(payload.get("evaluation_time"))
        if parsed is not None:
            return parsed
    return int(datetime.now(UTC).timestamp())


def _shared_consistency(items: Sequence[Mapping[str, Any]]) -> List[str]:
    if not items:
        return ["no_evidence"]
    conflicts: List[str] = []
    common = set(items[0])
    for item in items[1:]:
        common &= set(item)
    common -= {"signature", "status", "evidence_id", "timestamp", "ttl"}
    for key in sorted(common):
        values = {_canonical(item.get(key)) for item in items}
        if len(values) > 1:
            conflicts.append(f"inconsistent_evidence:{key}")
    return conflicts


def _score_intent_context(intent: Mapping[str, Any], context: Mapping[str, Any]) -> Tuple[float, List[str], List[str]]:
    conflicts: List[str] = []
    warnings: List[str] = []
    required = context.get("required_intent_fields") or []
    missing = [key for key in required if key not in intent]
    if missing:
        conflicts.append("missing_intent_fields:" + ",".join(sorted(map(str, missing))))
    allowed_scopes = context.get("allowed_scopes") or []
    if allowed_scopes and intent.get("scope") not in allowed_scopes:
        conflicts.append("scope_not_allowed")
    if context.get("standing_active") is False:
        conflicts.append("standing_inactive")
    if context.get("continuity_valid") is False:
        conflicts.append("continuity_invalid")
    if context.get("high_risk"):
        warnings.append("high_risk_movement")
    return (0.0 if conflicts else (0.75 if warnings else 1.0), conflicts, warnings)


def _score_evidence(items: Iterable[Mapping[str, Any]], evaluation_time: int) -> Tuple[float, List[str], List[str], str]:
    evidence = list(items)
    conflicts: List[str] = []
    warnings: List[str] = []
    if not evidence:
        return 0.0, ["no_evidence"], warnings, ""
    for idx, item in enumerate(evidence, start=1):
        evidence_id = str(item.get("evidence_id") or f"evidence_{idx}")
        status = str(item.get("status") or "accepted").lower()
        if status != "accepted":
            conflicts.append(f"evidence_status_invalid:{evidence_id}:{status}")
        if item.get("revoked") is True:
            conflicts.append(f"evidence_revoked:{evidence_id}")
        if not item.get("hash_reference"):
            conflicts.append(f"evidence_hash_missing:{evidence_id}")
        if not item.get("custody_owner"):
            conflicts.append(f"evidence_custody_missing:{evidence_id}")
        timestamp = _epoch(item.get("timestamp"))
        ttl = item.get("ttl")
        if timestamp is not None and ttl is not None and timestamp + int(ttl) < evaluation_time:
            warnings.append(f"evidence_stale:{evidence_id}")
        signature = str(item.get("signature") or "").strip()
        if not signature:
            conflicts.append(f"evidence_signature_missing:{evidence_id}")
    conflicts.extend(_shared_consistency(evidence))
    root = stable_hash(evidence)
    return (0.0 if conflicts else (0.8 if warnings else 1.0), conflicts, warnings, root)


def _score_authority(authority: Mapping[str, Any], evaluation_time: int) -> Tuple[float, List[str], List[str], str]:
    conflicts: List[str] = []
    warnings: List[str] = []
    participants = [str(x) for x in (authority.get("participants") or [])]
    threshold = int(authority.get("threshold") or 0)
    if not participants:
        conflicts.append("authority_missing")
    if len(set(participants)) != len(participants):
        conflicts.append("authority_duplicate_participant")
    if threshold < 1 or len(participants) < threshold:
        conflicts.append("authority_threshold_not_met")
    if authority.get("revoked") is True:
        conflicts.append("authority_revoked")
    expiry = _epoch(authority.get("expiry"))
    if expiry is not None:
        if evaluation_time > expiry:
            conflicts.append("authority_expired")
        elif expiry - evaluation_time < 60:
            warnings.append("authority_near_expiry")
    nullifiers = [str(x) for x in (authority.get("nullifiers") or [])]
    if threshold and len(nullifiers) < threshold:
        conflicts.append("authority_nullifier_gap")
    if authority.get("consumed") is True:
        conflicts.append("authority_already_consumed")
    root = stable_hash({"participants": participants, "threshold": threshold, "nullifiers": nullifiers})
    return (0.0 if conflicts else (0.85 if warnings else 1.0), conflicts, warnings, root)


def _score_state(before_state_hash: str, delta_hash: str, context: Mapping[str, Any]) -> Tuple[float, List[str], List[str]]:
    conflicts: List[str] = []
    warnings: List[str] = []
    allowed = {str(x) for x in (context.get("allowed_delta_hashes") or [])}
    if allowed and delta_hash not in allowed:
        conflicts.append("delta_not_allowed")
    if context.get("state_current") is False:
        conflicts.append("state_not_current")
    if context.get("rollback_available") is False:
        warnings.append("rollback_not_available")
    transition_map = context.get("transition_map") or {}
    if transition_map and before_state_hash not in transition_map:
        warnings.append("state_transition_unmapped")
    return (0.0 if conflicts else (0.75 if warnings else 1.0), conflicts, warnings)


@dataclass(frozen=True)
class HarmonicResolution:
    alignment_score: float
    coherence_vector: Dict[str, float]
    conflicts: List[str]
    warnings: List[str]
    evidence_root: str
    authority_root: str
    evaluator_version: str = "harmonics-v1"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def resolve_harmonics(
    *,
    intent: Mapping[str, Any],
    evidence_items: Sequence[Mapping[str, Any]],
    authority: Mapping[str, Any],
    context: Mapping[str, Any],
    before_state_hash: str,
    delta_hash: str,
    evaluation_time: Any = None,
) -> HarmonicResolution:
    now = _now({"evaluation_time": evaluation_time} if evaluation_time is not None else None)
    i, ic, iw = _score_intent_context(intent, context)
    e, ec, ew, evidence_root = _score_evidence(evidence_items, now)
    a, ac, aw, authority_root = _score_authority(authority, now)
    s, sc, sw = _score_state(before_state_hash, delta_hash, context)
    conflicts = ic + ec + ac + sc
    warnings = iw + ew + aw + sw
    alignment = (
        WEIGHTS["intent_context"] * i
        + WEIGHTS["evidence"] * e
        + WEIGHTS["authority"] * a
        + WEIGHTS["state"] * s
    )
    if conflicts:
        alignment = 0.0
    return HarmonicResolution(
        alignment_score=round(alignment, 6),
        coherence_vector={
            "intent_context": round(i, 6),
            "evidence": round(e, 6),
            "authority": round(a, 6),
            "state": round(s, 6),
        },
        conflicts=sorted(set(conflicts)),
        warnings=sorted(set(warnings)),
        evidence_root=evidence_root,
        authority_root=authority_root,
    )
