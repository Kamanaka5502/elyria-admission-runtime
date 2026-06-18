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
