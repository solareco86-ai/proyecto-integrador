"""Las páginas comerciales heredadas de DataMaq redirigen con 301 al catálogo académico.

El portal es institucional, público y gratuito (AGENTS.md §7.1). Las páginas de
telemetría por localidad, industria y landing se retiraron: conducen a /carreras
(como /pricing y /planes), no están en el sitemap y los redirects no encadenan.
"""

import re

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app

DESTINO: str = "/carreras"
REDIRECTS: dict[str, str] = DataService(data_dir="data").get_redirects()
COMERCIALES: tuple[str, ...] = (
    "/buenos-aires",
    "/buenos-aires/tigre",
    "/buenos-aires/tigre/el-talar.html",
    "/buenos-aires/escobar/garin.html",
    "/industria/grafica.html",
    "/industria/plastica.html",
    "/landing/calidad-energia",
    "/landing/calidad-energia.html",
    "/landing/telemetria-industrial",
    "/landing/telemetria-industrial.html",
)


def cliente() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=False)


def urls_servibles_desde_los_datos() -> set[str]:
    """Todas las URLs comerciales que las rutas podrían servir según geografia e industrias."""
    servicio = DataService(data_dir="data")
    urls: set[str] = {"/landing/calidad-energia", "/landing/telemetria-industrial"}
    urls |= {"/landing/calidad-energia.html", "/landing/telemetria-industrial.html"}
    for provincia, municipios in servicio.get_geografia().get("localidades", {}).items():
        urls.add(f"/{provincia}")
        for municipio, localidades in municipios.items():
            urls.add(f"/{provincia}/{municipio}")
            urls.update(f"/{provincia}/{municipio}/{localidad}.html" for localidad in localidades)
    urls.update(f"/industria/{industria}.html" for industria in servicio.get_industrias().industrias)
    return urls


@pytest.mark.asyncio
@pytest.mark.parametrize("ruta", COMERCIALES)
async def test_pagina_comercial_redirige_al_catalogo(ruta: str) -> None:
    async with cliente() as ac:
        respuesta = await ac.get(ruta)
    assert respuesta.status_code == 301
    assert respuesta.headers["location"] == DESTINO


@pytest.mark.asyncio
@pytest.mark.parametrize(("origen", "destino"), sorted(REDIRECTS.items()))
async def test_cada_redirect_del_yaml_se_aplica(origen: str, destino: str) -> None:
    async with cliente() as ac:
        respuesta = await ac.get(origen)
    assert respuesta.status_code == 301
    assert respuesta.headers["location"] == destino


def test_los_redirects_no_encadenan() -> None:
    encadenados: list[str] = [origen for origen, destino in REDIRECTS.items() if destino in REDIRECTS]
    assert not encadenados, f"redirects cuyo destino también redirige: {encadenados}"


def test_toda_url_comercial_servible_tiene_redirect() -> None:
    sin_redirect: set[str] = urls_servibles_desde_los_datos() - set(REDIRECTS)
    assert not sin_redirect, f"URLs comerciales sin redirect (se servirían con 200): {sorted(sin_redirect)}"


@pytest.mark.asyncio
async def test_sitemap_no_incluye_paginas_comerciales() -> None:
    async with cliente() as ac:
        respuesta = await ac.get("/sitemap.xml")
    assert respuesta.status_code == 200
    for fragmento in ("/buenos-aires", "/industria/", "/landing/"):
        assert fragmento not in respuesta.text, f"el sitemap todavía lista {fragmento}"


@pytest.mark.asyncio
async def test_sitemap_conserva_las_paginas_institucionales() -> None:
    async with cliente() as ac:
        respuesta = await ac.get("/sitemap.xml")
    for ruta in ("/carreras", "/cursos", "/contact"):
        assert f"{ruta}</loc>" in respuesta.text, f"falta {ruta} en el sitemap"


@pytest.mark.asyncio
async def test_los_redirects_no_afectan_estaticos_ni_paginas_vigentes() -> None:
    async with cliente() as ac:
        carreras = await ac.get("/carreras")
        casos = await ac.get("/casos/madygraf-eficiencia-y-vision-40")
    assert carreras.status_code == 200
    assert casos.status_code == 404
RUTAS_PUBLICAS: tuple[str, ...] = ("/", "/carreras", "/contact", "/terminos-y-condiciones")
@pytest.mark.asyncio
@pytest.mark.parametrize("ruta", RUTAS_PUBLICAS)
async def test_paginas_publicas_no_enlazan_a_paginas_retiradas(ruta: str) -> None:
    """Ni el cuerpo ni el footer de las páginas institucionales apuntan a URLs que ya redirigen."""
    retiradas = urls_servibles_desde_los_datos() | set(REDIRECTS)
    async with cliente() as ac:
        respuesta = await ac.get(ruta)
    assert respuesta.status_code in (200, 404)
    enlaces = set(re.findall(r'href="([^"#?]+)', respuesta.text))
    assert enlaces & retiradas == set()
