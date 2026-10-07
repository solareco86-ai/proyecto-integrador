"""Los números de resolución DGCyE publicados deben coincidir con carreras.yaml.

`data/content/carreras.yaml` es la fuente de verdad (AGENTS.md §7.5). Este test
evita que un número quede desactualizado o mal tipeado en otro documento (caso
real: Ciencia de Datos figuraba como 273/22 siendo 2730/22).
"""

import re
from pathlib import Path

import pytest

ROOT: Path = Path(__file__).resolve().parent.parent

# Número precedido por «DGCyE N°», «Res. N°», «Res.» o «Resolución N°».
PATRON_RESOLUCION: re.Pattern[str] = re.compile(r"(?:DGCyE|Res\.|Resoluci[oó]n)(?: N°)? (\d{3,5}/\d{2})")

DOCUMENTOS: tuple[str, ...] = (
    "README.md",
    "static/llms.txt",
    "static/llms-full.txt",
    "docs/srs.md",
    "docs/PROYECTO_CATEDRA_PAA.md",
    "data/core/cursos/procesamiento-aprendizaje-automatico/curso.yaml",
)


def resoluciones_oficiales() -> set[str]:
    """Números de resolución declarados en carreras.yaml (campo `resolucion`)."""
    texto: str = (ROOT / "data" / "content" / "carreras.yaml").read_text(encoding="utf-8")
    return set(re.findall(r"^\s*resolucion:.*?(\d{3,5}/\d{2})", texto, re.MULTILINE))


def test_carreras_yaml_declara_resoluciones() -> None:
    assert resoluciones_oficiales(), "carreras.yaml no declara ninguna resolución"


@pytest.mark.parametrize("relativo", DOCUMENTOS)
def test_documento_usa_resoluciones_oficiales(relativo: str) -> None:
    texto: str = (ROOT / relativo).read_text(encoding="utf-8")
    desconocidas: set[str] = set(PATRON_RESOLUCION.findall(texto)) - resoluciones_oficiales()
    assert not desconocidas, f"{relativo} cita resoluciones ausentes de carreras.yaml: {sorted(desconocidas)}"
