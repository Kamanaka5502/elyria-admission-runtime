# Traceability Matrix

## Purpose

This matrix maps Elyria Admission Runtime public review claims to implementation files, tests, and proof artifacts.

It is intended for buyer review, technical evaluation, recruiter review, implementation scoping, and final verification gate review.

## Current Status

```text
Implementation: complete across Phases 1-4
Verification: pending CI and fresh-clone evidence
Public posture: bounded buyer-review runtime candidate
Production deployment: subject to customer review and external review where required
```

## Claim-to-Evidence Matrix

| Public Review Claim | Implementation Surface | Test / Proof Surface | Status |
|---|---|---|---|
| runtime evaluates movement before consequence binds | `src/consequence_twin/engine.py` | engine tests, API tests, dashboard path | implemented for review |
| movement requires authority / standing / evidence / custody basis | `src/consequence_twin/engine.py`, `src/consequence_twin/evidence.py` | `tests/`, README engine flow | implemented for review |
| structured evidence can affect verdict | `src/consequence_twin/evidence.py` | `tests/`, `docs/15_evidence_enforcement.md` | implemented for review |
| admitted movement emits signed receipt envelope | `src/consequence_twin/receipt_runtime.py` | receipt replay tests, review bundle receipt | implemented for review |
| receipt replay verifies original basis | `src/consequence_twin/receipt_runtime.py` | replay tests, external verifier | implemented for review |
| black-path movement is visible as exposure | `src/consequence_twin/graph.py` | dashboard path, exposure graph docs | implemented for review |
| role permissions are explicit | `src/consequence_twin/authz.py` | `tests/test_auth_rbac.py` | implemented for review |
| tenant boundaries are enforced in review layer | `src/consequence_twin/tenant.py` | `tests/test_tenant_isolation.py` | implemented for review |
| signing adapter separates review signing from deployment signing | `src/consequence_twin/signing.py` | `tests/test_signing_adapter.py` | implemented for review |
| audit ledger supports ordered verification | `src/consequence_twin/audit_ledger.py` | `tests/test_audit_ledger.py`, external audit-chain verifier | implemented for review |
| receipt store prevents silent overwrite | `src/consequence_twin/receipt_store.py` | `tests/test_receipt_store.py` | implemented for review |
| policy pack can bound admissible movement | `src/consequence_twin/policy_pack.py` | `tests/test_policy_pack.py`, sample policy pack | implemented for review |
| refusal can produce no-bind proof | `src/consequence_twin/no_bind.py` | `tests/test_no_bind.py`, external no-bind verifier | implemented for review |
| held/refused route can be closed with proof state | `src/consequence_twin/route_closure.py` | `tests/test_route_closure.py` | implemented for review |
| changed condition replay creates linked review artifact | `src/consequence_twin/changed_replay.py` | `tests/test_changed_condition_replay.py`, external replay verifier | implemented for review |
| review bundle is independently inspectable | `review-bundle/latest/`, `external_verifier/` | `tests/test_external_verifier.py` | implemented for review |
| digest manifest can verify review bundle artifacts | `scripts/generate_digest_manifest.py`, `scripts/verify_digest_manifest.py` | `tests/test_digest_manifest.py` | implemented for review |
| production preflight separates review mode from production mode | `src/consequence_twin/preflight.py`, `scripts/production_preflight.py` | `tests/test_production_preflight.py` | implemented for review |
| one-command reviewer verification exists | `scripts/verify_all.py` | CI workflow, reviewer docs | implemented for review |
| verification report can be generated | `scripts/verify_all.py --report verification-report.json` | CI artifact path | implemented for review; evidence pending |
| final A+ wording is gated by evidence | `A_PLUS_VERIFICATION_GATE.md`, Issue #6 | fresh-clone evidence and CI status | gate pending |

## Verification Files

| File | Function |
|---|---|
| `BUYER_REVIEW_INDEX.md` | top-level review map |
| `REVIEWER_VERIFICATION.md` | one-command verification guide |
| `A_PLUS_VERIFICATION_GATE.md` | final gate before A+ wording |
| `FRESH_CLONE_REVIEW_TEST.md` | clean-clone review procedure |
| `VERIFICATION_EVIDENCE_TEMPLATE.md` | evidence capture template |
| `RELEASE_CHECKLIST.md` | release wording and final checks |
| `.github/workflows/ci.yml` | full verification runner in CI |
| `.github/workflows/review-bundle.yml` | review-bundle verifier workflow |
| `.github/workflows/security.yml` | security-posture workflow |

## Correct Claim Boundary

Current safe wording:

```text
Elyria Admission Runtime is a bounded buyer-review consequence-admission runtime candidate with implemented proof-gate layers across access control, tenant boundary, signed receipt review, audit-chain review, policy-pack mapping, no-bind proof, route closure, changed-condition replay, external verifier review, digest verification, and production preflight review mode.
```

Final A+ wording waits for CI and fresh-clone evidence.
