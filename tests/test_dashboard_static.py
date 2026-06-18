from pathlib import Path


DASHBOARD = Path("apps/api/static/index.html")


def test_dashboard_has_client_token_panel():
    html = DASHBOARD.read_text(encoding="utf-8")
    assert "Client Token Panel" in html
    assert "elyriaClientBearerToken" in html
    assert "Test Protected Access" in html
    assert "signature_matches" in html
