from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .engine import Verdict, assess_movement
from .evidence import summarize_evidence

CONTINUITY_VERSION = "0.1.0"
SIGNATURE_ALGORITHM = "Ed25519"
GENESIS = "GENESIS"


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def sign_digest(value: str, private_key: Ed25519PrivateKey) -> str:
    return private_key.sign(value.encode("ascii")).hex()


def verify_digest(value: str, signature: str, public_key: Ed25519PublicKey) -> bool:
    try:
        public_key.verify(bytes.fromhex(signature), value.encode("ascii"))
        return True
    except (InvalidSignature, ValueError):
        return False


@dataclass(frozen=True)
class NodeIdentity:
    node_id: str
    public_key: str
    active: bool = True


class IdentityRegistry:
    def __init__(self) -> None:
        self._identities: Dict[str, NodeIdentity] = {}

    def register(self, node_id: str, public_key: Ed25519PublicKey) -> NodeIdentity:
        identity = NodeIdentity(
            node_id=node_id,
            public_key=public_key.public_bytes(
                serialization.Encoding.Raw,
                serialization.PublicFormat.Raw,
            ).hex(),
        )
        self._identities[node_id] = identity
        return identity

    def revoke(self, node_id: str) -> None:
        identity = self._identities[node_id]
        self._identities[node_id] = NodeIdentity(
            node_id=identity.node_id,
            public_key=identity.public_key,
            active=False,
        )

    def get(self, node_id: str) -> NodeIdentity:
        return self._identities[node_id]

    def active(self, node_id: str) -> bool:
        identity = self._identities.get(node_id)
        return bool(identity and identity.active)

    def public_key(self, node_id: str) -> Ed25519PublicKey:
        identity = self.get(node_id)
        return Ed25519PublicKey.from_public_bytes(bytes.fromhex(identity.public_key))


@dataclass(frozen=True)
class ContinuityRecord:
    receipt_id: str
    movement_id: str
    origin: str
    previous_final_seal: str
    pre_state: Dict[str, Any]
    pre_seal: str
    quorum: Dict[str, Any]
    post_state: Dict[str, Any]
    post_seal: str
    final_seal: str
    continuation: Dict[str, Any]
    signature_algorithm: str
    origin_signature: str
    created_at_utc: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "movement_id": self.movement_id,
            "origin": self.origin,
            "previous_final_seal": self.previous_final_seal,
            "pre_state": self.pre_state,
            "pre_seal": self.pre_seal,
            "quorum": self.quorum,
            "post_state": self.post_state,
            "post_seal": self.post_seal,
            "final_seal": self.final_seal,
            "continuation": self.continuation,
            "signature_algorithm": self.signature_algorithm,
            "origin_signature": self.origin_signature,
            "created_at_utc": self.created_at_utc,
        }


def _quorum_material(pre_seal: str, votes: Mapping[str, str]) -> Dict[str, Any]:
    return {
        "threshold": len(votes),
        "votes": [{"node": node, "signature": votes[node]} for node in sorted(votes)],
        "pre_seal": pre_seal,
    }


def _pre_material(
    movement_id: str,
    origin: str,
    previous_final_seal: str,
    payload: Mapping[str, Any],
    evidence_summary: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "version": CONTINUITY_VERSION,
        "movement_id": movement_id,
        "origin": origin,
        "previous_final_seal": previous_final_seal,
        "input": dict(payload),
        "evidence_summary": dict(evidence_summary),
        "assessment": assess_movement(dict(payload)).to_dict(),
    }


def _post_material(pre_seal: str, outcome: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "pre_seal": pre_seal,
        "outcome": dict(outcome),
    }


def _final_material(
    receipt_id: str,
    pre_seal: str,
    quorum_seal: str,
    post_seal: str,
) -> Dict[str, Any]:
    return {
        "version": CONTINUITY_VERSION,
        "receipt_id": receipt_id,
        "pre_seal": pre_seal,
        "quorum_seal": quorum_seal,
        "post_seal": post_seal,
    }


def _continuation_material(final_seal: str, next_payload: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "final_seal": final_seal,
        "next_input_hash": digest(dict(next_payload)),
    }


def build_continuity_record(
    payload: Mapping[str, Any],
    origin: str,
    private_key: Ed25519PrivateKey,
    registry: IdentityRegistry,
    previous_final_seal: str = GENESIS,
    quorum_keys: Mapping[str, Ed25519PrivateKey] | None = None,
) -> ContinuityRecord:
    if not registry.active(origin):
        raise ValueError("IDENTITY_INACTIVE")

    assessment = assess_movement(dict(payload))
    if assessment.verdict != Verdict.ADMIT:
        raise ValueError(f"ADMISSION_NOT_BINDABLE:{assessment.verdict.value}")

    evidence_summary = summarize_evidence(dict(payload))
    pre_state = _pre_material(
        assessment.movement_id,
        origin,
        previous_final_seal,
        payload,
        evidence_summary,
    )
    pre_seal = digest(pre_state)

    voters = quorum_keys or {origin: private_key}
    if origin not in voters:
        voters = {origin: private_key, **voters}

    votes: Dict[str, str] = {}
    for node_id, signer in sorted(voters.items()):
        if not registry.active(node_id):
            raise ValueError(f"QUORUM_IDENTITY_INACTIVE:{node_id}")
        votes[node_id] = sign_digest(pre_seal, signer)

    quorum = _quorum_material(pre_seal, votes)
    quorum_seal = digest(quorum)

    outcome = {
        "status": "APPLIED",
        "movement_id": assessment.movement_id,
        "admitted_from": pre_seal,
    }
    post_state = _post_material(pre_seal, outcome)
    post_seal = digest(post_state)

    receipt_id = f"ECR-{uuid.uuid4().hex[:16].upper()}"
    final_seal = digest(_final_material(receipt_id, pre_seal, quorum_seal, post_seal))
    continuation = {
        "status": "PENDING",
        "basis": final_seal,
    }

    return ContinuityRecord(
        receipt_id=receipt_id,
        movement_id=assessment.movement_id,
        origin=origin,
        previous_final_seal=previous_final_seal,
        pre_state=pre_state,
        pre_seal=pre_seal,
        quorum=quorum,
        post_state=post_state,
        post_seal=post_seal,
        final_seal=final_seal,
        continuation=continuation,
        signature_algorithm=SIGNATURE_ALGORITHM,
        origin_signature=sign_digest(final_seal, private_key),
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def verify_continuity_record(
    record: Mapping[str, Any],
    registry: IdentityRegistry,
) -> Dict[str, bool]:
    pre_ok = digest(record["pre_state"]) == record["pre_seal"]
    quorum_votes = record["quorum"]["votes"]
    quorum_material = {
        "threshold": len(quorum_votes),
        "votes": sorted(quorum_votes, key=lambda item: item["node"]),
        "pre_seal": record["pre_seal"],
    }
    quorum_seal = digest(quorum_material)

    votes_ok = True
    seen = set()
    for vote in quorum_votes:
        node = vote["node"]
        if node in seen or not registry.active(node):
            votes_ok = False
            break
        seen.add(node)
        if not verify_digest(
            record["pre_seal"],
            vote["signature"],
            registry.public_key(node),
        ):
            votes_ok = False
            break

    post_ok = digest(record["post_state"]) == record["post_seal"]
    final_ok = digest(
        _final_material(
            record["receipt_id"],
            record["pre_seal"],
            quorum_seal,
            record["post_seal"],
        )
    ) == record["final_seal"]

    origin_ok = (
        registry.active(record["origin"])
        and verify_digest(
            record["final_seal"],
            record["origin_signature"],
            registry.public_key(record["origin"]),
        )
    )

    return {
        "pre_valid": pre_ok,
        "quorum_valid": votes_ok and bool(quorum_votes),
        "post_valid": post_ok,
        "final_valid": final_ok,
        "origin_signature_valid": origin_ok,
        "continuity_valid": (
            pre_ok
            and votes_ok
            and bool(quorum_votes)
            and post_ok
            and final_ok
            and origin_ok
        ),
    }


def admit_continuation(
    record: Mapping[str, Any],
    next_payload: Mapping[str, Any],
    registry: IdentityRegistry,
    admitting_node: str,
    private_key: Ed25519PrivateKey,
) -> Dict[str, Any]:
    verification = verify_continuity_record(record, registry)
    if not verification["continuity_valid"]:
        raise ValueError("CONTINUATION_DENIED:INVALID_CONTINUITY")
    if not registry.active(admitting_node):
        raise ValueError("CONTINUATION_DENIED:IDENTITY_INACTIVE")

    material = _continuation_material(record["final_seal"], next_payload)
    continuation_seal = digest(material)
    return {
        "status": "ADMITTED",
        "predecessor_final_seal": record["final_seal"],
        "next_input_hash": material["next_input_hash"],
        "continuation_seal": continuation_seal,
        "admitting_node": admitting_node,
        "signature_algorithm": SIGNATURE_ALGORITHM,
        "signature": sign_digest(continuation_seal, private_key),
    }
