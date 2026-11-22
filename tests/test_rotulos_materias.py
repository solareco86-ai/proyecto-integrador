"""Lo que el sitio llamaba «cursos» son materias de las tecnicaturas.

Se corrigen los rótulos visibles. Las rutas /cursos se conservan para no romper
enlaces compartidos ni el posicionamiento: cambiarlas necesita redirecciones 301
y es una decisión aparte.
"""

import re
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app

PLANTILLAS = Path(__file__).resolve().parent.parent / "templates"

# Rótulos visibles que antes decían «Cursos»: dock, migas, títulos y JSON-LD.
ROTULO_VIEJO = re.compile(r"'label': 'Cursos'|>Cursos</a>|\"name\": \"Cursos\"|Cursos destacados|Cursos Dictados")


def test_ninguna_plantilla_rotula_cursos() -> None:
    con_rotulo_viejo = [
        str(ruta.relative_to(PLANTILLAS))
        for ruta in PLANTILLAS.rglob("*.html")
        if ROTULO_VIEJO.search(ruta.read_text(encoding="utf-8"))
    ]
    assert con_rotulo_viejo == []


@pytest.mark.asyncio
async def test_el_listado_dice_materias_y_conserva_la_ruta() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        respuesta = await ac.get("/cursos")

    html = respuesta.text
    assert respuesta.status_code == 200
    assert "Materias destacadas" in html
    assert '"name": "Materias",' in html  # JSON-LD de las migas
    assert '<span data-v-236fef00="">Materias</span>' in html  # dock inferior
    assert not ROTULO_VIEJO.search(html)
