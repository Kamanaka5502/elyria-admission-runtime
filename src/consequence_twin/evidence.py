from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class EvidenceSummary:
    total: int
    required: int
    accepted: int
    missing: int
    insufficient: int
    custody_gaps: int
    hash_gaps: int
    hash_references: int
    source_systems: List[str]
    custody_owners: List[str]
    status: str
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _norm(value: Any) -> str:
    return str(value or "").strip()


def summarize_evidence(payload: Dict[str, Any]) -> Dict[str, Any]:
    items = payload.get("evidence_items") or []
    if not isinstance(items, list):
        items = []

    total = len(items)
    required = 0
    accepted = 0
    missing = 0
    insufficient = 0
    custody_gaps = 0
    hash_gaps = 0
    hash_references = 0
    source_systems: set[str] = set()
    custody_owners: set[str] = set()
    reasons: List[str] = []

    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            insufficient += 1
            reasons.append(f"evidence item {idx} is not structured")
            continue

        item_id = _norm(item.get("evidence_id")) or f"evidence item {idx}"
        required_flag = bool(item.get("required", True))
        status = _norm(item.get("status")).lower() or "accepted"
        source_system = _norm(item.get("source_system"))
        custody_owner = _norm(item.get("custody_owner"))
        evidence_hash = _norm(item.get("hash_reference"))

        if required_flag:
            required += 1
        if source_system:
            source_systems.add(source_system)
        if custody_owner:
            custody_owners.add(custody_owner)
        if evidence_hash:
            hash_references += 1

        if status == "accepted":
            accepted += 1
        elif status == "missing":
            missing += 1
            if required_flag:
                reasons.append(f"required evidence missing: {item_id}")
        elif status == "insufficient":
            insufficient += 1
            if required_flag:
                reasons.append(f"required evidence insufficient: {item_id}")
        else:
            insufficient += 1
            reasons.append(f"evidence status unsupported for {item_id}: {status}")

        if required_flag and not custody_owner:
            custody_gaps += 1
            reasons.append(f"required evidence lacks custody owner: {item_id}")
        if required_flag and not evidence_hash:
            hash_gaps += 1
            reasons.append(f"required evidence lacks hash/reference: {item_id}")

    if total == 0:
        status = "not_attached"
        reasons.append("no structured evidence attachments provided")
    elif missing or insufficient or custody_gaps or hash_gaps:
        status = "attention_required"
    else:
        status = "supporting"

    return EvidenceSummary(
        total=total,
        required=required,
        accepted=accepted,
        missing=missing,
        insufficient=insufficient,
        custody_gaps=custody_gaps,
        hash_gaps=hash_gaps,
        hash_references=hash_references,
        source_systems=sorted(source_systems),
        custody_owners=sorted(custody_owners),
        status=status,
        reasons=reasons,
    ).to_dict()
