# Consequence Twin Scan

## Offer

A 7–10 day operational diagnostic that maps where AI, workflow, access, approval, payment, deployment, or customer-operation actions may bind consequence without sufficient authority, evidence, custody, standing, or replay.

## What the Scan Finds

The scan identifies:

- where action can become operationally real
- where authority is assumed instead of proven
- where evidence is missing before consequence binds
- where custody breaks across systems or teams
- where approval exists but standing has expired or is unclear
- where AI/workflow outputs influence consequence without admission gates
- where refusal conditions are undefined or unenforced
- where revalidation is missing after material standing changes
- where receipts are insufficient for replay
- where black paths exist

## Inputs Requested

The scan can begin from limited materials. The client may provide:

- workflow diagrams
- approval matrices
- policy documents
- system diagrams
- access-control descriptions
- AI/model use cases
- incident examples
- release/deployment process notes
- customer escalation paths
- payment/release/authorization procedures
- logs or redacted examples
- known exceptions and override paths

## Output Standard

Each finding should identify:

```text
movement -> consequence -> authority -> evidence -> custody -> verdict -> failure mode -> remediation path
```

## Boundary

The diagnostic does not replace legal advice, regulated compliance certification, clinical judgment, financial advice, or security audit obligations. It identifies consequence-admission exposure and implementation requirements.
