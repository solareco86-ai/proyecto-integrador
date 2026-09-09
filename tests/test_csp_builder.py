"""Tests unitarios del builder declarativo de Content-Security-Policy."""

from src.infrastructure.fastapi.csp import build_csp


def test_build_csp_incluye_directivas_requeridas() -> None:
    csp = build_csp()
    for directive in (
        "default-src",
        "script-src",
        "style-src",
        "img-src",
        "connect-src",
        "font-src",
        "frame-src",
        "report-uri",
    ):
        assert f"{directive} " in csp


def test_build_csp_sin_cloudflare() -> None:
    csp = build_csp()
    assert "cloudflareinsights.com" not in csp


def test_build_csp_report_uri_conectado() -> None:
    csp = build_csp()
    assert "report-uri /csp-report" in csp


def test_build_csp_inyecta_telemetria() -> None:
    csp = build_csp(("https://api.datamaq.com.ar", "wss://api.datamaq.com.ar/ws/live"))
    assert "https://api.datamaq.com.ar" in csp
    assert "wss://api.datamaq.com.ar/ws/live" in csp
    # La telemetría debe quedar dentro de connect-src
    assert "connect-src 'self' ws: wss:" in csp


def test_build_csp_determinista() -> None:
    assert build_csp(("https://a.example",)) == build_csp(("https://a.example",))


def test_build_csp_conserva_dominios_ads_clarity() -> None:
    csp = build_csp()
    assert "https://www.googleadservices.com" in csp
    assert "https://googleads.g.doubleclick.net" in csp
    assert "https://stats.g.doubleclick.net" in csp
    assert "https://scripts.clarity.ms" in csp
    assert "https://c.bing.com" in csp


def test_build_csp_sin_telemetria_sin_espacios() -> None:
    csp = build_csp()
    assert "  " not in csp
    assert not csp.endswith(" ")
