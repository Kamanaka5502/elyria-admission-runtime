from __future__ import annotations

from .settings import get_settings


def describe_storage_backend() -> dict[str, str]:
    settings = get_settings()
    backend = settings.storage_backend
    if backend == "sqlite":
        return {
            "backend": "sqlite",
            "status": "active",
            "path": settings.db_path,
        }
    if backend == "postgres":
        return {
            "backend": "postgres",
            "status": "configured_boundary",
            "note": "Postgres mode is reserved for managed production deployment. SQLite remains the executable sandbox backend in this release.",
        }
    return {
        "backend": backend,
        "status": "unsupported",
        "note": "Set ELYRIA_STORAGE_BACKEND to sqlite or postgres.",
    }
