from pathlib import Path

import pytest
import yaml
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app

CARRERAS_YAML = Path(__file__).resolve().parent.parent / "data" / "content" / "carreras.yaml"


def test_data_service_carreras_catalog():
    data_svc = DataService(data_dir="data")
    carreras = data_svc.get_carreras()
    # La cantidad la fija data/content/carreras.yaml, no este test.
    assert len(carreras) == len(yaml.safe_load(CARRERAS_YAML.read_text(encoding="utf-8"))["carreras"])

    slugs = [c.slug for c in carreras]
    assert "ciencia-de-datos-ia" in slugs
    assert "mecatronica" in slugs
    assert "logistica" in slugs
    assert "higiene-y-seguridad" in slugs
    assert "recursos-humanos" in slugs
    assert "turismo" in slugs
    assert "hoteleria" in slugs
    assert "turismo-y-hoteleria" not in slugs


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
    # El encabezado dejó de ser un eslogan: ahora dice cuántas carreras hay y
    # el comparador responde en qué se diferencian (ver docs/rediseno).
    assert "Oferta académica vigente" in html
    assert "Comparar las" in html
    assert "Ciencia de Datos e Inteligencia Artificial" in html
    assert "Mecatrónica" in html
    assert "Logística" in html
    assert "Higiene y Seguridad" in html
    assert "Recursos Humanos" in html
    assert "Turismo" in html
    assert "Hotelería" in html


@pytest.mark.asyncio
async def test_carrera_detail_page():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/carreras/ciencia-de-datos-ia")

    assert response.status_code == 200
    html = response.text
    assert "Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial" in html
    assert "Perfil del egresado" in html
    assert "Contenidos centrales" in html
    assert "Dónde se trabaja" in html
    assert "Preinscribirme a esta carrera" in html
    # La ficha lateral y las migas son parte del recorrido nuevo.
    assert "Ficha de la carrera" in html
    assert "Seguir mirando" in html


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
