# Changed-Condition Replay

## Purpose

Changed-condition replay records when a movement is re-evaluated under changed evidence, authority, scope, custody, or policy context.

The original receipt must remain preserved. A changed-condition admission must create a new linked receipt.

## Replay Requirements

Changed replay compares:

```text
original movement
original evidence
original authority
original standing
changed evidence
changed authority
changed scope
changed custody
changed policy pack
resulting verdict
```

## Invariant

```text
same conditions  → same result expected
changed conditions → new linked receipt required
old receipt       → never silently mutated
```

## A+ Pass Condition

Tests prove:

- same-condition replay verifies original receipt
- changed-condition replay identifies changed fields
- changed-condition replay creates a new linked receipt
- old receipt remains preserved

Implemented proof file:

```text
tests/test_changed_condition_replay.py
```
