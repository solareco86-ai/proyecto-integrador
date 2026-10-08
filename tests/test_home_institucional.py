"""Pruebas de la portada migrada al sistema institucional (docs/rediseno).

Cubren las dos garantías que motivaron la migración: que el contenido salga de
`data/` y no de la plantilla, y que la portada no publique plazos de inscripción
mientras Secretaría no comunique una fecha oficial.
"""

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app
from src.infrastructure.settings import config


async def _home_html() -> str:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    return response.text


@pytest.mark.asyncio
async def test_portada_lista_las_carreras_de_data() -> None:
    """Las carreras de la portada salen del YAML, no de una lista en la plantilla."""
    html = await _home_html()
    carreras = DataService(data_dir=config.DATA_DIR).get_carreras()

    assert carreras, "El catálogo de carreras no debería estar vacío"
    for carrera in carreras:
        assert carrera.title in html
        assert f'href="/carreras/{carrera.slug}"' in html


@pytest.mark.asyncio
async def test_portada_toma_las_sedes_de_data() -> None:
    """Los domicilios dejaron de estar escritos en templates/index.html."""
    html = await _home_html()
    sedes = DataService(data_dir=config.DATA_DIR).get_contenido().content.sedes

    assert sedes, "Debería haber al menos una sede cargada"
    for sede in sedes:
        assert sede.nombre in html
        for linea in sede.direccion:
            assert linea in html


def test_la_plantilla_no_hardcodea_carreras_ni_sedes() -> None:
    """Regla de desacoplamiento de contenido (AGENTS.md, secciones 2b y 3).

    Se verifica sobre el texto de la plantilla, no sobre el HTML renderizado:
    el objetivo es que nadie vuelva a escribir el catálogo a mano.
    """
    plantilla = Path(config.TEMPLATES_DIR, "index.html").read_text(encoding="utf-8")

    for prohibido in (
        "Tecnicatura Superior en",
        "Celina Voena",
        "Alte. Brown",
        "Cerrito 3966",
    ):
        assert prohibido not in plantilla, (
            f"'{prohibido}' quedó hardcodeado en templates/index.html; "
            "ese dato vive en data/."
        )


@pytest.mark.asyncio
async def test_portada_no_publica_plazos_sin_fecha_oficial() -> None:
    """Sin `admision.cierre` cargado, la portada no muestra cuenta regresiva.

    Evita que vuelva a aparecer una fecha de inscripción inventada
    (AGENTS.md, secciones 3 y 7.5).
    """
    contenido = DataService(data_dir=config.DATA_DIR).get_contenido()
    admision = contenido.content.admision
    assert admision is not None

    html = await _home_html()
    if admision.cierre is None:
        assert "Cierre de la preinscripción" not in html
        assert "días restantes" not in html
    else:
        assert admision.cierre.fecha_texto in html


@pytest.mark.asyncio
async def test_portada_usa_el_sistema_institucional() -> None:
    """La portada carga su hoja de estilos y sale del shell heredado."""
    html = await _home_html()

    assert "css/sistema.css" in html
    # El shell heredado de DataMaq (fondo oscuro y reserva del CTA flotante) ya
    # no envuelve a la portada. Se verifica sobre el atributo del contenedor,
    # porque el nombre de la clase sigue existiendo en el CSS crítico que usan
    # las páginas todavía sin migrar.
    assert 'id="top" class="capa-institucional"' in html
    assert 'class="app-shell app-shell--home' not in html
