from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from .receipt_runtime import sha256_json, verify_receipt


class ReceiptStoreError(RuntimeError):
    """Raised when durable receipt-store semantics are violated."""


@dataclass(frozen=True)
class StoredReceipt:
    receipt_id: str
    receipt_hash: str
    path: str


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def receipt_path(root: str | Path, receipt_id: str) -> Path:
    safe = str(receipt_id).replace("/", "_").replace("\\", "_")
    return Path(root) / "receipts" / f"{safe}.json"


def write_once_receipt(root: str | Path, receipt: Dict[str, Any]) -> StoredReceipt:
    receipt_id = str(receipt.get("receipt_id", "")).strip()
    if not receipt_id:
        raise ReceiptStoreError("receipt_id is required")
    path = receipt_path(root, receipt_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise ReceiptStoreError(f"receipt already exists and cannot be overwritten: {receipt_id}")
    path.write_text(canonical_json(receipt), encoding="utf-8")
    return StoredReceipt(
        receipt_id=receipt_id,
        receipt_hash=sha256_json(receipt),
        path=str(path),
    )


def read_receipt(root: str | Path, receipt_id: str) -> Dict[str, Any]:
    path = receipt_path(root, receipt_id)
    if not path.exists():
        raise ReceiptStoreError(f"receipt not found: {receipt_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def list_receipt_ids(root: str | Path) -> List[str]:
    directory = Path(root) / "receipts"
    if not directory.exists():
        return []
    return sorted(path.stem for path in directory.glob("*.json"))


def verify_stored_receipt(root: str | Path, receipt_id: str) -> Dict[str, Any]:
    receipt = read_receipt(root, receipt_id)
    verification = verify_receipt(receipt)
    verification["receipt_hash"] = sha256_json(receipt)
    verification["stored_path"] = str(receipt_path(root, receipt_id))
    return verification


def export_proof_packet(root: str | Path, receipt_id: str) -> Dict[str, Any]:
    receipt = read_receipt(root, receipt_id)
    receipt_hash = sha256_json(receipt)
    return {
        "packet_type": "elyria_admission_runtime_receipt_proof_packet",
        "receipt_id": receipt_id,
        "receipt_hash": receipt_hash,
        "manifest": {
            "receipt.json": receipt_hash,
        },
        "receipt": receipt,
        "verification": verify_receipt(receipt),
    }
