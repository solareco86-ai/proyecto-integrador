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
    # El encabezado dejó de ser un eslogan con pastilla de color: ahora comunica
    # la oferta concreta y su carácter público (ver docs/rediseno).
    assert "Siete tecnicaturas superiores" in html
    assert "Validez nacional" in html
    assert "Ciencia de Datos" in html
    assert "Mecatrónica" in html


@pytest.mark.asyncio
async def test_home_academic_proof_and_services():
    """Verifica que la Home institucional comunique gratuidad, horario vespertino
    y Campus Virtual a través de sus secciones reales (Hero, FAQ, Estudiantes),
    ya sin la franja "proof strip" comercial de DataMaq."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    assert "100% gratuitas" in html
    assert "vespertino" in html.lower()
    assert "Campus Virtual" in html
    assert "c-home-proof-strip" not in html


@pytest.mark.asyncio
async def test_home_carreras_and_contact_ctas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    assert 'href="/carreras"' in html
    assert "/contact" in html

