"""Tests unitarios para validar Content-Security-Policy y cabeceras de seguridad con soporte de Google Ads."""

import logging
from collections.abc import Iterator

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.dtos import ContenidoModel
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido


@pytest.fixture
def _override_contenido(mock_contenido: ContenidoModel) -> Iterator[None]:
    app.dependency_overrides[get_contenido] = lambda: mock_contenido
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_csp_headers_en_respuestas_html(_override_contenido: None) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/contact")
        assert resp.status_code == 200
        assert "Content-Security-Policy" in resp.headers

        csp = resp.headers["Content-Security-Policy"]

        # 1. Directivas en script-src
        assert "https://www.googleadservices.com" in csp
        assert "https://googleads.g.doubleclick.net" in csp
        assert "https://scripts.clarity.ms" in csp
        assert "https://*.clarity.ms" in csp

        # 2. Directivas en img-src (pixels de conversión y telemetría)
        assert "https://www.google.com" in csp
        assert "https://www.google.com.ar" in csp
        assert "https://analytics.google.com" in csp
        assert "https://c.clarity.ms" in csp
        assert "https://c.bing.com" in csp

        # 3. Directivas en connect-src (beacons y colectores)
        assert "https://stats.g.doubleclick.net" in csp
        assert "https://ad.doubleclick.net" in csp
        assert "https://analytics.google.com" in csp
        assert "https://c.bing.com" in csp

        # 3b. Reporte de violaciones conectado
        assert "report-uri /csp-report" in csp

        # 4. Cabeceras estándar de seguridad y observabilidad
        assert resp.headers.get("X-Frame-Options") == "DENY"
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        assert "X-Commit-SHA" in resp.headers


@pytest.mark.asyncio
async def test_csp_report_endpoint() -> None:
    """Valida que el endpoint POST /csp-report acepte reportes de violación sin error 405."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/csp-report",
            json={"csp-report": {"document-uri": "https://datamaq.com.ar", "violated-directive": "script-src"}},
        )
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_csp_report_endpoint_loguea(caplog: pytest.LogCaptureFixture) -> None:
    """Valida que el endpoint loguee a nivel warning el reporte de violación CSP."""
    transport = ASGITransport(app=app)
    with caplog.at_level(logging.WARNING):
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/csp-report",
                json={"csp-report": {"document-uri": "https://datamaq.com.ar", "violated-directive": "script-src"}},
            )
    assert resp.status_code == 204
    assert any("Violación CSP" in record.message for record in caplog.records)


@pytest.mark.asyncio
async def test_security_headers_en_api_endpoints() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/healthz")
        assert resp.status_code == 200
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"
        assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
