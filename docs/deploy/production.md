# Production Deployment Notes

This repo is production-shaped, but live deployment requires a chosen provider and credentials.

## Required Production Settings

- HTTPS termination
- managed database instead of local SQLite
- signed receipt secret stored in a secrets manager
- backup and retention policy
- admin authentication
- role-based access
- immutable receipt storage
- monitoring and alerting

## Minimal Container Runtime

The container starts the API and dashboard together:

```bash
docker build -t elyria-consequence-twin .
docker run -p 8080:8080 -e ELYRIA_DB_PATH=/data/elyria.db elyria-consequence-twin
```

## Provider Targets

Good first deployment targets:

- Render
- Fly.io
- Railway
- AWS ECS/Fargate
- Google Cloud Run

## Production Boundary

The current sandbox is a demo-grade runtime. For client production use, replace local SQLite with a managed database and add authentication before exposing protected client material.
