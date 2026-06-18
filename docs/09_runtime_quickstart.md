# Runtime Quickstart

## Install

```bash
make install
```

## Run Tests

```bash
make test
```

## Run API and Dashboard

```bash
make api
```

Open:

```text
http://localhost:8080
```

## Dashboard Client Token Panel

The dashboard includes a **Client Token Panel**.

- Demo mode works without a token.
- Client mode requires a token for protected endpoints.
- The token is stored only in the browser local storage.
- The dashboard sends the token with protected requests.
- Use **Clear Token** before screenshots or public demos.

## Client Movement Intake

The dashboard includes **Client Movement Intake**.

Use it to enter a movement and emit a signed receipt. The submitted movement is stored, rendered in receipt cards, and included in the current exposure graph.

Recommended browser flow:

```text
Save Token Locally if running in client mode
Submit Movement + Emit Receipt
Load Current Stored Graph
Load Receipt Cards
Replay Receipt
Export Proof Packet
```

Use **Preset Black Path** or **Preset Refusal** to quickly demonstrate negative consequence controls.

## Evidence Attachment Layer

The dashboard includes structured evidence references.

Each movement may include `evidence_items` with:

```text
evidence_id
evidence_type
source_system
custody_owner
hash_reference
required
status
notes
```

The receipt includes an `evidence_summary` with counts for required, accepted, missing, insufficient, custody gaps, and hash references. The evidence summary is included in the signed receipt envelope and checked during replay.

Use **Preset Accepted Evidence** for a clean admission surface, or **Preset Missing Evidence** to show evidence/custody failure before consequence binds.

## Run Docker Sandbox

```bash
docker compose up --build
```

## Reset Demo Data

```bash
curl -X POST http://localhost:8080/sandbox/reset
```

## Load Demo Exposure Graph

```bash
curl http://localhost:8080/exposures/demo
```

## Load Current Stored Graph

```bash
curl http://localhost:8080/exposures/current
```

## Submit Movement by API

```bash
curl -X POST http://localhost:8080/movements/assess \
  -H "Content-Type: application/json" \
  -d '{
    "movement_id": "CLIENT-001",
    "source_node": "client.workflow",
    "target_node": "protected.action",
    "authority_present": true,
    "authority_scope_valid": true,
    "standing_active": true,
    "evidence_present": true,
    "evidence_sufficient": true,
    "custody_preserved": true,
    "refusal_condition_active": false,
    "revalidation_required": false,
    "receipt_available": true,
    "replay_available": true,
    "notes": "Client-entered movement.",
    "evidence_items": [
      {
        "evidence_id": "EV-CLIENT-001",
        "evidence_type": "policy_record",
        "source_system": "client.governance.registry",
        "custody_owner": "operations.owner",
        "hash_reference": "sha256:client-demo-reference",
        "required": true,
        "status": "accepted",
        "notes": "Required evidence reference for this movement."
      }
    ]
  }'
```

## Export Demo Proof Packet

```bash
curl http://localhost:8080/demo/proof > local_artifacts/demo_proof/elyria-consequence-twin-demo-proof.json
```

The dashboard also includes an **Export Proof Packet** button that downloads the current demo proof packet as JSON.

## CLI Commands

```bash
python -m consequence_twin.cli assess examples/sample_assessments.json
python -m consequence_twin.cli graph examples/sample_assessments.json
python -m consequence_twin.cli store examples/sample_assessments.json --db data/elyria.db
```

The runtime path is:

```text
movement intake -> structured evidence references -> deterministic verdict -> signed receipt -> storage -> replay check -> current exposure graph -> dashboard
```
