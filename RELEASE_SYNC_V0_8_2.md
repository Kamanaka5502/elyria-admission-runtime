# Release Sync v0.8.2

## Purpose

The verified buyer-review runtime is on current `main`.

The existing `v0.8.1-public` tag remains valid as historical release metadata, but it predates the current verification evidence, proof-gate layers, and buyer-review documentation.

This release sync creates an immutable release reference for the verified current-main snapshot.

## Recommended Values

```text
tag: v0.8.2-public
target: main
title: Elyria Admission Runtime v0.8.2 — Verified Buyer-Review Release
```

## Release Description

```text
Verified buyer-review release of Elyria Admission Runtime.

This release captures the current full-stack consequence-admission runtime on main, including deterministic verdicting, structured evidence gates, signed receipts, replay verification, exposure graphing, policy-pack review, no-bind proof, route closure, changed-condition replay, external verifier review, digest manifest verification, production preflight review mode, and recorded CI proof-gate evidence.

Recorded CI evidence: ci #155, proof-gates successful, verification-report artifact passed.

This release is public for buyer review and portfolio inspection under the repository's proprietary source-available license. Production deployment remains subject to customer approval and external review where required.
```

## Publication Steps

1. Open **Releases** in the repository.
2. Choose **Draft a new release**.
3. Create/select `v0.8.2-public` from `main`.
4. Use the title and description above.
5. Publish the release.
6. Record the release URL in the release-sync issue.

## Boundary

```text
current main: verified buyer-review runtime candidate
new tag: immutable public review snapshot
production deployment: separate customer-controlled step
```
