"""Garantías sobre el prototipo del rediseño (docs/rediseno/prototipo).

El prototipo contiene datos inventados (fechas, novedades, campus). Estos tests
mantienen la señalización de que no es información oficial y evitan que los
números de resolución se separen de carreras.yaml.
"""

import re
from pathlib import Path

from tests.test_resoluciones_consistentes import PATRON_RESOLUCION, resoluciones_oficiales

PROTOTIPO: Path = Path(__file__).resolve().parent.parent / "docs" / "rediseno" / "prototipo"
PANTALLAS: tuple[str, ...] = ("index.html", "carreras.html", "carrera.html", "campus.html")

# En el comparador la resolución aparece sola dentro de una celda de tabla.
CELDA_RESOLUCION: re.Pattern[str] = re.compile(r'<td class="dato">(\d{3,5}/\d{2})</td>')


def leer(pantalla: str) -> str:
    return (PROTOTIPO / pantalla).read_text(encoding="utf-8")


def test_cada_pantalla_abre_con_la_banda_de_prototipo() -> None:
    for pantalla in PANTALLAS:
        assert 'class="banda-prototipo"' in leer(pantalla), f"{pantalla} sin banda de prototipo"


def test_portada_etiqueta_el_estado_y_la_fecha_de_cierre_como_ejemplo() -> None:
    html: str = leer("index.html")
    assert html.count('class="etiqueta-ejemplo"') >= 2
    assert "Contenido de ejemplo" in html


def test_campus_declara_que_sus_datos_son_de_ejemplo() -> None:
    assert "datos de ejemplo" in leer("campus.html")


def test_resoluciones_del_prototipo_coinciden_con_carreras_yaml() -> None:
    oficiales: set[str] = resoluciones_oficiales()
    citadas: set[str] = set()
    for pantalla in PANTALLAS:
        html: str = leer(pantalla)
        citadas |= set(PATRON_RESOLUCION.findall(html))
        citadas |= set(CELDA_RESOLUCION.findall(html))
    assert citadas, "el prototipo no cita ninguna resolución"
    assert not citadas - oficiales, f"resoluciones fuera de carreras.yaml: {sorted(citadas - oficiales)}"
