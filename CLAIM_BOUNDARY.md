# Claim Boundary

## What this public repository demonstrates

This repository demonstrates a bounded public pilot for consequence-admission assessment. It can accept a movement payload, classify caller-supplied assessment dimensions, summarize supplied structured evidence, create a signed receipt, persist the record, and replay-check the recorded assessment.

The configured verdicts are:

- `ADMIT`
- `HOLD`
- `REFUSE`
- `NO_PROVABLE_ADMISSION`

The public pilot now fails closed when no structured evidence attachments are supplied: favorable caller-supplied Boolean fields alone are not enough to produce `ADMIT`.

## What this repository does not independently establish

This repository does not, by itself:

- derive standing from an authoritative mathematical Floor;
- independently verify the provenance or truth of caller-supplied standing and authority assertions;
- authenticate the underlying evidence merely because an attachment has an accepted status or a hash/reference string;
- prove exclusive control over every route to an external protected effect;
- prove that an external consequence did or did not commit;
- establish universal governance proof, substrate status, or production certification.

An HMAC-authenticated receipt can support integrity and authenticity of the signed record relative to the shared secret. It does not make the record's premises true. Deterministic replay can show that the same recorded input yields the same assessment; it is not independent verification of the input's truth.

## Evidence gate behavior

The configured behavior is:

- no structured evidence attachments: `NO_PROVABLE_ADMISSION` when authority and standing are asserted as potentially binding; otherwise the missing-evidence hold/refusal logic applies;
- structured evidence with required items missing, insufficient, or lacking required custody/hash-reference fields: non-admission according to the engine's configured refusal/black-path/hold precedence;
- structured evidence with acceptable fields: `ADMIT` remains possible, subject to the other caller-supplied dimensions.

A hash/reference field is a reference, not proof that the referenced content is authentic or authoritative. An accepted status is a classification supplied in the record, not independent validation of the source.

## Standing and effect boundary

The public API accepts standing and other dimensions as caller-supplied fields. Type-checking a Boolean is not provenance verification. A trusted standing mechanism would require a separately specified authority model and verification procedure, including scope, validity, revocation, and binding to the exact transition.

The inspected public API demonstrates an assessment and receipt path, not exclusive custody of an external operation. Claims about pre-effect enforcement or protected consequences require separate, explicit evidence for the relevant effect boundary.

## Scope and limitations

This is a bounded public runtime/pilot, not the full private Elyria runtime. Separate repositories or harnesses must not be treated as one integrated chain without evidence of integration. Tests establish only the software behaviors they actually exercise.

Production use requires independent security review, appropriate key management, customer-specific policy and evidence mapping, and operational validation.

## Public claim

The repository demonstrates a bounded consequence-admission assessment pilot with structured-evidence gating, signed assessment receipts, persistence, and replay checks. It does not independently prove the truth of caller assertions, constitutive standing, or exclusive control over external protected consequences.
