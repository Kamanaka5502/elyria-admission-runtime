from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict


REVIEW_SIGNATURE_ALG = "SHA256-CANONICAL-REVIEW"
RECEIPT_SIGNING_FIELDS = [
    "receipt_id",
    "movement_id",
    "tenant_id",
    "verdict",
    "input_hash",
    "evidence_hash",
    "policy_pack_hash",
    "engine_version",
    "key_id",
    "signature_alg",
]


class VerificationError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def receipt_material(receipt: Dict[str, Any]) -> Dict[str, Any]:
    missing = [field for field in RECEIPT_SIGNING_FIELDS if field not in receipt]
    if missing:
        raise VerificationError(f"receipt missing fields: {', '.join(missing)}")
    return {field: receipt[field] for field in RECEIPT_SIGNING_FIELDS}


def verify_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    if receipt.get("signature_alg") != REVIEW_SIGNATURE_ALG:
        raise VerificationError("unsupported review signature algorithm")
    material = receipt_material(receipt)
    expected = sha256_json(material)
    actual = str(receipt.get("signature", ""))
    if actual != expected:
        raise VerificationError("receipt signature mismatch")
    return {
        "valid": True,
        "receipt_id": receipt["receipt_id"],
        "movement_id": receipt["movement_id"],
        "verdict": receipt["verdict"],
    }


def verify_receipt_file(path: str | Path) -> Dict[str, Any]:
    return verify_receipt(load_json(path))


if __name__ == "__main__":
    import sys

    result = verify_receipt_file(sys.argv[1])
    print(json.dumps(result, indent=2, sort_keys=True))
