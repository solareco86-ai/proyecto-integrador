import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_cursos_default_solo_publicos():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos")

    assert response.status_code == 200
    assert "Instalaciones y Aplicaciones de la Energía" in response.text
    assert "Lenguajes Electrónicos: Nivel Básico" not in response.text


@pytest.mark.asyncio
async def test_cursos_view_all_incluye_academicos():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos?view=all")

    assert response.status_code == 200
    assert "Lenguajes Electrónicos: Nivel Básico" in response.text
    assert "Instalaciones y Aplicaciones de la Energía" in response.text


@pytest.mark.asyncio
async def test_cursos_view_all_noindex():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos?view=all")

    assert response.status_code == 200
    assert "noindex, nofollow" in response.text


@pytest.mark.asyncio
async def test_cursos_default_indexable():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos")

    assert response.status_code == 200
    assert "noindex" not in response.text


@pytest.mark.asyncio
async def test_cursos_view_all_canonical_sin_query():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos?view=all")

    assert response.status_code == 200
    assert "rel='canonical' href='https://datamaq.com.ar/cursos'" in response.text
    assert "?view=all" not in response.text


@pytest.mark.asyncio
async def test_cursos_view_all_badge_academico():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos?view=all")

    assert response.status_code == 200
    assert "c-curso-card__badge--academic" in response.text
    assert "Alumnos" in response.text


@pytest.mark.asyncio
async def test_cursos_view_valor_desconocido_usa_default():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos?view=foo")

    assert response.status_code == 200
    assert "Lenguajes Electrónicos: Nivel Básico" not in response.text
    assert "noindex" not in response.text


@pytest.mark.asyncio
async def test_sitemap_no_incluye_view_all():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "?view=all" not in response.text
    assert "https://datamaq.com.ar/cursos" in response.text
