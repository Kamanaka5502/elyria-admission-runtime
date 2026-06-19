# Claim Boundary

## This repo claims

This repo demonstrates a bounded full-stack consequence-admission runtime and buyer-facing product scaffold for Elyria's universal consequence-governance architecture.

It proves that a consequence-bearing movement can be:

- entered through a client-facing dashboard
- submitted through an API layer
- evaluated against authority, standing, evidence, custody, refusal, receipt, and replay dimensions
- classified into `ADMIT`, `HOLD`, `REFUSE`, or `NO_PROVABLE_ADMISSION`
- attached to structured evidence references
- summarized into an evidence basis
- emitted as a signed receipt
- stored in a local receipt store
- replay-verified against the stored verdict basis
- rendered into a current consequence exposure graph
- exported as a proof packet
- tested through a local reviewer path

## This repo does not claim

- It does not expose protected Elyria / Veritas kernel internals.
- It does not claim production certification unless externally certified.
- It does not claim customer-specific certification without customer corridor verification.
- It does not claim universal governance proof by itself.
- It does not claim substrate status.
- It does not claim deployment readiness without security review.
- It does not replace regulated legal, medical, financial, security, or compliance review.

## Architecture posture

Elyria is universal at the architecture layer.

This repository is bounded at the public runtime/product-demo layer.

The public claim is conservative: this repo demonstrates one full-stack consequence-admission runtime scaffold within the larger Elyria consequence-governance architecture.

## Full-stack boundary

Full-stack means the repo contains a working local chain from interface to proof artifact:

```text
frontend dashboard
API layer
admission engine
evidence summary layer
signed receipt runtime
local storage
replay verifier
exposure graph
proof packet export
tests
buyer/reviewer documentation
```

Full-stack does not mean production certification, protected kernel disclosure, or substrate status.

## Core invariant

Proof before operation.  
Claim boundary before promotion.  
No protected consequence binds without the boundary result.
