"""La oferta de carreras publicada debe coincidir con carreras.yaml (fuente de verdad).

Caso real que motiva este test: README, llms*.txt y el JSON-LD de SEO describían
6 carreras ("Servicios Gastronómicos y Turismo") cuando el catálogo oficial tiene
7 (Turismo y Hotelería por separado).
"""

import json
import re
from pathlib import Path
from typing import cast

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app

ROOT: Path = Path(__file__).resolve().parent.parent
PREFIJO: str = "Tecnicatura Superior en "
CANTIDAD_EN_PALABRAS: dict[str, int] = {"cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9}


def titulos_oficiales() -> list[str]:
    service = DataService(data_dir=str(ROOT / "data"))
    return [carrera.title for carrera in service.get_carreras()]


def leer(relativo: str) -> str:
    return (ROOT / relativo).read_text(encoding="utf-8")


def test_catalogo_oficial_no_esta_vacio() -> None:
    assert titulos_oficiales()


def test_readme_lista_todas_las_carreras() -> None:
    texto: str = leer("README.md")
    titulos: list[str] = titulos_oficiales()
    for titulo in titulos:
        assert f"*{titulo.removeprefix(PREFIJO)}*" in texto, f"README no lista: {titulo}"
    assert len(re.findall(r"^\s+\d+\. \*.+\(Resolución", texto, re.MULTILINE)) == len(titulos)


def test_llms_txt_lista_todas_las_carreras() -> None:
    texto: str = leer("static/llms.txt")
    titulos: list[str] = titulos_oficiales()
    for titulo in titulos:
        assert f"[{titulo}]" in texto, f"llms.txt no lista: {titulo}"
    assert len(re.findall(r"^\d+\. \[Tecnicatura Superior", texto, re.MULTILINE)) == len(titulos)


def test_llms_full_txt_lista_todas_las_carreras() -> None:
    texto: str = leer("static/llms-full.txt")
    titulos: list[str] = titulos_oficiales()
    for titulo in titulos:
        assert re.search(rf"^### 2\.\d+ {re.escape(titulo)}$", texto, re.MULTILINE), f"llms-full no lista: {titulo}"
    assert len(re.findall(r"^### 2\.\d+ Tecnicatura Superior", texto, re.MULTILINE)) == len(titulos)


def test_textos_del_home_citan_la_cantidad_correcta_de_tecnicaturas() -> None:
    texto: str = leer("data/content/home_sections.yaml")
    esperado: int = len(titulos_oficiales())
    citadas: list[int] = []
    for token in re.findall(r"\b(\w+) tecnicaturas", texto, re.IGNORECASE):
        if token.isdigit():
            citadas.append(int(token))
        elif token.lower() in CANTIDAD_EN_PALABRAS:
            citadas.append(CANTIDAD_EN_PALABRAS[token.lower()])
    assert citadas, "home_sections.yaml no menciona la cantidad de tecnicaturas"
    assert all(cantidad == esperado for cantidad in citadas), f"cantidades citadas {citadas}, oficiales {esperado}"


def nombres_de_cursos(nodo: object) -> list[str]:
    """Nombres de todos los nodos JSON-LD de tipo Course, en cualquier nivel."""
    nombres: list[str] = []
    if isinstance(nodo, dict):
        propiedades = cast(dict[str, object], nodo)
        nombre: object = propiedades.get("name")
        if propiedades.get("@type") == "Course" and isinstance(nombre, str):
            nombres.append(nombre)
        for valor in propiedades.values():
            nombres.extend(nombres_de_cursos(valor))
    elif isinstance(nodo, list):
        for elemento in cast(list[object], nodo):
            nombres.extend(nombres_de_cursos(elemento))
    return nombres


@pytest.mark.asyncio  # type: ignore
async def test_json_ld_del_home_ofrece_exactamente_las_carreras_oficiales() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        respuesta = await cliente.get("/")
    assert respuesta.status_code == 200
    bloques: list[str] = re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", respuesta.text, re.DOTALL)
    assert bloques, "el home no publica JSON-LD"
    nombres: list[str] = []
    for bloque in bloques:
        nombres.extend(nombres_de_cursos(json.loads(bloque)))
    assert sorted(nombres) == sorted(titulos_oficiales())
