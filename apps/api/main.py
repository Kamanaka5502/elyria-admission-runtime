from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from consequence_twin.auth import require_client_auth
from consequence_twin.demo_data import DEMO_ASSESSMENTS
from consequence_twin.graph import build_exposure_graph
from consequence_twin.settings import get_settings
from consequence_twin.storage import get_receipt, list_receipts, replay_from_store, store_assessment

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"

app = FastAPI(
    title="Elyria Consequence Twin API",
    version="0.4.0",
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


def db_path() -> str:
    return get_settings().db_path


@app.get("/")
def dashboard() -> FileResponse:
    index = STATIC_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(index)


@app.get("/healthz")
def healthz() -> Dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "elyria-consequence-twin",
        "mode": settings.mode,
        "storage_backend": settings.storage_backend,
    }


@app.post("/movements/assess", dependencies=[Depends(require_client_auth)])
def assess_movement_endpoint(payload: MovementAssessment) -> Dict[str, Any]:
    return store_assessment(db_path(), payload.model_dump(exclude_none=True))


@app.get("/receipts", dependencies=[Depends(require_client_auth)])
def receipts(limit: int = 100) -> Dict[str, Any]:
    return {"items": list_receipts(db_path(), limit=limit)}


@app.get("/receipts/{receipt_id}", dependencies=[Depends(require_client_auth)])
def receipt(receipt_id: str) -> Dict[str, Any]:
    item = get_receipt(db_path(), receipt_id)
    if not item:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return item


@app.post("/receipts/{receipt_id}/replay", dependencies=[Depends(require_client_auth)])
def replay(receipt_id: str) -> Dict[str, Any]:
    result = replay_from_store(db_path(), receipt_id)
    if not result:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return result


@app.get("/exposures/demo")
def demo_exposure_graph() -> Dict[str, Any]:
    return build_exposure_graph(DEMO_ASSESSMENTS)


@app.get("/demo/proof", dependencies=[Depends(require_client_auth)])
def demo_proof_packet() -> Dict[str, Any]:
    receipts = list_receipts(db_path(), limit=100)
    return {
        "service": healthz(),
        "graph": build_exposure_graph(DEMO_ASSESSMENTS),
        "receipts": receipts,
        "proof_claim": "Elyria Consequence Twin classifies consequence-bearing movement, emits signed receipts, preserves replay basis, and exposes black-path execution risk before consequence binds.",
    }


@app.post("/sandbox/reset", dependencies=[Depends(require_client_auth)])
def sandbox_reset() -> Dict[str, Any]:
    settings = get_settings()
    path = Path(settings.db_path)
    if path.exists():
        path.unlink()
    receipts = [store_assessment(settings.db_path, item) for item in DEMO_ASSESSMENTS]
    return {
        "status": "reset",
        "mode": settings.mode,
        "receipt_count": len(receipts),
        "receipts": receipts,
        "graph": build_exposure_graph(DEMO_ASSESSMENTS),
    }
