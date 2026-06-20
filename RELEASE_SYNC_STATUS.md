# Release Sync Status

## Current Main

```text
status: verified buyer-review runtime candidate
CI evidence: recorded
final buyer-review gate: complete
```

## Existing Release

```text
tag: v0.8.1-public
role: historic public release marker
relationship to current main: predates current verification surface
```

## Next Immutable Release

```text
tag: v0.8.2-public
target: current main
title: Elyria Admission Runtime v0.8.2 — Verified Buyer-Review Release
release notes: RELEASE_NOTES_V0_8_2_VERIFIED.md
```

## Why This Exists

A release tag should identify an immutable snapshot. The current verification evidence is on `main`, so the buyer-review release must be synchronized to the current verified branch before it is represented as the current release snapshot.
