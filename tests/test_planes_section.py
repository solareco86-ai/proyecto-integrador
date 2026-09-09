"""Pruebas de la sección institucional y de carreras del home de ISFT N° 199."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_home_renders_complete_isft199():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    assert "ISFT N° 199" in html
    assert "Educación Pública Superior" in html
    assert "Formación técnica de excelencia" in html
    assert "Ciencia de Datos" in html
    assert "Mecatrónica" in html


@pytest.mark.asyncio
async def test_home_academic_proof_and_services():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    assert "Educación Superior Técnica Gratuita" in html
    assert "Horario Vespertino (18 a 22:30 hs)" in html
    assert "Campus Virtual Integrado" in html


@pytest.mark.asyncio
async def test_home_carreras_and_contact_ctas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    assert 'href="/carreras"' in html
    assert "/contact" in html

