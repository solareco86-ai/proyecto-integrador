import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_landing_calidad_energia_200():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://datamaq.com.ar") as client:
        response = await client.get("/landing/calidad-energia")
        assert response.status_code == 200
        text = response.text
        assert "Elimine Multas por Factor de Potencia" in text
        assert "Res. ENRE 544/2024" in text or "ENRE" in text
        assert 'data-component="power-factor-calculator"' in text or "c-calculator" in text
        assert "Schema.org" in text or "application/ld+json" in text
        assert "canonical" in text
        assert "https://datamaq.com.ar/landing/calidad-energia" in text


@pytest.mark.asyncio
async def test_landing_calidad_energia_html_redirect():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://datamaq.com.ar", follow_redirects=False) as client:
        response = await client.get("/landing/calidad-energia.html")
        assert response.status_code == 301
        assert response.headers["location"] == "/landing/calidad-energia"


@pytest.mark.asyncio
async def test_landing_telemetria_industrial_200():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://datamaq.com.ar") as client:
        response = await client.get("/landing/telemetria-industrial")
        assert response.status_code == 200
        text = response.text
        assert "Telemetría y Adquisición de Datos" in text
        assert "SaaS $0" in text or "SaaS" in text
        assert 'data-component="contact-form"' in text or "landing-nombre" in text
        assert "Schema.org" in text or "application/ld+json" in text
        assert "canonical" in text
        assert "https://datamaq.com.ar/landing/telemetria-industrial" in text


@pytest.mark.asyncio
async def test_landing_telemetria_industrial_html_redirect():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://datamaq.com.ar", follow_redirects=False) as client:
        response = await client.get("/landing/telemetria-industrial.html")
        assert response.status_code == 301
        assert response.headers["location"] == "/landing/telemetria-industrial"


@pytest.mark.asyncio
async def test_sitemap_includes_landings():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://datamaq.com.ar") as client:
        response = await client.get("/sitemap.xml")
        assert response.status_code == 200
        assert "<loc>https://datamaq.com.ar/landing/calidad-energia</loc>" in response.text
        assert "<loc>https://datamaq.com.ar/landing/telemetria-industrial</loc>" in response.text
