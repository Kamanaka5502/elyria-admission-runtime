# Implementation Blueprint

## Governed Corridor

[Describe the bounded consequence path selected for implementation.]

## Objective

Prevent inadmissible movement from binding consequence without valid authority, evidence, custody, standing, receipt, and replay.

## Required Components

| Component | Requirement | Implementation Notes |
|---|---|---|
| Consequence Node Registry | Define all consequence-bearing positions | [Notes] |
| Authority Rule Set | Bind authority to movement and consequence type | [Notes] |
| Evidence Requirements | Define required evidence before bind | [Notes] |
| Custody Controls | Preserve evidence chain across handoffs | [Notes] |
| Refusal Matrix | Define hard blocks | [Notes] |
| Hold Conditions | Define missing-proof state | [Notes] |
| Revalidation Triggers | Force re-check after material changes | [Notes] |
| Receipt Model | Emit durable ADMIT/HOLD/REFUSE receipts | [Notes] |
| Replay Verifier | Reproduce verdict basis later | [Notes] |

## Pilot Acceptance Criteria

- inadmissible movement cannot silently bind
- missing evidence produces HOLD or REFUSE
- refusal reasons are explicit
- authority scope is checked before consequence movement
- receipts are generated for verdicts
- replay can reproduce verdict basis
- black paths are detected or eliminated

## Build Phases

1. Scope lock
2. Node and movement inventory
3. Authority/evidence/custody model
4. Verdict logic
5. Receipt model
6. Replay path
7. Negative testing
8. Executive report
