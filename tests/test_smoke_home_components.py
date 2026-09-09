"""Pruebas de humo: verifican que los componentes clave del home están presentes en el HTML renderizado.

Estas pruebas usan la app real con sus dependencias de datos (no mocks),
lo que las hace más sensibles a regresiones de UI que los tests unitarios.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_home_renders_with_all_key_sections():
    """Verifica que la home contiene todos los componentes clave post-refactorización."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    # Hero
    assert "Formación técnica de excelencia" in html or "ISFT N° 199" in html
    assert "Educación Pública Superior" in html

    # Proof strip
    assert "c-home-proof-strip" in html
    assert "Educación Superior Técnica Gratuita" in html
    assert "Campus Virtual Integrado" in html

    # Servicios / Ejes Formativos
    assert "Ciencia de Datos" in html or "Mecatrónica" in html

    # Process
    assert "c-home-process" in html
    assert "Elegí tu Carrera" in html or "Preinscripción" in html

    # Profile / Docentes
    assert "Docentes con trayectoria" in html or "Cuerpo Docente" in html

    # Casos section
    assert "c-home-casos" in html

    # Cursos section
    assert "c-home-cursos" in html
    assert "Campus Virtual" in html

    # FAQ
    assert "c-home-faq" in html

    # Contact
    assert "Inscripciones y Consultas Institucionales" in html



@pytest.mark.asyncio
async def test_home_no_prohibited_content():
    """Verifica que NO hay referencias a Vaca Muerta, Oil & Gas ni Neuquén en la home."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    prohibited = [
        "Vaca Muerta",
        "Oil &amp; Gas",
        "yacimiento",
        "Cuenca Neuquina",
        "Neuquén Capital",
    ]
    for term in prohibited:
        assert term not in html, f"Término prohibido '{term}' encontrado en la home"


@pytest.mark.asyncio
async def test_home_json_ld_valid():
    """Verifica que el JSON-LD de la home es sintácticamente válido."""
    import json
    import re

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    pattern = re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', re.DOTALL)
    blocks = pattern.findall(html)
    assert len(blocks) > 0, "No se encontraron bloques JSON-LD en la home"

    for block in blocks:
        try:
            json.loads(block.strip())
        except json.JSONDecodeError as e:
            pytest.fail(f"JSON-LD inválido: {block[:200]}... Error: {e}")


@pytest.mark.asyncio
async def test_service_automatizacion_linked_to_caso():
    """Verifica que el servicio de automatización linkea al caso MadyGraf."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text

    # El caso_slug "madygraf-eficiencia-y-vision-40" debe estar referenciado
    assert "madygraf-eficiencia-y-vision-40" in html


@pytest.mark.asyncio
async def test_casos_detail_renders_all_fields():
    """Verifica que el detalle del caso MadyGraf renderiza los campos clave."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/casos/madygraf-eficiencia-y-vision-40")

    assert response.status_code == 200
    html = response.text

    assert "MadyGraf" in html
    assert "visión artificial" in html.lower() or "iot" in html.lower()


@pytest.mark.asyncio
async def test_all_casos_pages_render():
    """Verifica que todos los casos listados renderizan sin error."""
    from src.application.data_service import DataService

    service = DataService()
    casos = service.get_casos()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for caso in casos:
            response = await ac.get(f"/casos/{caso.slug}")
            assert response.status_code == 200, f"Error en /casos/{caso.slug}"
            assert caso.title[:30] in response.text, f"Título no encontrado en /casos/{caso.slug}"
