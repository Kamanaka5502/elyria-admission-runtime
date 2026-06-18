from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from .engine import assess_movement
from .graph import build_exposure_graph
from .storage import replay_from_store, store_assessment


def _load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Assess consequence-bearing movements.")
    sub = parser.add_subparsers(dest="cmd")

    assess = sub.add_parser("assess", help="Assess a JSON movement or list of movements.")
    assess.add_argument("input")

    graph = sub.add_parser("graph", help="Build an exposure graph from assessments.")
    graph.add_argument("input")

    store = sub.add_parser("store", help="Assess and store receipts in SQLite.")
    store.add_argument("input")
    store.add_argument("--db", default="data/elyria.db")

    replay = sub.add_parser("replay", help="Replay a stored receipt.")
    replay.add_argument("receipt_id")
    replay.add_argument("--db", default="data/elyria.db")

    parser.add_argument("input", nargs="?", help="Backward-compatible input path for assessment.")
    args = parser.parse_args()

    cmd = args.cmd or "assess"
    input_path = getattr(args, "input", None)

    if cmd == "replay":
        print(json.dumps(replay_from_store(args.db, args.receipt_id), indent=2))
        return

    if not input_path:
        parser.error("input path required")

    payload = _load_json(input_path)
    items: List[Dict[str, Any]] = payload if isinstance(payload, list) else [payload]

    if cmd == "graph":
        print(json.dumps(build_exposure_graph(items), indent=2))
    elif cmd == "store":
        print(json.dumps([store_assessment(args.db, item) for item in items], indent=2))
    else:
        print(json.dumps([assess_movement(item).to_dict() for item in items], indent=2))


if __name__ == "__main__":
    main()
