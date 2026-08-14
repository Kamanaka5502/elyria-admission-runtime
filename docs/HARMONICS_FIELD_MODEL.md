# Elyria Harmonics Field Model

## Purpose

Harmonics is the deterministic coherence layer for a proposed movement. It does not replace admission. It resolves whether the movement's governing dimensions remain mutually compatible before consequence can bind.

## Coherence dimensions

```text
intent_context
 evidence
 authority
 state
```

The evaluator produces:

- `alignment_score` in `[0, 1]`
- a per-dimension `coherence_vector`
- deterministic `conflicts`
- deterministic `warnings`
- evidence and authority roots

## Enforcement

Any conflict produces an alignment score of `0.0` and must be resolved by the admission layer as non-admission. Warnings remain visible and replayable but do not silently override a conflict.

## Replay rule

The evaluator is deterministic over the canonicalized movement inputs, evidence, authority, field context, state basis, delta basis, and explicit evaluation time. The same governed inputs must produce the same harmonic resolution.

## Time

Evaluation time is part of the governed context. Replay must use the recorded evaluation time rather than wall-clock time. This prevents time drift from changing historical conclusions.

## Boundary

Harmonics is a resolving surface, not an authority source. It cannot sign, execute, or manufacture evidence. Its output is consumed by the admission boundary.
