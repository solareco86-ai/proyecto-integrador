import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app


def test_data_service_carreras_catalog():
    data_svc = DataService(data_dir="data")
    carreras = data_svc.get_carreras()
    assert len(carreras) == 6

    slugs = [c.slug for c in carreras]
    assert "ciencia-de-datos-ia" in slugs
    assert "mecatronica" in slugs
    assert "logistica" in slugs
    assert "higiene-y-seguridad" in slugs
    assert "recursos-humanos" in slugs
    assert "turismo-y-hoteleria" in slugs


def test_data_service_carrera_by_slug():
    data_svc = DataService(data_dir="data")
    carrera = data_svc.get_carrera_by_slug("ciencia-de-datos-ia")
    assert carrera is not None
    assert "Ciencia de Datos" in carrera.title
    assert carrera.duracion == "3 años"
    assert len(carrera.materias_destacadas) > 0
    assert len(carrera.salida_laboral) > 0


@pytest.mark.asyncio
async def test_carreras_catalog_page():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/carreras")

    assert response.status_code == 200
    html = response.text
    assert "Oferta Académica & Tecnicaturas Superiores" in html
    assert "Ciencia de Datos e Inteligencia Artificial" in html
    assert "Mecatrónica" in html
    assert "Logística" in html
    assert "Higiene y Seguridad" in html
    assert "Recursos Humanos" in html
    assert "Turismo" in html


@pytest.mark.asyncio
async def test_carrera_detail_page():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/carreras/ciencia-de-datos-ia")

    assert response.status_code == 200
    html = response.text
    assert "Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial" in html
    assert "Perfil Profesional del Egresado" in html
    assert "Ejes Temáticos y Materias Destacadas" in html
    assert "Alcance y Salida Laboral" in html
    assert "Preinscribirme a esta Carrera" in html


@pytest.mark.asyncio
async def test_carrera_detail_page_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/carreras/carrera-inexistente-123")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_inscripciones_redirect():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=False) as ac:
        response = await ac.get("/inscripciones")

    assert response.status_code == 301
    assert response.headers["location"] == "/carreras#requisitos"


@pytest.mark.asyncio
async def test_pricing_and_planes_redirect():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=False) as ac:
        res_pricing = await ac.get("/pricing")
        res_planes = await ac.get("/planes")

    assert res_pricing.status_code == 301
    assert res_pricing.headers["location"] == "/carreras"
    assert res_planes.status_code == 301
    assert res_planes.headers["location"] == "/carreras"


@pytest.mark.asyncio
async def test_sitemap_includes_carreras():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    xml = response.text
    assert "/carreras" in xml
    assert "/carreras/ciencia-de-datos-ia" in xml
    assert "/carreras/mecatronica" in xml
