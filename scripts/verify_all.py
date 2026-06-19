from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Check:
    name: str
    command: List[str]


DEFAULT_CHECKS = [
    Check("unit tests", [sys.executable, "-m", "pytest"]),
    Check(
        "generate digest manifest",
        [sys.executable, "scripts/generate_digest_manifest.py", "review-bundle/latest"],
    ),
    Check(
        "verify digest manifest",
        [sys.executable, "scripts/verify_digest_manifest.py", "review-bundle/latest"],
    ),
    Check(
        "external verifier",
        [sys.executable, "external_verifier/verify_bundle.py", "review-bundle/latest"],
    ),
    Check(
        "production preflight review mode",
        [sys.executable, "scripts/production_preflight.py", "--mode", "review"],
    ),
]


def run_check(check: Check) -> None:
    print(f"\n=== {check.name.upper()} ===")
    completed = subprocess.run(check.command, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all Elyria buyer-review verification gates")
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Run verifier gates without pytest. Intended only for narrow troubleshooting.",
    )
    args = parser.parse_args()

    checks = DEFAULT_CHECKS[1:] if args.skip_tests else DEFAULT_CHECKS
    for check in checks:
        run_check(check)

    print("\nRESULT: ELYRIA ADMISSION RUNTIME FULL VERIFY PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
