# Auth / RBAC Boundary

## Purpose

Elyria Admission Runtime now includes a bounded role-based authorization model for buyer-review hardening.

This is not an enterprise identity provider. It is the runtime authorization surface that defines which role may perform which admission, receipt, replay, proof, and audit actions.

## Roles

```text
viewer
operator
reviewer
admin
auditor
external_verifier
```

## Permission Model

| Role | Intended Access |
|---|---|
| `viewer` | read dashboard only |
| `operator` | read dashboard and submit movement |
| `reviewer` | inspect receipts, verify proof, issue review verdict |
| `admin` | configure runtime and inspect audit material, but cannot silently bypass admission |
| `auditor` | inspect receipts, audit chain, and proof verification |
| `external_verifier` | verify proof packet only |

## Non-Bypass Rule

Admin does not mean admission bypass.

```text
admin may configure runtime
admin may inspect receipts and audit chain
admin may not silently issue admission
admin may not silently mutate receipts
admin may not bypass the deterministic admission engine
```

## A+ Pass Condition

Tests must prove unauthorized users cannot:

- submit movement without permission
- issue admission without permission
- inspect protected receipt material without permission
- export proof packets without permission
- bypass review state

Implemented proof file:

```text
tests/test_auth_rbac.py
```
