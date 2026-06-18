# Reviewer Quickstart

## Fresh Clone Path

```bash
git clone https://github.com/Kamanaka5502/elyria-consequence-twin.git
cd elyria-consequence-twin
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest tests
```

Expected:

```text
RESULT: PASS
```

The local test count may increase over time. The required standard is that the full test suite passes from a fresh clone after dependency installation.

## Run Dashboard

```bash
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8080
```

Open:

```text
http://localhost:8080
```

Expected:

```text
Dashboard loads.
Demo graph loads.
Sandbox reset emits receipts.
Receipt cards render.
Replay verification works.
Proof packet export works.
```

## Client Mode Path

```bash
export ELYRIA_MODE=client
export ELYRIA_API_TOKEN="local-demo-token-only"
export ELYRIA_RECEIPT_SIGNING_SECRET="local-demo-signing-secret-only"
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8080
```

Browser path:

```text
1. Enter local demo token.
2. Click Save Token Locally.
3. Click Test Protected Access.
4. Click Reset Sandbox + Generate Receipts.
5. Click Preset Accepted Evidence.
6. Click Submit Movement + Emit Receipt.
7. Click Preset Black Path.
8. Click Submit Movement + Emit Receipt.
9. Click Load Current Stored Graph.
10. Click Load Receipt Cards.
11. Click Replay Receipt.
12. Click Export Proof Packet.
```

Expected protected-access result:

```text
Protected access OK.
```

Expected replay result:

```text
input_hash_matches: true
verdict_matches: true
signature_matches: true
evidence_summary_matches: true
```

## Reviewer Boundary

Do not treat local demo secrets, demo signatures, or sample proof packets as production proof.

A reviewer should verify:

```text
claim boundary exists
tests pass
client-mode token gate works
movement intake works
evidence summary appears in receipt
receipt replay verifies
black-path warning appears for unprovable movement
proof packet exports without protected client data
```
