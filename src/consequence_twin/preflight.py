from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, Iterable, List


class PreflightMode(str, Enum):
    REVIEW = "review"
    PRODUCTION = "production"


class ProductionPreflightError(RuntimeError):
    """Raised when production mode is requested without required controls."""


@dataclass(frozen=True)
class PreflightRequirement:
    name: str
    enabled: bool
    category: str
    required_for_production: bool = True

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class PreflightResult:
    mode: PreflightMode
    passed: bool
    missing: List[str]
    requirements: List[PreflightRequirement]

    def to_dict(self) -> Dict[str, object]:
        return {
            "mode": self.mode.value,
            "passed": self.passed,
            "missing": list(self.missing),
            "requirements": [requirement.to_dict() for requirement in self.requirements],
        }


REQUIRED_CONTROL_NAMES = [
    "auth_enabled",
    "rbac_enabled",
    "tenant_isolation_enabled",
    "persistent_receipt_store_enabled",
    "audit_ledger_enabled",
    "non_demo_signing_enabled",
    "policy_pack_loaded",
    "external_verifier_bundle_generated",
    "runtime_environment_marker_present",
    "debug_mode_disabled",
]


def build_requirements(config: Dict[str, bool]) -> List[PreflightRequirement]:
    return [
        PreflightRequirement("auth_enabled", bool(config.get("auth_enabled")), "identity"),
        PreflightRequirement("rbac_enabled", bool(config.get("rbac_enabled")), "identity"),
        PreflightRequirement(
            "tenant_isolation_enabled",
            bool(config.get("tenant_isolation_enabled")),
            "tenant_boundary",
        ),
        PreflightRequirement(
            "persistent_receipt_store_enabled",
            bool(config.get("persistent_receipt_store_enabled")),
            "persistence",
        ),
        PreflightRequirement(
            "audit_ledger_enabled",
            bool(config.get("audit_ledger_enabled")),
            "audit",
        ),
        PreflightRequirement(
            "non_demo_signing_enabled",
            bool(config.get("non_demo_signing_enabled")),
            "signing",
        ),
        PreflightRequirement("policy_pack_loaded", bool(config.get("policy_pack_loaded")), "policy"),
        PreflightRequirement(
            "external_verifier_bundle_generated",
            bool(config.get("external_verifier_bundle_generated")),
            "verification",
        ),
        PreflightRequirement(
            "runtime_environment_marker_present",
            bool(config.get("runtime_environment_marker_present")),
            "runtime_environment",
        ),
        PreflightRequirement(
            "debug_mode_disabled",
            bool(config.get("debug_mode_disabled")),
            "runtime_environment",
        ),
    ]


def evaluate_preflight(
    config: Dict[str, bool],
    *,
    mode: PreflightMode | str = PreflightMode.REVIEW,
) -> PreflightResult:
    resolved_mode = mode if isinstance(mode, PreflightMode) else PreflightMode(str(mode))
    requirements = build_requirements(config)
    missing = [
        requirement.name
        for requirement in requirements
        if requirement.required_for_production and not requirement.enabled
    ]
    if resolved_mode == PreflightMode.REVIEW:
        return PreflightResult(
            mode=resolved_mode,
            passed=True,
            missing=missing,
            requirements=requirements,
        )
    passed = not missing
    return PreflightResult(
        mode=resolved_mode,
        passed=passed,
        missing=missing,
        requirements=requirements,
    )


def require_production_ready(config: Dict[str, bool]) -> PreflightResult:
    result = evaluate_preflight(config, mode=PreflightMode.PRODUCTION)
    if not result.passed:
        raise ProductionPreflightError(
            "production preflight failed: " + ", ".join(result.missing)
        )
    return result


def review_mode_defaults() -> Dict[str, bool]:
    return {
        "auth_enabled": True,
        "rbac_enabled": True,
        "tenant_isolation_enabled": True,
        "persistent_receipt_store_enabled": True,
        "audit_ledger_enabled": True,
        "non_demo_signing_enabled": False,
        "policy_pack_loaded": True,
        "external_verifier_bundle_generated": True,
        "runtime_environment_marker_present": True,
        "debug_mode_disabled": True,
    }


def all_enabled_config(names: Iterable[str] = REQUIRED_CONTROL_NAMES) -> Dict[str, bool]:
    return {name: True for name in names}
