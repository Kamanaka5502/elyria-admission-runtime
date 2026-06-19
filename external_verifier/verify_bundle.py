from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.verify_digest_manifest import verify_manifest
from external_verifier.verify_audit_chain import verify_audit_chain_file
from external_verifier.verify_no_bind import verify_no_bind_file
from external_verifier.verify_receipt import verify_receipt_file
from external_verifier.verify_replay import verify_replay_file


class BundleVerificationError(RuntimeError):
    pass


def verify_bundle(bundle_dir: str | Path) -> Dict[str, Any]:
    root = Path(bundle_dir)
    required_paths = [
        "DIGEST_MANIFEST.json",
        "sample_receipts/receipt_admit.json",
        "sample_audit_chain/audit_chain.json",
        "sample_no_bind/no_bind_refuse.json",
        "sample_replays/changed_replay.json",
    ]
    missing = [path for path in required_paths if not (root / path).exists()]
    if missing:
        raise BundleVerificationError(f"bundle missing required files: {', '.join(missing)}")

    digest_result = verify_manifest(root)
    receipt_result = verify_receipt_file(root / "sample_receipts/receipt_admit.json")
    audit_result = verify_audit_chain_file(root / "sample_audit_chain/audit_chain.json")
    no_bind_result = verify_no_bind_file(root / "sample_no_bind/no_bind_refuse.json")
    replay_result = verify_replay_file(root / "sample_replays/changed_replay.json")

    return {
        "valid": True,
        "digest": digest_result,
        "receipt": receipt_result,
        "audit_chain": audit_result,
        "no_bind": no_bind_result,
        "replay": replay_result,
    }


def main(argv: List[str] | None = None) -> int:
    args = list(argv or sys.argv[1:])
    bundle_dir = args[0] if args else "review-bundle/latest"
    try:
        verify_bundle(bundle_dir)
    except Exception as exc:
        print(f"RESULT: ELYRIA ADMISSION RUNTIME VERIFIER FAIL: {exc}")
        return 1
    print("RESULT: ELYRIA ADMISSION RUNTIME VERIFIER PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
