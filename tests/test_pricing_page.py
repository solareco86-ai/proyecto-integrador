"""Pruebas RED de la página /pricing (planes y precios de telemetría).

Usan la app real con sus dependencias de datos YAML (sin mocks),
siguiendo el patrón de tests/test_planes_section.py.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_pricing_page_redirects_to_carreras():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=False) as ac:
        response = await ac.get("/pricing")

    assert response.status_code == 301
    assert response.headers["location"] == "/carreras"


@pytest.mark.asyncio
async def test_planes_page_redirects_to_carreras():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=False) as ac:
        response = await ac.get("/planes")

    assert response.status_code == 301
    assert response.headers["location"] == "/carreras"





@pytest.mark.asyncio
async def test_sitemap_does_not_include_pricing():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "/carreras" in response.text
    assert "/pricing" not in response.text

