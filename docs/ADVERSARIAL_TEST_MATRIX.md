# Adversarial Test Matrix

This matrix defines the minimum hostile cases for a consequence-admission runtime.

| Attack / fault | Required result |
|---|---|
| forged evidence with valid schema | REFUSE or HOLD; never ADMIT |
| revoked authority | REFUSE |
| expired standing | REFUSE or REVALIDATE; never inherited ADMIT |
| changed governing state after admission | revalidation required; stale admission cannot bind |
| replay with modified request | replay fails |
| replay with modified governing basis | replay fails or decision basis changes |
| receipt mutation | integrity verification fails |
| signer identity mismatch | refuse signed authority |
| duplicate one-time authority consumption | second consumption refused |
| missing custody basis | HOLD/REFUSE according to corridor law |
| contradictory evidence | fail closed |
| bypass attempt around gate | protected effect remains unreachable |
| partial authority/quorum | no execution authority |
| clock/freshness failure | fail closed or require revalidation |

## Required assertion

A hostile input must not create a protected effect merely because the request is syntactically valid.

## Evidence rule

An adversarial test passes only when the observed runtime result, receipt, and protected-state behavior agree with the expected fail-closed outcome.