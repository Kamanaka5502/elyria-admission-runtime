# Public Release Checklist

## Attribution

```text
Samantha Revita / Elyria Systems
```

## Public release status

This repository may be made public only as a bounded portfolio, buyer-demo, and proof-surface repository.

It must not be described as:

```text
production-certified
customer-certified
regulated compliance approval
protected Elyria / Veritas kernel disclosure
substrate proof by itself
legal, medical, financial, or security certification
```

Correct public framing:

```text
Full-stack proof surface, not production certification.
Universal architecture layer, bounded public repo claim.
Samantha Revita / Elyria Systems.
```

## Required checks before making public

Confirm:

- no real API tokens
- no real signing secrets
- no customer data
- no medical, financial, HR, legal, or regulated data
- no private hashes or production proof packets
- no live client identifiers
- no private evidence documents
- no protected kernel internals
- no outside personal names that should not be attached
- no `.env` file committed
- no database file with real data committed
- no permissive license added unless reuse is intentional

## Public-safe files

The following file types are acceptable for public release when sanitized:

```text
README.md
CLAIM_BOUNDARY.md
FULL_STACK_SCOPE.md
REVIEWER_QUICKSTART.md
BUYER_READOUT.md
PROOF_OR_DEMO_PATH.md
LIMITATIONS.md
PROPRIETARY_NOTICE.md
source code using demo values
example proof packets using sanitized demo values
tests using synthetic values
```

## Demo boundary

Demo secrets and placeholder values are acceptable only when clearly marked as placeholders.

Production credentials, customer credentials, and operational signing secrets must never be committed.

## License boundary

No license is granted by default.

The absence of a license file means public viewers may inspect the repository, but no reuse, copying, modification, sublicensing, training, selling, or derivative commercial work is granted unless Samantha Revita / Elyria Systems provides express written permission.

## Final pre-public statement

```text
This repository is a public proof surface for review and commercial positioning.
It is not a grant of rights, production certification, or disclosure of protected Elyria internals.
```
