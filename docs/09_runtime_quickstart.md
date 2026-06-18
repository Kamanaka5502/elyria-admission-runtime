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

## Run Docker Sandbox

```bash
docker compose up --build
```

## Reset Demo Data

```bash
curl -X POST http://localhost:8080/sandbox/reset
```

## Load Exposure Graph

```bash
curl http://localhost:8080/exposures/demo
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
movement intake -> deterministic verdict -> receipt -> storage -> replay check -> exposure graph -> dashboard
```
