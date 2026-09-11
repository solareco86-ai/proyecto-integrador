"""Generador de slugs url-safe a partir de texto libre (stdlib, sin dependencias nuevas)."""

import re
import unicodedata


def slugify(texto: str) -> str:
    """Normaliza un texto a un slug en minúsculas, sin tildes, separado por guiones.

    Ej: "Inscripción 2027: ¡Últimas vacantes!" -> "inscripcion-2027-ultimas-vacantes"
    """
    normalizado = unicodedata.normalize("NFKD", texto)
    sin_tildes = normalizado.encode("ascii", "ignore").decode("ascii")
    minusculas = sin_tildes.lower()
    con_guiones = re.sub(r"[^a-z0-9]+", "-", minusculas)
    return con_guiones.strip("-") or "item"
