import pytest

from consequence_twin.preflight import (
    ProductionPreflightError,
    PreflightMode,
    all_enabled_config,
    evaluate_preflight,
    require_production_ready,
    review_mode_defaults,
)


def test_review_mode_passes_without_claiming_production_ready():
    result = evaluate_preflight(review_mode_defaults(), mode=PreflightMode.REVIEW)
    assert result.passed is True
    assert "non_demo_signing_enabled" in result.missing


def test_production_mode_fails_closed_when_controls_missing():
    config = review_mode_defaults()
    with pytest.raises(ProductionPreflightError):
        require_production_ready(config)


def test_production_mode_passes_when_all_required_controls_enabled():
    result = require_production_ready(all_enabled_config())
    assert result.passed is True
    assert result.missing == []


def test_production_mode_reports_missing_controls():
    config = all_enabled_config()
    config["audit_ledger_enabled"] = False
    result = evaluate_preflight(config, mode="production")
    assert result.passed is False
    assert result.missing == ["audit_ledger_enabled"]


def test_debug_mode_must_be_disabled_for_production():
    config = all_enabled_config()
    config["debug_mode_disabled"] = False
    with pytest.raises(ProductionPreflightError):
        require_production_ready(config)
