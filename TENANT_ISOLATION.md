# Tenant Isolation Boundary

## Purpose

Elyria Admission Runtime must be able to prove that tenant-scoped movement, receipt, replay, proof, and audit material cannot silently cross customer boundaries.

This file defines the Phase 1 tenant isolation posture.

## Required Tenant Field

Every production-scoped material object should carry:

```text
tenant_id
```

Applies to:

- movement input
- receipt
- replay request
- audit event
- proof packet
- external verifier bundle

## Fail-Closed Rule

In production mode, missing `tenant_id` is invalid.

```text
missing tenant_id → refuse / forbidden / fail closed
blank tenant_id   → refuse / forbidden / fail closed
cross-tenant read → refuse / forbidden / fail closed
```

## Cross-Tenant Protection

Tenant A must not be able to:

- read tenant B movement
- replay tenant B receipt
- export tenant B proof packet
- inspect tenant B audit chain
- verify tenant B protected bundle without explicit authorization

## A+ Pass Condition

Tests must prove tenant filtering and cross-tenant denial.

Implemented proof file:

```text
tests/test_tenant_isolation.py
```
