# Full-Stack System Architecture

Elyria Consequence Twin should evolve from a diagnostic scaffold into a full-stack consequence-admission runtime.

The core question remains:

```text
Can this movement bind consequence right now?
```

## Runtime Stack

### 1. Interface Layer

- executive dashboard
- consequence exposure graph
- movement intake workspace
- authority review view
- evidence gap register
- refusal matrix view
- receipt and replay viewer

### 2. API Layer

Core API surface:

```text
POST /movements/assess
POST /graphs/build
POST /receipts/verify
POST /replay/run
GET  /exposures/{graph_id}
GET  /movements/{movement_id}
```

The API receives an attempted movement and sends it through deterministic assessment before any protected effect is treated as admitted.

### 3. Engine Layer

Engine modules:

- movement normalizer
- authority resolver
- standing checker
- evidence validator
- custody verifier
- refusal evaluator
- revalidation evaluator
- verdict emitter
- receipt generator
- replay packet builder

Verdicts:

```text
ADMIT
HOLD
REFUSE
NO_PROVABLE_ADMISSION
```

### 4. Authority Layer

Authority is modeled as bind-time standing, not a generic role label.

Objects:

- authority grant
- scope
- expiration
- revocation
- delegation
- policy reference
- actor reference

Collapse conditions:

- missing authority
- stale authority
- out-of-scope authority
- inherited authority without proof
- authority detached from evidence

### 5. Evidence and Custody Layer

Evidence must exist before consequence binds.

Objects:

- source record
- approval record
- policy version
- model version
- input snapshot
- workflow state
- operator rationale
- system event reference

Custody fields:

- owner
- source
- timestamp
- hash
- handoff chain
- retention rule

### 6. Exposure Graph Layer

The exposure graph renders movement as consequence-bearing paths.

```text
Green  = admissible
Yellow = hold / missing proof
Red    = refused
Black  = no provable admission
```

Black paths remain the executive risk surface.

### 7. Receipt and Replay Layer

Each verdict should produce a durable receipt.

Receipt fields:

- receipt id
- movement id
- verdict
- reason codes
- authority reference
- evidence references
- custody references
- engine version
- input hash
- timestamp
- replay pointer

Replay must reproduce the verdict basis without relying on memory or informal explanation.

### 8. Adapter Layer

Adapters connect external systems without absorbing their authority.

Pattern:

```text
external system emits event
Elyria evaluates admission
external system receives verdict
protected effect binds only when admitted
```

### 9. Data Layer

Minimum persistence model:

```text
movements
authority_grants
evidence_references
custody_chains
verdicts
receipts
replay_packets
consequence_nodes
consequence_edges
exposure_findings
revalidation_triggers
```

### 10. Observability Layer

Operational metrics:

```text
black_path_count
unreplayable_decision_count
authority_collapse_count
evidence_gap_count
refusal_enforcement_count
admission_coverage_percent
```

## Build Sequence

### Phase 0: Diagnostic Surface

Current state: methodology, commercial packet, templates, schemas, examples, starter engine, tests.

### Phase 1: Local Runtime Prototype

Build:

- API service
- database schema
- deterministic engine service
- receipt generator
- graph builder
- local dashboard

Acceptance:

- movement enters API
- verdict is generated
- receipt is stored
- graph updates
- replay reproduces basis

### Phase 2: Pilot Corridor

Build one governed corridor from movement intake through verdict, receipt, graph update, and replay.

Acceptance:

- missing evidence becomes HOLD
- authority collapse becomes REFUSE
- missing receipt or replay becomes BLACK
- admissible movement becomes GREEN

### Phase 3: Enterprise Twin

Expand from one corridor to multiple operational paths, integrations, graph views, and executive reporting.

## Target Monorepo Structure

```text
apps/
  dashboard/
  api/
packages/
  engine/
  schemas/
  graph/
  receipts/
  adapters/
docs/
commercial/
templates/
examples/
tests/
```

## Boundary

Execution is not assumed. It is admitted.

Nothing persists without validation.

Truth must be replayable.

No motion binds without dimensional coherence.
