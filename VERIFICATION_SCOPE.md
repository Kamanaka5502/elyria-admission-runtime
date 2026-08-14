# Verification Scope

This repository is a bounded, reviewable admission-runtime surface.

## Admission invariant

A movement may bind operational consequence only when authority, standing, required evidence, custody/proof basis, and the configured admission law all resolve admissibly at the boundary.

## Replay invariant

Replay must reconstruct the original verdict against the same request and governing basis. Changed governing inputs must invalidate inherited admission or produce a changed proof basis.

## Effect invariant

`HOLD`, `REFUSE`, and `NO_PROVABLE_ADMISSION` do not authorize protected effect.

## Security boundary

The public runtime is production-oriented but not production-certified. Production use requires environment-specific authentication, authorization, key management, policy mapping, evidence provenance, logging/retention, deployment hardening, independent review, and operational acceptance evidence.

## Claim discipline

Repository status is bounded by executable evidence. A green local verifier is evidence for the tested surface, not proof of universal or third-party certification.