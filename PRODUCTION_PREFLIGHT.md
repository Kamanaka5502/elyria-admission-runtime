# Production Preflight

## Purpose

Production preflight prevents Elyria Admission Runtime from presenting an incomplete production posture as ready.

Review mode may pass while still listing missing production controls. Production mode must fail closed until all required controls are enabled.

## Required Production Controls

```text
auth_enabled
rbac_enabled
tenant_isolation_enabled
persistent_receipt_store_enabled
audit_ledger_enabled
non_demo_signing_enabled
policy_pack_loaded
external_verifier_bundle_generated
runtime_environment_marker_present
debug_mode_disabled
```

## Commands

Review mode:

```bash
python scripts/production_preflight.py --mode review
```

Production mode:

```bash
python scripts/production_preflight.py --mode production --config path/to/config.json
```

## Boundary

Passing review mode does not mean production certification.

Production readiness requires customer review, deployment review, signing custody review, enterprise identity, tenant isolation approval, and applicable external review.

Implemented proof file:

```text
tests/test_production_preflight.py
```
