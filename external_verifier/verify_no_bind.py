from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class VerificationError(RuntimeError):
    pass


REQUIRED_FIELDS = [
    "proof_type",
    "movement_attempted",
    "reason_admission_failed",
    "blocked_consequence_path",
    "route_closure_state",
    "receipt_reference",
    "replay_reference",
    "downstream_effect_status",
]


def verify_no_bind(proof: Dict[str, Any]) -> Dict[str, Any]:
    missing = [field for field in REQUIRED_FIELDS if field not in proof]
    if missing:
        raise VerificationError(f"no-bind proof missing fields: {', '.join(missing)}")
    if proof.get("route_closure_state") != "closed":
        raise VerificationError("no-bind route closure state is not closed")
    if proof.get("downstream_effect_status") != "not_activated":
        raise VerificationError("downstream effect status is not protected")
    if not proof.get("reason_admission_failed"):
        raise VerificationError("no-bind proof missing reason")
    return {
        "valid": True,
        "proof_type": proof.get("proof_type"),
        "receipt_reference": proof.get("receipt_reference"),
    }


def verify_no_bind_file(path: str | Path) -> Dict[str, Any]:
    return verify_no_bind(json.loads(Path(path).read_text(encoding="utf-8")))


if __name__ == "__main__":
    import sys

    result = verify_no_bind_file(sys.argv[1])
    print(json.dumps(result, indent=2, sort_keys=True))
