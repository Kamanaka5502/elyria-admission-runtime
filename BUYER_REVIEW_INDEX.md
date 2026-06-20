# Buyer Review Index

## Purpose

This is the top-level review map for Elyria Admission Runtime.

It directs a buyer, reviewer, recruiter, technical evaluator, or implementation partner to the current public proof surface and its recorded evidence.

## Current Classification

```text
Implementation: complete across Phases 1-4
Verification: CI proof-gates and hosted fresh-checkout evidence recorded
Final buyer-review gate: complete on current main
Public posture: A+ bounded buyer-review consequence-admission runtime candidate
Production deployment: subject to customer review and external review where required
```

## One-Command Verification

From repository root:

```bash
python scripts/verify_all.py --report verification-report.json
```

Expected final marker:

```text
RESULT: ELYRIA ADMISSION RUNTIME FULL VERIFY PASS
```

## Recorded Verification Evidence

```text
workflow: ci
run: #155
status: Success
job: proof-gates green
artifact: verification-report
```

Evidence files:

```text
verification-evidence/ci-155-verification-report.json
verification-evidence/CI_155_SUMMARY.md
FRESH_CLONE_REVIEW_TEST.md
```

## Core Review Files

| File | Purpose |
|---|---|
| `README.md` | public runtime overview and local run path |
| `STATUS.md` | current verified-main status |
| `TRACEABILITY_MATRIX.md` | public claim-to-evidence map |
| `A_PLUS_VERIFICATION_GATE.md` | recorded final buyer-review gate |
| `REVIEWER_VERIFICATION.md` | reviewer command path |
| `FRESH_CLONE_REVIEW_TEST.md` | hosted fresh-checkout and manual review path |
| `RELEASE_CHECKLIST.md` | release boundary and material checklist |
| `RELEASE_SYNC_STATUS.md` | immutable current-main release sync status |
| `RELEASE_SYNC_V0_8_2.md` | next release values and publication steps |
| `RELEASE_NOTES_V0_8_2_VERIFIED.md` | next verified release notes |
| `verification-evidence/CI_155_SUMMARY.md` | CI #155 evidence summary |
| `verification-evidence/ci-155-verification-report.json` | machine-readable CI report |

## Phase 1 — Enterprise Hardening Foundation

```text
RBAC
Tenant isolation
Signing adapter
Audit ledger
Receipt store
```

Implementation and tests:

```text
src/consequence_twin/authz.py
tests/test_auth_rbac.py
src/consequence_twin/tenant.py
tests/test_tenant_isolation.py
src/consequence_twin/signing.py
tests/test_signing_adapter.py
src/consequence_twin/audit_ledger.py
tests/test_audit_ledger.py
src/consequence_twin/receipt_store.py
tests/test_receipt_store.py
```

## Phase 2 — Consequence Proof Layer

```text
Policy packs
No-bind proof
Route closure
Changed-condition replay
```

Implementation and tests:

```text
src/consequence_twin/policy_pack.py
tests/test_policy_pack.py
src/consequence_twin/no_bind.py
tests/test_no_bind.py
src/consequence_twin/route_closure.py
tests/test_route_closure.py
src/consequence_twin/changed_replay.py
tests/test_changed_condition_replay.py
```

## Phase 3 — External Verifier and Review Bundle

```text
external_verifier/
review-bundle/latest/
scripts/generate_digest_manifest.py
scripts/verify_digest_manifest.py
tests/test_digest_manifest.py
tests/test_external_verifier.py
```

## Phase 4 — Production Boundary and CI Proof Gates

```text
PRODUCTION_PREFLIGHT.md
SECURITY_POSTURE.md
DEPLOYMENT_SECURITY_CHECKLIST.md
THREAT_MODEL.md
src/consequence_twin/preflight.py
scripts/production_preflight.py
scripts/verify_all.py
.github/workflows/ci.yml
.github/workflows/review-bundle.yml
.github/workflows/security.yml
tests/test_production_preflight.py
```

## Release Synchronization

```text
existing tag: v0.8.1-public
existing tag role: historic public release marker
verified runtime: current main
next immutable release: v0.8.2-public from current main
```

Use `RELEASE_SYNC_V0_8_2.md` and `RELEASE_NOTES_V0_8_2_VERIFIED.md` when publishing the current-main release snapshot.

## Buyer-Review Claim Boundary

```text
Elyria Admission Runtime is an A+ bounded buyer-review consequence-admission runtime candidate on current main, with recorded CI proof-gate evidence for unit tests, digest verification, external verifier review, and production preflight review mode.
```

Production deployment remains a separate customer-controlled step.
