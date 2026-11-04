"""Adaptador para leer archivos CSV sin exponer detalles al dominio."""

import csv
from pathlib import Path
from typing import cast


class CsvReader:
    """Adaptador pequeño para leer CSV institucionales de forma reproducible."""

    def read_rows(self, path: Path) -> list[dict[str, str]]:
        """Lee un CSV UTF-8 y devuelve sus filas como diccionarios."""
        with path.open(mode="r", encoding="utf-8-sig", newline="") as file:
            return list(csv.DictReader(file))

    def read_headers(self, path: Path) -> tuple[str, ...]:
        """Lee únicamente los encabezados para validar un archivo antes de procesarlo."""
        with path.open(mode="r", encoding="utf-8-sig", newline="") as file:
            headers = cast(list[str], next(csv.reader(file), []))
            return tuple(headers)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Mantiene la función pública para los consumidores existentes."""
    return CsvReader().read_rows(path)

