from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class SigningMode(str, Enum):
    LOCAL_DEMO_HMAC = "local_demo_hmac"
    FILE_KEY = "file_key"
    KMS_STUB = "kms_stub"
    EXTERNAL_SIGNING_ADAPTER = "external_signing_adapter"


class SigningError(RuntimeError):
    """Raised when signing configuration is invalid or verification fails."""


DEMO_KEY_ID = "elyria-demo-key"
DEMO_SECRET = "elyria-demo-signing-secret-change-me"
SIGNATURE_ALG = "HMAC-SHA256"


@dataclass(frozen=True)
class SigningConfig:
    mode: SigningMode
    key_id: str
    secret: str | None = None
    production_mode: bool = False


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_signing_config(
    *,
    mode: str | SigningMode | None = None,
    key_id: str | None = None,
    secret: str | None = None,
    production_mode: bool | None = None,
) -> SigningConfig:
    resolved_mode = SigningMode(mode or os.getenv("ELYRIA_SIGNING_MODE", SigningMode.LOCAL_DEMO_HMAC.value))
    resolved_production = (
        production_mode
        if production_mode is not None
        else os.getenv("ELYRIA_MODE", "demo").lower() == "production"
    )
    resolved_key_id = key_id or os.getenv("ELYRIA_SIGNING_KEY_ID") or (
        DEMO_KEY_ID if resolved_mode == SigningMode.LOCAL_DEMO_HMAC else ""
    )
    resolved_secret = secret or os.getenv("ELYRIA_RECEIPT_SIGNING_SECRET")

    if resolved_mode == SigningMode.LOCAL_DEMO_HMAC:
        resolved_secret = resolved_secret or DEMO_SECRET
        resolved_key_id = resolved_key_id or DEMO_KEY_ID

    config = SigningConfig(
        mode=resolved_mode,
        key_id=resolved_key_id,
        secret=resolved_secret,
        production_mode=bool(resolved_production),
    )
    validate_signing_config(config)
    return config


def validate_signing_config(config: SigningConfig) -> None:
    if config.production_mode and config.mode == SigningMode.LOCAL_DEMO_HMAC:
        raise SigningError("demo signing mode cannot be used in production mode")
    if config.production_mode and config.key_id == DEMO_KEY_ID:
        raise SigningError("demo key_id cannot be used in production mode")
    if config.mode in {SigningMode.LOCAL_DEMO_HMAC, SigningMode.FILE_KEY} and not config.secret:
        raise SigningError("signing secret is required")
    if not config.key_id:
        raise SigningError("key_id is required")


def sign_material(material: Dict[str, Any], config: SigningConfig) -> str:
    validate_signing_config(config)
    if config.mode == SigningMode.KMS_STUB:
        body = f"kms_stub:{config.key_id}:{sha256_json(material)}"
        return hashlib.sha256(body.encode("utf-8")).hexdigest()
    if config.mode == SigningMode.EXTERNAL_SIGNING_ADAPTER:
        body = f"external_adapter:{config.key_id}:{sha256_json(material)}"
        return hashlib.sha256(body.encode("utf-8")).hexdigest()
    if not config.secret:
        raise SigningError("signing secret is required")
    return hmac.new(
        config.secret.encode("utf-8"),
        canonical_json(material).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_material(material: Dict[str, Any], signature: str, config: SigningConfig) -> bool:
    expected = sign_material(material, config)
    return hmac.compare_digest(signature, expected)


def build_receipt_signing_material(receipt: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "receipt_id",
        "movement_id",
        "tenant_id",
        "verdict",
        "input_hash",
        "evidence_hash",
        "policy_pack_hash",
        "engine_version",
        "key_id",
        "signature_alg",
    ]
    missing = [field for field in required if field not in receipt]
    if missing:
        raise SigningError(f"missing receipt signing fields: {', '.join(missing)}")
    return {field: receipt[field] for field in required}


def sign_receipt_fields(receipt: Dict[str, Any], config: SigningConfig) -> Dict[str, Any]:
    enriched = dict(receipt)
    enriched["key_id"] = config.key_id
    enriched["signature_alg"] = SIGNATURE_ALG
    material = build_receipt_signing_material(enriched)
    enriched["signature"] = sign_material(material, config)
    return enriched


def verify_signed_receipt(receipt: Dict[str, Any], config: SigningConfig) -> bool:
    material = build_receipt_signing_material(receipt)
    return verify_material(material, str(receipt.get("signature", "")), config)
