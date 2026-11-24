"""Pruebas de la lección 2.2 (histogramas, umbral de Otsu y bordes) del curso de PDI.

Verifican que la lección se renderiza con sus imágenes de antes y después y con
las secciones que pide el issue #103 (ecualización y Otsu), y que las imágenes
que referencia existen y se sirven.
"""

import re
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app

RAIZ: Path = Path(__file__).resolve().parent.parent
LECCION: Path = (
    RAIZ
    / "data"
    / "core"
    / "cursos"
    / "procesamiento-imagenes-python-opencv"
    / "lecciones"
    / "cap-2-2-histogramas-umbralizacion-bordes-canny.md"
)
URL_LECCION: str = "/cursos/procesamiento-imagenes-python-opencv/histogramas-umbralizacion-bordes-canny"
PATRON_ESTATICO: re.Pattern[str] = re.compile(r"\]\((/static/[^)\s]+)\)")

IMAGENES_ESPERADAS: list[str] = [
    "/static/media/cursos/pdi/retina.jpg",
    "/static/media/cursos/pdi/monedas.png",
    "/static/media/cursos/pdi/texto.png",
    "/static/media/cursos/pdi/camara.jpg",
    "/static/media/cursos/pdi/astronauta.jpg",
    "/static/media/cursos/pdi/cafe.jpg",
    "/static/media/cursos/pdi/cohete.jpg",
    "/static/media/cursos/pdi/retina-histograma.webp",
    "/static/media/cursos/pdi/retina-ecualizada.webp",
    "/static/media/cursos/pdi/retina-clahe.webp",
    "/static/media/cursos/pdi/monedas-histograma-otsu.webp",
    "/static/media/cursos/pdi/monedas-umbral.webp",
    "/static/media/cursos/pdi/texto-otsu-vs-adaptativa.webp",
    "/static/media/cursos/pdi/monedas-sobel.webp",
    "/static/media/cursos/pdi/monedas-canny.webp",
    "/static/media/cursos/pdi/decision-antes-despues.webp",
]

SECCIONES_ESPERADAS: list[str] = [
    "El histograma de una imagen",
    "Ecualización del histograma",
    "Ecualización adaptativa (CLAHE)",
    "El método de Otsu",
    "Cuándo no alcanza un solo umbral",
    "Detección de bordes: Sobel",
    "Detección de bordes: Canny",
    "Ejercicio de cierre: el método de Otsu con NumPy",
    "Caso integrador: decidir qué corrección necesita una foto",
]


def test_la_leccion_solo_referencia_imagenes_que_existen() -> None:
    referencias: list[str] = PATRON_ESTATICO.findall(LECCION.read_text(encoding="utf-8"))
    assert sorted(set(referencias)) == sorted(IMAGENES_ESPERADAS)
    faltantes: list[str] = [ruta for ruta in referencias if not (RAIZ / ruta.lstrip("/")).is_file()]
    assert faltantes == []


@pytest.mark.asyncio
async def test_leccion_renderiza_secciones_e_imagenes() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(URL_LECCION)

    assert response.status_code == 200
    html: str = response.text
    for seccion in SECCIONES_ESPERADAS:
        assert seccion in html, seccion
    for imagen in IMAGENES_ESPERADAS:
        if imagen.endswith(".webp"):
            assert f'src="{imagen}"' in html, imagen
        else:
            assert f'href="{imagen}"' in html, imagen  # imágenes de trabajo, para descargar
    assert "cv2.equalizeHist" in html
    assert "cv2.THRESH_OTSU" in html


@pytest.mark.asyncio
async def test_imagenes_de_la_leccion_se_sirven() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for imagen in IMAGENES_ESPERADAS:
            response = await ac.get(imagen)
            assert response.status_code == 200, imagen
            assert response.headers["content-type"].startswith("image/"), imagen


VIDEO: str = "/static/media/cursos/pdi/video-histogramas-brillo-contraste.mp4"
PORTADA_VIDEO: str = "/static/media/cursos/pdi/video-histogramas-brillo-contraste.webp"


@pytest.mark.asyncio
async def test_leccion_muestra_el_video_y_se_sirve() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        pagina = await ac.get(URL_LECCION)
        video = await ac.get(VIDEO)
        portada = await ac.get(PORTADA_VIDEO)

    assert f'poster="{PORTADA_VIDEO}"' in pagina.text
    assert f'<source src="{VIDEO}" type="video/mp4">' in pagina.text
    assert video.status_code == 200
    assert video.headers["content-type"] == "video/mp4"
    assert portada.status_code == 200
    assert portada.headers["content-type"] == "image/webp"


def test_el_parser_permite_video_pero_filtra_atributos_peligrosos() -> None:
    from src.application.markdown_parser import MarkdownParser

    html: str = MarkdownParser().to_html(
        '<video controls="controls" autoplay="autoplay" onplay="robar()" poster="/p.webp">'
        '<source src="/v.mp4" type="video/mp4"></video>'
    )

    assert html == '<video controls="controls" poster="/p.webp"><source src="/v.mp4" type="video/mp4"></video>'
