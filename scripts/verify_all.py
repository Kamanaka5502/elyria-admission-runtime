from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Check:
    name: str
    command: List[str]


@dataclass(frozen=True)
class CheckResult:
    name: str
    command: List[str]
    returncode: int
    passed: bool


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


def run_check(check: Check) -> CheckResult:
    print(f"\n=== {check.name.upper()} ===")
    completed = subprocess.run(check.command, text=True)
    return CheckResult(
        name=check.name,
        command=check.command,
        returncode=completed.returncode,
        passed=completed.returncode == 0,
    )


def write_report(path: str | Path, results: List[CheckResult], *, skipped_tests: bool) -> None:
    report = {
        "report_type": "elyria_admission_runtime_verification_report",
        "generated_timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "skipped_tests": skipped_tests,
        "passed": all(result.passed for result in results),
        "results": [asdict(result) for result in results],
        "final_marker": "RESULT: ELYRIA ADMISSION RUNTIME FULL VERIFY PASS"
        if all(result.passed for result in results)
        else "RESULT: ELYRIA ADMISSION RUNTIME FULL VERIFY FAIL",
    }
    output = Path(path)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all Elyria buyer-review verification gates")
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Run verifier gates without pytest. Intended only for narrow troubleshooting.",
    )
    parser.add_argument(
        "--report",
        default=None,
        help="Optional path for a machine-readable verification report JSON file.",
    )
    args = parser.parse_args()

    checks = DEFAULT_CHECKS[1:] if args.skip_tests else DEFAULT_CHECKS
    results: List[CheckResult] = []
    for check in checks:
        result = run_check(check)
        results.append(result)
        if not result.passed:
            if args.report:
                write_report(args.report, results, skipped_tests=args.skip_tests)
            raise SystemExit(result.returncode)

    if args.report:
        write_report(args.report, results, skipped_tests=args.skip_tests)

    print("\nRESULT: ELYRIA ADMISSION RUNTIME FULL VERIFY PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
