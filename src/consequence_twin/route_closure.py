from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict


class RouteClosureError(ValueError):
    """Raised when a route closure invariant is violated."""


CLOSING_VERDICTS = {"REFUSE", "HOLD", "NO_PROVABLE_ADMISSION"}


@dataclass(frozen=True)
class RouteClosureProof:
    proof_type: str
    movement_id: str
    verdict: str
    protected_execution_route: str
    downstream_consequence_path: str
    route_state: str
    downstream_state: str
    receipt_reference: str | None
    replay_reference: str | None
    timestamp_utc: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def create_route_closure_proof(
    *,
    movement_id: str,
    verdict: str,
    receipt_reference: str | None = None,
    replay_reference: str | None = None,
    protected_execution_route: str = "protected_execution_route",
    downstream_consequence_path: str = "downstream_consequence_path",
) -> RouteClosureProof:
    normalized_verdict = str(verdict)
    route_state = "closed" if normalized_verdict in CLOSING_VERDICTS else "open"
    downstream_state = "not_activated" if route_state == "closed" else "eligible_after_admission"
    return RouteClosureProof(
        proof_type="elyria_route_closure_proof",
        movement_id=str(movement_id),
        verdict=normalized_verdict,
        protected_execution_route=protected_execution_route,
        downstream_consequence_path=downstream_consequence_path,
        route_state=route_state,
        downstream_state=downstream_state,
        receipt_reference=receipt_reference,
        replay_reference=replay_reference,
        timestamp_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def assert_closed_for_refusal(proof: Dict[str, Any]) -> None:
    verdict = str(proof.get("verdict", ""))
    if verdict in CLOSING_VERDICTS:
        if proof.get("route_state") != "closed":
            raise RouteClosureError("refused or held route must be closed")
        if proof.get("downstream_state") != "not_activated":
            raise RouteClosureError("closed route cannot activate downstream consequence")


def can_export_as_admitted(
    *,
    original_closure: Dict[str, Any],
    new_receipt: Dict[str, Any] | None = None,
) -> bool:
    if original_closure.get("verdict") == "ADMIT":
        return True
    if original_closure.get("route_state") != "closed":
        return False
    if not new_receipt:
        return False
    return (
        new_receipt.get("verdict") == "ADMIT"
        and new_receipt.get("receipt_id") != original_closure.get("receipt_reference")
        and new_receipt.get("changed_condition_replay") is True
    )
