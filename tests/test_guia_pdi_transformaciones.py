"""Pruebas de la lección 1.3 (transformaciones geométricas) del curso de PDI.

Verifican que la lección se renderiza con sus imágenes de antes y después, y que
ninguna lección del campus referencia archivos de `static/` inexistentes.
"""

import re
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app

RAIZ: Path = Path(__file__).resolve().parent.parent
LECCIONES: Path = RAIZ / "data" / "core" / "cursos"
URL_LECCION: str = "/cursos/procesamiento-imagenes-python-opencv/transformaciones-geometricas-operaciones"
PATRON_ESTATICO: re.Pattern[str] = re.compile(r"\]\((/static/[^)\s]+)\)")

IMAGENES_ESPERADAS: list[str] = [
    "/static/media/cursos/pdi/cafe.png",
    "/static/media/cursos/pdi/cafe-reducida.webp",
    "/static/media/cursos/pdi/cafe-deformada.webp",
    "/static/media/cursos/pdi/cafe-interpolacion.webp",
    "/static/media/cursos/pdi/cafe-zona-recorte.webp",
    "/static/media/cursos/pdi/cafe-recorte-taza.webp",
    "/static/media/cursos/pdi/cafe-rotada.webp",
    "/static/media/cursos/pdi/cafe-rotada-completa.webp",
    "/static/media/cursos/pdi/cafe-miniatura.webp",
]


@pytest.mark.asyncio
async def test_leccion_transformaciones_renderiza_imagenes_y_ejercicio() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(URL_LECCION)

    assert response.status_code == 200
    html: str = response.text
    for imagen in IMAGENES_ESPERADAS:
        assert f'src="{imagen}"' in html, imagen
    assert "Escalado con" in html
    assert "Recorte con slicing de NumPy" in html
    assert "Rotación con matrices afines" in html
    assert "Ejercicio de cierre" in html


@pytest.mark.asyncio
async def test_imagenes_de_la_leccion_se_sirven() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for imagen in IMAGENES_ESPERADAS:
            response = await ac.get(imagen)
            assert response.status_code == 200, imagen
            assert response.headers["content-type"].startswith("image/"), imagen


def test_lecciones_no_referencian_archivos_estaticos_inexistentes() -> None:
    faltantes: list[str] = []
    for leccion in sorted(LECCIONES.glob("*/lecciones/*.md")):
        texto: str = leccion.read_text(encoding="utf-8")
        for ruta in PATRON_ESTATICO.findall(texto):
            if not (RAIZ / ruta.lstrip("/")).is_file():
                faltantes.append(f"{leccion.relative_to(RAIZ)} -> {ruta}")
    assert faltantes == []
