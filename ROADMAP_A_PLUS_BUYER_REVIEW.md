# A+ Buyer-Review Roadmap

## Target

Elyria Admission Runtime is being advanced toward an A+ bounded buyer-review consequence-admission runtime candidate.

The current public release is buyer-showable and reviewer-runnable. It demonstrates dashboard intake, API assessment, deterministic admission logic, evidence-gated verdicts, signed receipts, replay verification, black-path exposure, proof-packet export, source install, container install posture, bounded claim language, and proprietary source-available licensing.

This roadmap does not claim production certification.

Production deployment remains dependent on customer security review, external audit where required, production key custody, enterprise identity, tenant isolation approval, customer-specific policy packs, and deployment-specific controls.

## Safe A+ Claim

```text
Elyria Admission Runtime is an A+ bounded buyer-review consequence-admission runtime candidate when the enterprise-hardening roadmap is complete and verified.
```

## Phase 1 — Enterprise Hardening Foundation

Goal: establish access control, isolation, signing abstraction, persistent proof storage, and tamper-evident event history.

Required additions:

- `AUTH_RBAC.md`
- `TENANT_ISOLATION.md`
- `PRODUCTION_SIGNING_ADAPTER.md`
- `PERSISTENT_AUDIT_LEDGER.md`
- `PERSISTENT_RECEIPT_STORE.md`
- `src/consequence_twin/authz.py`
- `src/consequence_twin/tenant.py`
- `src/consequence_twin/signing.py`
- `src/consequence_twin/audit_ledger.py`
- `src/consequence_twin/receipt_store.py`
- `tests/test_auth_rbac.py`
- `tests/test_tenant_isolation.py`
- `tests/test_signing_adapter.py`
- `tests/test_audit_ledger.py`
- `tests/test_receipt_store.py`

Phase 1 pass conditions:

- role permissions are explicit and test-covered
- tenant boundaries fail closed
- production signing cannot silently use demo keys
- audit events form a verifiable hash chain
- receipt persistence prevents silent overwrite

## Phase 2 — Consequence Proof Layer

Goal: prove not only admission, but refusal, no-bind, route closure, and changed-condition replay.

Required additions:

- `POLICY_PACKS.md`
- `NO_BIND_PROOF.md`
- `ROUTE_CLOSURE_PROOF.md`
- `CHANGED_CONDITION_REPLAY.md`
- `examples/policy_packs/basic_customer_corridor.json`
- `schemas/policy_pack.schema.json`
- `src/consequence_twin/policy_pack.py`
- `src/consequence_twin/no_bind.py`
- `src/consequence_twin/route_closure.py`
- `src/consequence_twin/changed_replay.py`
- `tests/test_policy_pack.py`
- `tests/test_no_bind.py`
- `tests/test_route_closure.py`
- `tests/test_changed_condition_replay.py`

Phase 2 pass conditions:

- the governing policy pack is identified by digest in the decision record
- refused movement emits no-bind proof
- held or refused routes produce closure state
- changed-condition replay creates a new linked receipt rather than mutating the original

## Phase 3 — External Verification and Review Bundle

Goal: allow a reviewer to verify proof artifacts outside the running app.

Required additions:

- `EXTERNAL_VERIFIER_GUIDE.md`
- `review-bundle/latest/`
- `review-bundle/latest/DIGEST_MANIFEST.json`
- `scripts/generate_digest_manifest.py`
- `scripts/verify_digest_manifest.py`
- `external_verifier/verify_bundle.py`
- `external_verifier/verify_receipt.py`
- `external_verifier/verify_audit_chain.py`
- `external_verifier/verify_no_bind.py`
- `external_verifier/verify_replay.py`
- `tests/test_digest_manifest.py`

Phase 3 pass conditions:

- every review-bundle artifact has a recomputed SHA-256 digest
- receipt verification fails on tamper
- audit-chain verification fails on tamper
- replay verification fails on mismatch
- external verifier returns a clear pass/fail result without starting the app

Expected verifier success output:

```text
RESULT: ELYRIA ADMISSION RUNTIME VERIFIER PASS
```

## Phase 4 — Production Boundary and CI Proof Gates

Goal: show that production mode fails closed until required controls are present.

Required additions:

- `PRODUCTION_PREFLIGHT.md`
- `SECURITY_POSTURE.md`
- `DEPLOYMENT_SECURITY_CHECKLIST.md`
- `THREAT_MODEL.md`
- `FRESH_CLONE_REVIEW_TEST.md`
- `src/consequence_twin/preflight.py`
- `tests/test_production_preflight.py`
- `.github/workflows/review-bundle.yml`
- `.github/workflows/security.yml`

Phase 4 pass conditions:

- production mode refuses to start without required controls
- CI runs unit tests, digest verification, verifier checks, and production preflight review mode
- fresh-clone test evidence is recorded
- main branch shows green verification status

## Final A+ Gate

The repo reaches bounded A+ buyer-review candidate status only when all of the following are true:

- RBAC tests pass
- tenant isolation tests pass
- signing adapter tests pass
- audit-ledger tamper tests pass
- receipt-store tests pass
- policy-pack tests pass
- no-bind proof tests pass
- route-closure tests pass
- same-condition replay tests pass
- changed-condition replay tests pass
- digest manifest verification passes
- external verifier passes
- production preflight fails closed when incomplete
- fresh-clone review test passes
- GitHub Actions are green on main
- release tag is published

## Final Buyer Classification After Upgrade

```text
Elyria Admission Runtime is an A+ bounded buyer-review consequence-admission runtime candidate. It demonstrates pre-consequence authority, standing, evidence, custody, admissibility, refusal/no-bind behavior, route closure, signed receipts, replay verification, tamper-evident audit chain, digest verification, external verifier review, and production preflight. It is not production-certified until customer security approval or external audit.
```
