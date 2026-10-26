import pytest


@pytest.fixture(autouse=True)
def explicit_demo_mode_for_legacy_unit_tests(monkeypatch, request):
    """Keep legacy unit tests deterministic without weakening default-mode tests."""
    if request.module.__name__.endswith("test_runtime_security_defaults"):
        return
    if "ELYRIA_MODE" not in __import__("os").environ:
        monkeypatch.setenv("ELYRIA_MODE", "demo")
