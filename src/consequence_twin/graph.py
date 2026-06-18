from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List

from .engine import assess_movement


def build_exposure_graph(assessments: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    verdicts = []

    for idx, payload in enumerate(assessments, start=1):
        result = assess_movement(payload).to_dict()
        verdicts.append(result["verdict"])
        source = payload.get("source_node", f"source-{idx}")
        target = payload.get("target_node", f"target-{idx}")
        movement_id = result["movement_id"]
        nodes.extend([
            {"id": source, "label": source, "kind": "source"},
            {"id": target, "label": target, "kind": "target", "status": result["color"]},
        ])
        edges.append({
            "id": movement_id,
            "from": source,
            "to": target,
            "verdict": result["verdict"],
            "color": result["color"],
            "reasons": result["reasons"],
        })

    unique_nodes = {node["id"]: node for node in nodes}
    counts = Counter(verdicts)
    return {
        "graph_id": "DEMO-GRAPH",
        "nodes": list(unique_nodes.values()),
        "edges": edges,
        "summary": {
            "total_movements": len(edges),
            "admit": counts.get("ADMIT", 0),
            "hold": counts.get("HOLD", 0),
            "refuse": counts.get("REFUSE", 0),
            "black_paths": counts.get("NO_PROVABLE_ADMISSION", 0),
        },
    }
