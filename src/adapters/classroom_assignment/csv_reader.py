"""Adaptador para leer archivos CSV sin exponer detalles al dominio."""

import csv
from pathlib import Path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Lee un CSV UTF-8 y devuelve sus filas como diccionarios."""
    with path.open(mode="r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

