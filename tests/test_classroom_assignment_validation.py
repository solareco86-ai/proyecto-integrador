"""Pruebas del primer work unit de asignación de aulas."""

import csv
from pathlib import Path

from src.adapters.classroom_assignment.csv_reader import read_csv_rows
from src.application.use_cases.classroom_assignment.validate_input_data import (
    ValidateInputDataUseCase,
)
from src.domain.classroom_assignment.validation import validate_aulas, validate_comisiones

DATA_DIR = Path(__file__).parents[1] / "data" / "asignacion_aulas"


def _read_csv(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def test_lee_los_csv_sinteticos() -> None:
    aulas = read_csv_rows(DATA_DIR / "aulas.csv")
    comisiones = read_csv_rows(DATA_DIR / "comisiones.csv")

    assert len(aulas) == 5
    assert len(comisiones) == 8


def test_valida_los_datos_sinteticos() -> None:
    result = ValidateInputDataUseCase().execute(_read_csv("aulas.csv"), _read_csv("comisiones.csv"))

    assert result.is_valid
    assert len(result.aulas) == 5
    assert len(result.comisiones) == 8
    assert result.comisiones[0].hora_inicio.hour == 18


def test_informa_columnas_obligatorias_faltantes() -> None:
    result = validate_aulas([{"id_aula": "A001"}])

    assert not result.aulas
    assert {issue.code for issue in result.issues} == {"missing_column"}


def test_rechaza_capacidad_no_positiva() -> None:
    rows = _read_csv("aulas.csv")
    rows[0]["capacidad"] = "0"

    result = validate_aulas(rows)

    assert any(issue.code == "not_positive" and issue.field == "capacidad" for issue in result.issues)
    assert len(result.aulas) == 4


def test_rechaza_identificador_de_aula_repetido() -> None:
    rows = _read_csv("aulas.csv")
    rows[1]["id_aula"] = rows[0]["id_aula"]

    result = validate_aulas(rows)

    assert any(issue.code == "duplicate" for issue in result.issues)


def test_permite_aula_sin_equipamiento() -> None:
    rows = _read_csv("aulas.csv")
    for row in rows:
        row.pop("equipamiento")

    result = validate_aulas(rows)

    assert result.issues == ()
    assert result.aulas[0].equipamiento == ()


def test_rechaza_intervalo_horario_invertido() -> None:
    rows = _read_csv("comisiones.csv")
    rows[0]["hora_inicio"] = "20:00"
    rows[0]["hora_fin"] = "18:00"

    result = validate_comisiones(rows)

    assert any(issue.code == "invalid_interval" for issue in result.issues)


def test_rechaza_hora_con_formato_invalido() -> None:
    rows = _read_csv("comisiones.csv")
    rows[0]["hora_inicio"] = "18hs"

    result = validate_comisiones(rows)

    assert any(issue.code == "invalid_time" and issue.field == "hora_inicio" for issue in result.issues)

