# Buyer Review Index

## Purpose

This is the top-level review map for Elyria Admission Runtime.

It points a buyer, reviewer, recruiter, technical evaluator, or implementation partner to the current public proof surface without overstating deployment status.

## Current Classification

```text
Implementation: complete across Phases 1-4
Verification: CI evidence recorded; fresh-clone evidence pending
Public posture: bounded buyer-review runtime candidate
Production deployment: subject to customer review and external review where required
```

## One-Command Verification

From repository root:

```bash
python scripts/verify_all.py
```

With report output:

```bash
python scripts/verify_all.py --report verification-report.json
```

Expected final marker:

```text
RESULT: ELYRIA ADMISSION RUNTIME FULL VERIFY PASS
```

## Core Review Files

| File | Purpose |
|---|---|
| `README.md` | public runtime overview and local run path |
| `STATUS.md` | plain-language current status snapshot |
| `TRACEABILITY_MATRIX.md` | public claim-to-evidence map |
| `ROADMAP_A_PLUS_BUYER_REVIEW.md` | phased A+ buyer-review roadmap |
| `A_PLUS_VERIFICATION_GATE.md` | final evidence gate before A+ wording |
| `REVIEWER_VERIFICATION.md` | reviewer command path |
| `RELEASE_CHECKLIST.md` | release naming and bounded wording |
| `RELEASE_NOTES_V0_8_1_PUBLIC.md` | public release notes |
| `RELEASE_PUBLICATION_STEPS.md` | GitHub release publication steps |
| `FRESH_CLONE_REVIEW_TEST.md` | clean-clone verification procedure |
| `VERIFICATION_EVIDENCE_TEMPLATE.md` | evidence capture template |
| `verification-evidence/CI_155_SUMMARY.md` | CI #155 verification summary |
| `verification-evidence/ci-155-verification-report.json` | machine-readable CI report evidence |

## Phase 1 — Enterprise Hardening Foundation

| File | Purpose |
|---|---|
| `AUTH_RBAC.md` | role and permission boundary |
| `TENANT_ISOLATION.md` | tenant-scoped review boundary |
| `PRODUCTION_SIGNING_ADAPTER.md` | signing adapter posture |
| `PERSISTENT_AUDIT_LEDGER.md` | audit-chain model |
| `PERSISTENT_RECEIPT_STORE.md` | write-once receipt-store boundary |

Implementation files:

```text
src/consequence_twin/authz.py
src/consequence_twin/tenant.py
src/consequence_twin/signing.py
src/consequence_twin/audit_ledger.py
src/consequence_twin/receipt_store.py
```

Tests:

```text
tests/test_auth_rbac.py
tests/test_tenant_isolation.py
tests/test_signing_adapter.py
tests/test_audit_ledger.py
tests/test_receipt_store.py
```

## Phase 2 — Consequence Proof Layer

| File | Purpose |
|---|---|
| `POLICY_PACKS.md` | customer corridor / policy-pack mapping |
| `NO_BIND_PROOF.md` | no-bind proof surface |
| `ROUTE_CLOSURE_PROOF.md` | route closure proof surface |
| `CHANGED_CONDITION_REPLAY.md` | changed-condition replay surface |

Implementation files:

```text
src/consequence_twin/policy_pack.py
src/consequence_twin/no_bind.py
src/consequence_twin/route_closure.py
src/consequence_twin/changed_replay.py
```

Tests:

```text
tests/test_policy_pack.py
tests/test_no_bind.py
tests/test_route_closure.py
tests/test_changed_condition_replay.py
```

## Phase 3 — External Verifier and Review Bundle

| File / Folder | Purpose |
|---|---|
| `EXTERNAL_VERIFIER_GUIDE.md` | external verifier instructions |
| `external_verifier/` | standalone verification scripts |
| `review-bundle/latest/` | sample review bundle |
| `review-bundle/latest/DIGEST_MANIFEST.json` | artifact digest manifest |
| `scripts/generate_digest_manifest.py` | manifest generator |
| `scripts/verify_digest_manifest.py` | manifest verifier |

Tests:

```text
tests/test_digest_manifest.py
tests/test_external_verifier.py
```

## Phase 4 — Production Boundary and CI Proof Gates

| File | Purpose |
|---|---|
| `PRODUCTION_PREFLIGHT.md` | review/production preflight distinction |
| `SECURITY_POSTURE.md` | security posture map |
| `DEPLOYMENT_SECURITY_CHECKLIST.md` | deployment checklist |
| `THREAT_MODEL.md` | review threat model |
| `.github/workflows/ci.yml` | full verification runner |
| `.github/workflows/review-bundle.yml` | review-bundle verification workflow |
| `.github/workflows/security.yml` | security posture workflow |

Implementation files:

```text
src/consequence_twin/preflight.py
scripts/production_preflight.py
scripts/verify_all.py
```

Tests:

```text
tests/test_production_preflight.py
```

## Open Tracking Issues

| Issue | Purpose |
|---|---|
| `#2` | Phase 1 enterprise hardening foundation |
| `#3` | Phase 2 consequence proof layer |
| `#4` | Phase 3 external verifier and review bundle |
| `#5` | Phase 4 production boundary and CI proof gates |
| `#6` | final A+ verification evidence gate |

## Buyer-Review Claim Boundary

Safe current wording:

```text
Elyria Admission Runtime is a bounded buyer-review consequence-admission runtime candidate with implemented proof-gate layers across access control, tenant boundary, signed receipt review, audit-chain review, policy-pack mapping, no-bind proof, route closure, changed-condition replay, external verifier review, digest verification, and production preflight review mode.
```

Final A+ wording should wait until fresh-clone evidence and release evidence are recorded in the final verification gate.
