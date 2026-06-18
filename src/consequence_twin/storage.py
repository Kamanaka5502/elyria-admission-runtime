from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from .receipt_runtime import ReceiptRecord, create_receipt, verify_receipt

SCHEMA = """
CREATE TABLE IF NOT EXISTS receipts (
    receipt_id TEXT PRIMARY KEY,
    movement_id TEXT NOT NULL,
    verdict TEXT NOT NULL,
    color TEXT NOT NULL,
    timestamp_utc TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    engine_version TEXT NOT NULL,
    receipt_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_receipts_movement_id ON receipts(movement_id);
CREATE INDEX IF NOT EXISTS idx_receipts_verdict ON receipts(verdict);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def store_assessment(db_path: str | Path, payload: Dict[str, Any]) -> Dict[str, Any]:
    init_db(db_path)
    receipt: ReceiptRecord = create_receipt(payload)
    receipt_dict = receipt.to_dict()
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO receipts (
                receipt_id, movement_id, verdict, color, timestamp_utc,
                input_hash, engine_version, receipt_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                receipt.receipt_id,
                receipt.movement_id,
                receipt.verdict,
                receipt.color,
                receipt.timestamp_utc,
                receipt.input_hash,
                receipt.engine_version,
                json.dumps(receipt_dict, sort_keys=True),
            ),
        )
        conn.commit()
    return receipt_dict


def list_receipts(db_path: str | Path, limit: int = 100) -> List[Dict[str, Any]]:
    init_db(db_path)
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT receipt_json FROM receipts ORDER BY timestamp_utc DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [json.loads(row["receipt_json"]) for row in rows]


def get_receipt(db_path: str | Path, receipt_id: str) -> Optional[Dict[str, Any]]:
    init_db(db_path)
    with connect(db_path) as conn:
        row = conn.execute(
            "SELECT receipt_json FROM receipts WHERE receipt_id = ?",
            (receipt_id,),
        ).fetchone()
    return json.loads(row["receipt_json"]) if row else None


def replay_from_store(db_path: str | Path, receipt_id: str) -> Optional[Dict[str, Any]]:
    receipt = get_receipt(db_path, receipt_id)
    if not receipt:
        return None
    return verify_receipt(receipt)
