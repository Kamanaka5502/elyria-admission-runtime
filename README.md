<p align="center">
  <img src="assets/consequence-exposure-graph.svg" alt="Elyria Consequence Exposure Graph" width="100%" />
</p>

# Elyria Consequence Twin

**Consequence admission before execution binds.**

Elyria Consequence Twin is a working governance sandbox for classifying consequence-bearing movement, attaching evidence references, emitting signed receipts, verifying replay basis, and exposing black-path execution risk before action becomes operationally real.

It answers a stricter operational question than ordinary workflow, risk, GRC, process-mining, or AI-governance software:

> Can this action become real right now, under valid authority, active standing, sufficient evidence, preserved custody, refusal logic, receipt, and replay proof?

## Current Runtime Status

```text
v0.7 Evidence Attachment Layer
client mode authentication
custom movement intake
structured evidence references
signed receipt envelope
receipt replay verification
current stored exposure graph
proof packet export
black-path executive warning
test suite passing locally
```

## What It Proves

Most systems record what happened after execution. Elyria models whether a movement can bind consequence before execution becomes operational reality.

The runtime classifies each movement as:

| Verdict | Color | Meaning |
|---|---|---|
| `ADMIT` | green | movement may bind consequence |
| `HOLD` | yellow | missing or incomplete proof prevents clean admission |
| `REFUSE` | red | movement is blocked by refusal, invalid authority, or inactive standing |
| `NO_PROVABLE_ADMISSION` | black | movement is attempting to become real without durable proof |

The black path is the executive risk surface. It shows where action may bind without valid authority, evidence, custody, receipt, or replay basis.

## Core Runtime Path

```text
movement intake
-> structured evidence references
-> deterministic admission verdict
-> signed receipt
-> SQLite storage
-> replay verification
-> current exposure graph
-> proof packet export
```

## Dashboard Capabilities

The local dashboard includes:

```text
Client Token Panel
Client Movement Intake
Evidence Attachment Layer
Preset Accepted Evidence
Preset Missing Evidence
Preset Black Path
Preset Refusal
Current Stored Graph
Receipt Cards
Replay Receipt
Export Proof Packet
Raw Proof JSON
```

Client mode protects receipt, replay, proof export, sandbox reset, and movement-assessment endpoints behind a bearer token.

## Evidence Attachment Layer

Each client movement can include structured evidence references:

```json
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
```

Receipts include an `evidence_summary` showing:

```text
total evidence items
required evidence count
accepted evidence count
missing evidence count
insufficient evidence count
custody gaps
hash/reference count
source systems
custody owners
evidence status
```

The evidence summary is included inside the signed receipt envelope and verified during replay.

## API Surface

```text
GET  /healthz
POST /movements/assess
GET  /receipts
GET  /receipts/{receipt_id}
POST /receipts/{receipt_id}/replay
GET  /exposures/demo
GET  /exposures/current
GET  /demo/proof
POST /sandbox/reset
```

Protected in client mode:

```text
POST /movements/assess
GET  /receipts
GET  /receipts/{receipt_id}
POST /receipts/{receipt_id}/replay
GET  /exposures/current
GET  /demo/proof
POST /sandbox/reset
```

## Run Locally

```bash
cd elyria-consequence-twin
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8080
```

Open:

```text
http://localhost:8080
```

## Client Mode

```bash
export ELYRIA_MODE=client
export ELYRIA_API_TOKEN="replace-with-local-demo-token"
export ELYRIA_RECEIPT_SIGNING_SECRET="replace-with-local-signing-secret"
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8080
```

In the browser:

```text
enter token
Save Token Locally
Test Protected Access
Reset Sandbox + Generate Receipts
Preset Accepted Evidence or Preset Missing Evidence
Submit Movement + Emit Receipt
Load Current Stored Graph
Load Receipt Cards
Replay Receipt
Export Proof Packet
```

Do not commit or screenshot real tokens, signing secrets, client evidence, private hashes, or live client identifiers.

## Demo Script and Packaging Docs

```text
docs/10_executive_demo_script.md
docs/11_buyer_one_page.md
docs/12_demo_screenshot_and_proof_safety.md
examples/public_demo_proof_packet.example.json
```

## Commercial Offer

### Consequence Twin Scan

A 7-10 day operational diagnostic that maps where AI, workflow, access, approval, payment, deployment, or customer-operation actions may bind consequence without sufficient authority, evidence, custody, standing, receipt, or replay proof.

Deliverables can include:

```text
Consequence Binding Map
Consequence Exposure Graph
Authority Collapse Report
Evidence Gap Register
AI / Workflow Action Exposure Map
Refusal Conditions Matrix
Revalidation Trigger Map
Executive Consequence Risk Brief
Implementation Blueprint
```

## Repository Boundary

This repository is a commercial and technical scaffold. It is not the full private Elyria runtime, private artifact estate, or proprietary proof corridor. It defines the sellable diagnostic surface and a starter implementation lane while preserving deeper runtime IP boundaries.

## Ownership Notice

Copyright (c) Samantha Revita / Elyria Systems. All rights reserved.
