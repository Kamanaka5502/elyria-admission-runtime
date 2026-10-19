from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List

from .evidence import summarize_evidence


class Verdict(str, Enum):
    ADMIT = "ADMIT"
    HOLD = "HOLD"
    REFUSE = "REFUSE"
    NO_PROVABLE_ADMISSION = "NO_PROVABLE_ADMISSION"


VERDICT_COLOR = {
    Verdict.ADMIT: "green",
    Verdict.HOLD: "yellow",
    Verdict.REFUSE: "red",
    Verdict.NO_PROVABLE_ADMISSION: "black",
}


@dataclass(frozen=True)
class AssessmentResult:
    movement_id: str
    verdict: Verdict
    color: str
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["verdict"] = self.verdict.value
        return data


def _required_bool(payload: Dict[str, Any], key: str) -> bool:
    if key not in payload:
        raise ValueError(f"missing required assessment field: {key}")
    value = payload[key]
    if not isinstance(value, bool):
        raise TypeError(f"assessment field must be boolean: {key}")
    return value


def _add_unique(reasons: List[str], reason: str) -> None:
    if reason not in reasons:
        reasons.append(reason)


def _required_evidence_missing(evidence_summary: Dict[str, Any]) -> bool:
    return any(
        str(reason).startswith("required evidence missing:")
        for reason in evidence_summary.get("reasons", [])
    )


def assess_movement(payload: Dict[str, Any]) -> AssessmentResult:
    """
    Deterministic assessment of a proposed consequence-bearing movement.

    This public pilot classifies caller-supplied dimensions; it does not
    independently constitute standing or verify the truth/provenance of
    caller assertions. Structured evidence is required for ADMIT, but the
    presence of an attachment or a hash/reference does not itself authenticate
    the underlying evidence.
    """

    movement_id = str(payload.get("movement_id", "UNKNOWN"))

    authority_present = _required_bool(payload, "authority_present")
    authority_scope_valid = _required_bool(payload, "authority_scope_valid")
    standing_active = _required_bool(payload, "standing_active")
    evidence_present = _required_bool(payload, "evidence_present")
    evidence_sufficient = _required_bool(payload, "evidence_sufficient")
    custody_preserved = _required_bool(payload, "custody_preserved")
    refusal_condition_active = _required_bool(payload, "refusal_condition_active")
    revalidation_required = _required_bool(payload, "revalidation_required")
    receipt_available = _required_bool(payload, "receipt_available")
    replay_available = _required_bool(payload, "replay_available")

    evidence_summary = summarize_evidence(payload)
    has_structured_evidence = evidence_summary["total"] > 0

    hard_refusal_reasons: List[str] = []
    hold_reasons: List[str] = []
    black_path_reasons: List[str] = []

    if refusal_condition_active:
        hard_refusal_reasons.append("active refusal condition blocks consequence movement")
    if not authority_present:
        hard_refusal_reasons.append("authority absent")
    if authority_present and not authority_scope_valid:
        hard_refusal_reasons.append("authority exists but is outside required scope")
    if not standing_active:
        hard_refusal_reasons.append("standing inactive or expired")

    if not evidence_present:
        hold_reasons.append("required evidence missing before bind")
    if evidence_present and not evidence_sufficient:
        hold_reasons.append("evidence present but insufficient")
    if not custody_preserved:
        hold_reasons.append("custody not preserved")
    if revalidation_required:
        hold_reasons.append("material change requires revalidation")
    if not receipt_available:
        hold_reasons.append("receipt unavailable")
    if not replay_available:
        hold_reasons.append("replay unavailable")

    # Fail closed when the caller asserts evidence exists but supplies no
    # structured evidence objects. The Boolean fields are not substitutes
    # for the evidence attachments required by this public pilot.
    if not has_structured_evidence:
        _add_unique(
            hold_reasons,
            "no structured evidence attachments provided; admission cannot be established",
        )
        if authority_present and authority_scope_valid and standing_active:
            black_path_reasons.append(
                "authority and standing are asserted but required structured evidence is absent"
            )

    if has_structured_evidence and evidence_summary["status"] == "attention_required":
        for reason in evidence_summary["reasons"]:
            _add_unique(hold_reasons, reason)

    if not receipt_available or not replay_available:
        black_path_reasons.append("consequence path lacks durable receipt or replay proof")
    if authority_present and authority_scope_valid and standing_active and not evidence_present:
        black_path_reasons.append("authority appears to admit movement without required evidence")
    if not custody_preserved and evidence_present:
        black_path_reasons.append("evidence exists but custody does not hold")

    if (
        has_structured_evidence
        and _required_evidence_missing(evidence_summary)
        and authority_present
        and authority_scope_valid
        and standing_active
    ):
        black_path_reasons.append(
            "required structured evidence missing while authority could bind movement"
        )

    if hard_refusal_reasons:
        verdict = Verdict.REFUSE
        reasons = hard_refusal_reasons + hold_reasons
    elif black_path_reasons:
        verdict = Verdict.NO_PROVABLE_ADMISSION
        reasons = black_path_reasons + hold_reasons
    elif hold_reasons:
        verdict = Verdict.HOLD
        reasons = hold_reasons
    else:
        verdict = Verdict.ADMIT
        reasons = ["all configured assessment dimensions passed; standing and evidence provenance are not independently verified by this pilot"]

    return AssessmentResult(
        movement_id=movement_id,
        verdict=verdict,
        color=VERDICT_COLOR[verdict],
        reasons=reasons,
    )
