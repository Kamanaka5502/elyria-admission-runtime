# Portfolio Position — Elyria Admission Runtime

## Flagship Runnable Proof Surface for Pre-Execution Governance

Elyria Admission Runtime is the flagship runnable proof surface within the public Elyria Systems portfolio.

It is the first repository a technical reviewer, prospective customer, hiring panel, or governance evaluator should inspect because it makes the full control corridor visible:

```text
proposed movement
→ authority
→ standing
→ evidence
→ custody / hash basis
→ deterministic verdict
→ signed receipt
→ storage
→ replay verification
→ proof-packet export
```

The runtime does not claim to replace every control surface in the broader architecture. It demonstrates the point where those control surfaces converge:

> **Whether a proposed movement may become operationally real.**

---

## The Category: Pre-Execution Governance

**Pre-execution governance** determines whether an action may bind consequence before the protected effect occurs.

This runtime expresses that category through four operational verdicts:

| Verdict | Runtime meaning |
|---|---|
| `ADMIT` | authority, standing, evidence, and custody permit the movement to bind |
| `HOLD` | proof is incomplete or repair is required before movement can bind |
| `REFUSE` | an invalid or refusal-bearing condition blocks movement |
| `NO_PROVABLE_ADMISSION` | movement attempts to bind without durable proof |

The point is not to add another approval screen.

The point is to make invalid movement non-binding.

---

## How This Repository Relates to the Portfolio

| Control dimension | Supporting public surface | Relationship to this runtime |
|---|---|---|
| Bind-time authority | [bind-time-authority-proof](https://github.com/Kamanaka5502/bind-time-authority-proof) | Establishes why standing must be evaluated at the boundary where consequence would bind. |
| Revocation | [authority-revocation-witness](https://github.com/Kamanaka5502/authority-revocation-witness) | Demonstrates that a technically executable continuation must still refuse after authority has been revoked. |
| Change and revalidation | [elyria-ai-revalidation-engine](https://github.com/Kamanaka5502/elyria-ai-revalidation-engine) | Shows when changed AI systems invalidate prior approval and require renewed review or refusal. |
| Pre-effect enforcement | [elyria-pre-effect-enforcement-harness](https://github.com/Kamanaka5502/elyria-pre-effect-enforcement-harness) | Provides the enforce-before-effect posture that the admission corridor operationalizes. |
| Action control | [elyria-action-firewall](https://github.com/Kamanaka5502/elyria-action-firewall) | Supports an explicit boundary around actions that should not execute without admitted standing. |
| Evidence / proof register | [elyria-boundary-proof-register](https://github.com/Kamanaka5502/elyria-boundary-proof-register) | Complements receipt, verification, and proof continuity framing. |
| Safe change | [veritas-safechange](https://github.com/Kamanaka5502/veritas-safechange) | Extends the same governance posture to controlled system modification. |

---

## Reviewer Route

1. Run the local verification path in this repository.
2. Submit one admitted movement and one no-provable-admission or refusal-bearing movement.
3. Inspect the signed receipts and replay the decisions.
4. Use the supporting repositories above to trace individual authority, revocation, revalidation, evidence, and change-control dimensions.
5. Review the portfolio index for the full public map: [Elyria Systems — Portfolio Start Here](https://github.com/Kamanaka5502/Samantha-Revita-Elyria-Systems/blob/main/PORTFOLIO_START_HERE.md).

---

## Claim Boundary

This repository is a public, reviewable product/runtime layer. It is not a claim that every protected Elyria / Veritas implementation detail, customer-specific configuration, production key/signing architecture, or private validator is disclosed here.

The public surface is sufficient to inspect the operating thesis:

> **No authority, no standing, no evidence, no custody, no admission.**
>
> **No admission, no binding consequence.**
