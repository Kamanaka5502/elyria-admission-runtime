from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from consequence_twin.demo_data import DEMO_ASSESSMENTS
from consequence_twin.graph import build_exposure_graph
from consequence_twin.storage import get_receipt, list_receipts, replay_from_store, store_assessment

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
DB_PATH = Path(os.getenv("ELYRIA_DB_PATH", "data/elyria.db"))

app = FastAPI(
    title="Elyria Consequence Twin API",
    version="0.1.0",
    description="Admission API for consequence-bearing execution.",
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class MovementAssessment(BaseModel):
    movement_id: str = Field(..., examples=["MOVE-001"])
    source_node: str | None = None
    target_node: str | None = None
    authority_present: bool
    authority_scope_valid: bool
    standing_active: bool
    evidence_present: bool
    evidence_sufficient: bool
    custody_preserved: bool
    refusal_condition_active: bool
    revalidation_required: bool
    receipt_available: bool
    replay_available: bool
    notes: str | None = None


@app.get("/")
def dashboard() -> FileResponse:
    index = STATIC_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(index)


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok", "service": "elyria-consequence-twin"}


@app.post("/movements/assess")
def assess_movement_endpoint(payload: MovementAssessment) -> Dict[str, Any]:
    return store_assessment(DB_PATH, payload.model_dump(exclude_none=True))


@app.get("/receipts")
def receipts(limit: int = 100) -> Dict[str, Any]:
    return {"items": list_receipts(DB_PATH, limit=limit)}


@app.get("/receipts/{receipt_id}")
def receipt(receipt_id: str) -> Dict[str, Any]:
    item = get_receipt(DB_PATH, receipt_id)
    if not item:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return item


@app.post("/receipts/{receipt_id}/replay")
def replay(receipt_id: str) -> Dict[str, Any]:
    result = replay_from_store(DB_PATH, receipt_id)
    if not result:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return result


@app.get("/exposures/demo")
def demo_exposure_graph() -> Dict[str, Any]:
    return build_exposure_graph(DEMO_ASSESSMENTS)


@app.post("/sandbox/reset")
def sandbox_reset() -> Dict[str, Any]:
    if DB_PATH.exists():
        DB_PATH.unlink()
    receipts = [store_assessment(DB_PATH, item) for item in DEMO_ASSESSMENTS]
    return {
        "status": "reset",
        "receipt_count": len(receipts),
        "receipts": receipts,
        "graph": build_exposure_graph(DEMO_ASSESSMENTS),
    }
