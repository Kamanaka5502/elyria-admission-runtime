# Production Deployment Notes

This repo is production-shaped, but live deployment requires a chosen provider and credentials.

## Runtime Modes

```text
ELYRIA_MODE=demo
```

Demo mode keeps the sandbox open for public-safe review.

```text
ELYRIA_MODE=client
```

Client mode requires bearer-token authorization for protected operational endpoints.

## Required Production Settings

- HTTPS termination
- managed database instead of local SQLite
- signed receipt secret stored in a secrets manager
- backup and retention policy
- admin authentication
- role-based access
- immutable receipt storage
- monitoring and alerting

## Environment Variables

```text
ELYRIA_MODE=client
ELYRIA_DB_PATH=/data/elyria.db
ELYRIA_STORAGE_BACKEND=sqlite
ELYRIA_API_TOKEN=<set-in-secret-manager>
ELYRIA_RECEIPT_SIGNING_SECRET=<set-in-secret-manager>
```

For managed production deployment, set:

```text
ELYRIA_STORAGE_BACKEND=postgres
```

The current executable sandbox uses SQLite. Postgres is the production storage boundary and should be wired to managed infrastructure before client data enters the system.

## Auth Header

Client mode protected requests must include a bearer authorization header.

Protected endpoints:

```text
POST /movements/assess
GET  /receipts
GET  /receipts/{receipt_id}
POST /receipts/{receipt_id}/replay
```

## Signed Receipts

Receipts include:

```text
signature_algorithm=HMAC-SHA256
signature=<hex digest>
```

Replay verification checks input hash, verdict basis, and receipt signature.

## Minimal Container Runtime

The container starts the API and dashboard together:

```bash
docker build -t elyria-consequence-twin .
docker run -p 8080:8080 \
  -e ELYRIA_MODE=client \
  -e ELYRIA_DB_PATH=/data/elyria.db \
  elyria-consequence-twin
```

## Provider Targets

Good first deployment targets:

- Render
- Fly.io
- Railway
- AWS ECS/Fargate
- Google Cloud Run

## Production Boundary

The current sandbox is demo-grade and public-safe. Client mode adds an auth gate and signed receipts, but protected client material should not enter the system until managed database, secret storage, monitoring, retention, and access-control policies are active.
