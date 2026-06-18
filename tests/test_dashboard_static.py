from pathlib import Path


DASHBOARD = Path("apps/api/static/index.html")


def test_dashboard_has_client_token_panel():
    html = DASHBOARD.read_text(encoding="utf-8")
    assert "Client Token Panel" in html
    assert "elyriaClientBearerToken" in html
    assert "Test Protected Access" in html
    assert "signature_matches" in html


def test_dashboard_has_client_movement_intake():
    html = DASHBOARD.read_text(encoding="utf-8")
    assert "Client Movement Intake" in html
    assert "Submit Movement + Emit Receipt" in html
    assert "submitMovement" in html
    assert "/movements/assess" in html
    assert "/exposures/current" in html
