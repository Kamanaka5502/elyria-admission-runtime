from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeSettings:
    mode: str
    db_path: str
    storage_backend: str
    api_token: str | None
    receipt_signing_secret: str

    @property
    def is_demo_mode(self) -> bool:
        return self.mode == "demo"

    @property
    def is_client_mode(self) -> bool:
        return self.mode == "client"


def get_settings() -> RuntimeSettings:
    # Demo access must be explicitly opted into; unknown values must never
    # silently downgrade a deployment to the unauthenticated demo posture.
    mode = os.getenv("ELYRIA_MODE", "client").lower().strip()
    if mode not in {"demo", "client"}:
        raise ValueError("ELYRIA_MODE must be explicitly set to 'demo' or 'client'.")

    default_demo_secret = "elyria-demo-signing-secret-change-me" if mode == "demo" else ""
    return RuntimeSettings(
        mode=mode,
        db_path=os.getenv("ELYRIA_DB_PATH", "data/elyria.db"),
        storage_backend=os.getenv("ELYRIA_STORAGE_BACKEND", "sqlite").lower().strip(),
        api_token=os.getenv("ELYRIA_API_TOKEN"),
        receipt_signing_secret=os.getenv("ELYRIA_RECEIPT_SIGNING_SECRET", default_demo_secret),
    )
