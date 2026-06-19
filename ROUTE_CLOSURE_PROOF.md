# Route Closure Proof

## Purpose

Route closure proof records whether the protected execution path is open or closed after a runtime verdict.

A held, refused, or no-provable-admission movement should close the protected route and prevent downstream consequence activation.

## Route State

```text
ADMIT                 → route may open
HOLD                  → route closed
REFUSE                → route closed
NO_PROVABLE_ADMISSION → route closed
```

## A+ Pass Condition

Tests prove:

- held route closes
- refused route closes
- downstream path remains not activated
- refused movement cannot later be exported as admitted without a new changed-condition receipt

Implemented proof file:

```text
tests/test_route_closure.py
```
