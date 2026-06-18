# Proof or Demo Path

## Purpose

This file gives a reviewer one clean path to see the repository's bounded proof claim in action.

## Bounded proof claim

```text
A client-entered movement can be assessed before consequence binds, attached to structured evidence references, emitted as a signed receipt, replay-verified, and rendered into a consequence exposure graph.
```

## Demo path

### 1. Start runtime

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8080
```

Open:

```text
http://localhost:8080
```

### 2. Reset sandbox

Click:

```text
Reset Sandbox + Generate Receipts
Load Receipt Cards
```

Expected baseline:

```text
MOVE-001 -> ADMIT -> green
MOVE-002 -> NO_PROVABLE_ADMISSION -> black
MOVE-003 -> REFUSE -> red
```

### 3. Prove accepted evidence path

Click:

```text
Preset Accepted Evidence
Submit Movement + Emit Receipt
Load Current Stored Graph
Load Receipt Cards
```

Expected:

```text
new client movement appears
verdict: ADMIT
color: green
signature_algorithm: HMAC-SHA256
evidence_summary.status: supporting
```

### 4. Prove black-path failure case

Click:

```text
Preset Black Path
Submit Movement + Emit Receipt
Load Current Stored Graph
Load Receipt Cards
```

Expected:

```text
verdict: NO_PROVABLE_ADMISSION
color: black
black_paths increases
evidence_summary.status: attention_required
missing evidence count > 0
custody gaps > 0
```

### 5. Prove replay

Click:

```text
Replay Receipt
```

Expected:

```text
input_hash_matches: true
verdict_matches: true
signature_matches: true
evidence_summary_matches: true
```

### 6. Export proof packet

Click:

```text
Export Proof Packet
```

Expected proof packet contains:

```text
service metadata
current graph
receipts
signed receipt fields
evidence_summary
proof_claim
```

## Pass/fail standard

Pass:

```text
tests pass
runtime starts
dashboard loads
client movement can be submitted
signed receipt is emitted
black-path failure case is visible
replay verifies
proof packet exports
```

Fail:

```text
tests fail
runtime does not start
protected endpoint opens in client mode without token
movement submission does not emit receipt
replay does not verify
black-path movement is admitted silently
proof packet omits receipt/evidence basis
```
