from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from .engine import assess_movement


def _load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Assess consequence-bearing movements.")
    parser.add_argument("input", help="Path to a JSON assessment object or list of assessment objects.")
    parser.add_argument("--output", "-o", help="Optional output JSON path.")
    args = parser.parse_args()

    payload = _load_json(args.input)
    items: List[Dict[str, Any]] = payload if isinstance(payload, list) else [payload]
    results = [assess_movement(item).to_dict() for item in items]

    rendered = json.dumps(results, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
