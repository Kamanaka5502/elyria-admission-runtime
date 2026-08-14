# Security Boundary

## Reporting

Report suspected vulnerabilities privately before public disclosure.

## Security properties expected of the runtime

- protected effects require an admitted boundary result;
- non-admitted verdicts do not authorize effect;
- receipt inputs and governing basis are integrity-bound;
- replay verifies the original decision basis;
- stale, revoked, incomplete, contradictory, or unverifiable authority/evidence fails closed;
- production signing custody is separated from the admission resolver;
- public artifacts contain no live credentials or customer data.

## Non-claims

This repository does not claim that a local test suite proves complete security, production certification, or safety for a particular customer environment. Those properties require independent assessment and deployment-specific evidence.