from consequence_twin.demo_data import DEMO_ASSESSMENTS
from consequence_twin.engine import Verdict, assess_movement
from consequence_twin.graph import build_exposure_graph
from consequence_twin.receipt_runtime import create_receipt, verify_receipt
from consequence_twin.storage import get_receipt, replay_from_store, store_assessment


def test_demo_graph_exposes_black_path():
    graph = build_exposure_graph(DEMO_ASSESSMENTS)
    assert graph["summary"]["total_movements"] == 3
    assert graph["summary"]["black_paths"] == 1
    assert any(edge["color"] == "black" for edge in graph["edges"])


def test_receipt_verification_matches_verdict_basis():
    receipt = create_receipt(DEMO_ASSESSMENTS[1]).to_dict()
    check = verify_receipt(receipt)
    assert check["input_hash_matches"] is True
    assert check["verdict_matches"] is True
    assert check["actual"]["verdict"] == "NO_PROVABLE_ADMISSION"


def test_sqlite_store_and_replay(tmp_path):
    db = tmp_path / "elyria.db"
    receipt = store_assessment(db, DEMO_ASSESSMENTS[0])
    loaded = get_receipt(db, receipt["receipt_id"])
    assert loaded is not None
    assert loaded["verdict"] == "ADMIT"
    check = replay_from_store(db, receipt["receipt_id"])
    assert check is not None
    assert check["verdict_matches"] is True


def test_engine_refuses_authority_collapse():
    result = assess_movement(DEMO_ASSESSMENTS[2])
    assert result.verdict == Verdict.REFUSE
    assert result.color == "red"
