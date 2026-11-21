"""Integridad de la lista maestra de palabras clave negativas de Google Ads (data/ads/)."""

import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path

from src.application.data_service import DataService

ADS_DIR = Path("data/ads")
TXT_PATH = ADS_DIR / "negative_keywords_clean.txt"
CSV_PATH = ADS_DIR / "negative_keywords_editor.csv"
CSV_HEADER: list[str] = ["List Name", "Criterion Type", "Keyword Text", "Match Type"]
MATCH_TYPES: frozenset[str] = frozenset({"Broad", "Phrase", "Exact"})
TERMINOS_HEREDADOS: tuple[str, ...] = ("datamaq", "powermeter", "xubio")


def _palabras(texto: str) -> list[str]:
    """Palabras en minúscula y sin tildes, para comparar términos de búsqueda."""
    plano = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return re.findall(r"[a-z0-9]+", plano)


def _desde_txt(linea: str) -> tuple[str, str]:
    """Traduce la sintaxis de Google Ads: "frase" -> Phrase, [exacta] -> Exact, resto -> Broad."""
    if linea.startswith('"') and linea.endswith('"'):
        return linea[1:-1], "Phrase"
    if linea.startswith("[") and linea.endswith("]"):
        return linea[1:-1], "Exact"
    return linea, "Broad"


def _negativas_txt() -> list[tuple[str, str]]:
    lineas: list[str] = [linea.strip() for linea in TXT_PATH.read_text(encoding="utf-8").splitlines()]
    return [_desde_txt(linea) for linea in lineas if linea]


def _filas_csv() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        assert lector.fieldnames == CSV_HEADER, f"Encabezado inválido: {lector.fieldnames}"
        return list(lector)


def test_negative_keywords_txt_and_csv_are_in_sync() -> None:
    """Ambos archivos tienen los mismos términos, en el mismo orden y con la misma concordancia."""
    desde_txt = _negativas_txt()
    desde_csv: list[tuple[str, str]] = [(fila["Keyword Text"], fila["Match Type"]) for fila in _filas_csv()]
    assert len(desde_txt) > 0
    assert desde_txt == desde_csv


def test_negative_keywords_csv_format() -> None:
    """Formato válido para Google Ads Editor: una sola lista del ISFT N° 199 y tipos conocidos."""
    filas = _filas_csv()
    nombres: set[str] = {fila["List Name"] for fila in filas}
    assert len(nombres) == 1, f"Se esperaba una sola lista: {nombres}"
    assert "ISFT N° 199" in next(iter(nombres))
    assert {fila["Criterion Type"] for fila in filas} == {"Negative Keyword"}
    assert {fila["Match Type"] for fila in filas} <= MATCH_TYPES
    for fila in filas:
        texto = fila["Keyword Text"]
        assert texto.strip(), "Hay una negativa vacía"
        assert not re.search(r'["\[\]]', texto), f"Sintaxis de concordancia dentro del texto: {texto!r}"


def test_negative_keywords_have_no_duplicates() -> None:
    claves: list[tuple[str, str]] = [(" ".join(_palabras(kw)), tipo) for kw, tipo in _negativas_txt()]
    duplicadas: list[tuple[str, str]] = [clave for clave, n in Counter(claves).items() if n > 1]
    assert duplicadas == [], f"Negativas duplicadas: {duplicadas}"


def test_negative_keywords_have_no_inherited_brand() -> None:
    for ruta in (TXT_PATH, CSV_PATH):
        texto: str = ruta.read_text(encoding="utf-8").lower()
        for termino in TERMINOS_HEREDADOS:
            assert termino not in texto, f"{ruta} conserva contenido heredado: {termino!r}"


def test_negative_keywords_do_not_block_official_careers() -> None:
    """Ninguna negativa excluye búsquedas del nombre, materias o salida laboral de una tecnicatura."""
    protegidos: list[str] = []
    for carrera in DataService(data_dir="data").get_carreras():
        protegidos += [carrera.title, *carrera.materias_destacadas, *carrera.salida_laboral]

    bloqueos: list[str] = []
    for kw, tipo in _negativas_txt():
        kw_palabras = _palabras(kw)
        for texto in protegidos:
            palabras = _palabras(texto)
            if (
                (tipo == "Broad" and set(kw_palabras) <= set(palabras))
                or (tipo == "Phrase" and f" {' '.join(kw_palabras)} " in f" {' '.join(palabras)} ")
                or (tipo == "Exact" and kw_palabras == palabras)
            ):
                bloqueos.append(f"{kw!r} ({tipo}) bloquea: {texto}")
    assert bloqueos == [], "\n".join(bloqueos)


CONSULTAS_DE_PRECIO: tuple[str, ...] = (
    "cuanto cuesta la carrera de mecatronica",
    "precio de la carrera de logistica",
    "arancel tecnicatura higiene y seguridad",
    "aranceles isft 199",
    "cuota mensual tecnicatura en ciencia de datos",
    "cuanto sale la cuota de la tecnicatura",
    "costo por mes de la tecnicatura",
    "precio mensual tecnicatura recursos humanos",
)


def _bloquea(kw: str, tipo: str, consulta: str) -> bool:
    """Regla de coincidencia de una negativa de Google Ads (amplia, frase o exacta) sobre una búsqueda."""
    kw_palabras = _palabras(kw)
    palabras = _palabras(consulta)
    if tipo == "Broad":
        return set(kw_palabras) <= set(palabras)
    if tipo == "Phrase":
        return f" {' '.join(kw_palabras)} " in f" {' '.join(palabras)} "
    if tipo == "Exact":
        return kw_palabras == palabras
    raise ValueError(f"Tipo de concordancia desconocido: {tipo!r}")


def test_negative_keywords_do_not_exclude_generic_price_searches() -> None:
    """Política 2.1.1: la gratuidad es la propuesta de valor; no se excluyen búsquedas genéricas de precio."""
    negativas = _negativas_txt()
    bloqueadas: list[str] = [
        f"{consulta!r} <- {kw!r} ({tipo})"
        for consulta in CONSULTAS_DE_PRECIO
        for kw, tipo in negativas
        if _bloquea(kw, tipo, consulta)
    ]
    assert bloqueadas == [], "\n".join(bloqueadas)
