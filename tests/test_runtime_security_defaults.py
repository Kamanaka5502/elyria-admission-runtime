import pytest

from consequence_twin.settings import get_settings


def test_runtime_defaults_to_client_mode(monkeypatch):
    monkeypatch.delenv("ELYRIA_MODE", raising=False)
    assert get_settings().mode == "client"
    assert get_settings().receipt_signing_secret == ""


def test_demo_mode_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv("ELYRIA_MODE", "demo")
    assert get_settings().is_demo_mode is True
    assert get_settings().receipt_signing_secret == "elyria-demo-signing-secret-change-me"


def test_unknown_runtime_mode_does_not_fall_back_to_demo(monkeypatch):
    monkeypatch.setenv("ELYRIA_MODE", "typo")
    with pytest.raises(ValueError, match="ELYRIA_MODE must be explicitly set"):
        get_settings()
