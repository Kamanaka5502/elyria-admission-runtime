# No-Bind Proof

## Purpose

No-bind proof records that a movement did not become admitted consequence.

A refused, held, or no-provable-admission movement should produce a proof artifact showing:

```text
movement attempted
reason admission failed
missing or invalid standing condition
blocked consequence path
route closure state
receipt reference
replay reference
downstream effect status
```

## Runtime Rule

A non-admitted movement must not be described only as a rejected request. It should carry proof that the protected consequence path did not activate.

## A+ Pass Condition

Tests prove:

- non-admitted movement emits no-bind proof
- no-bind proof records closure state
- downstream effect remains not activated
- admitted movement cannot emit no-bind proof

Implemented proof file:

```text
tests/test_no_bind.py
```
