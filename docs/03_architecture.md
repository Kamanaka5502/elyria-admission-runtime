# Architecture

## Core Objects

### Consequence Node

A node is a consequence-bearing position, not merely a person, role, application, or process step.

Examples:

```text
AI recommendation
operator approval
payment release
customer escalation
data access
model update
workflow override
vendor handoff
policy exception
system deployment
```

### Consequence Edge

An edge is an attempted movement from one consequence-bearing position to another.

Each edge must answer:

```text
Can this movement bind consequence?
What authority admits it?
What evidence supports it?
What custody must hold?
What standing can expire?
What refusal condition blocks it?
What receipt proves it?
What replay verifies it?
```

## Consequence Exposure Graph

The graph classifies every relevant movement path:

| Color | Meaning |
|---|---|
| Green | admissible consequence path |
| Yellow | hold / missing evidence |
| Red | refused / no standing |
| Black | consequence path with no lawful or provable admission |

## Runtime Direction

The diagnostic scaffold can become a runtime layer through:

1. consequence-node inventory
2. authority model
3. evidence model
4. custody model
5. refusal matrix
6. revalidation triggers
7. receipt generation
8. replay verifier
9. implementation corridor

## Minimal Pilot Surface

A pilot should prove:

- deterministic verdicts
- explicit refusal reasons
- no silent admission
- evidence requirements before movement
- receipt generation for ADMIT/HOLD/REFUSE
- replayable decision path
- black-path detection
