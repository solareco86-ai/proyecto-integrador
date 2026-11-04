"""Pruebas de conflictos y grafo de superposiciones."""

import csv
from pathlib import Path

from src.application.use_cases.classroom_assignment.detect_conflicts import DetectConflictsUseCase
from src.application.use_cases.classroom_assignment.validate_input_data import ValidateInputDataUseCase
from src.domain.classroom_assignment.entities import Aula, Comision

DATA_DIR = Path(__file__).parents[1] / "data" / "asignacion_aulas"


def _read(name: str) -> list[dict[str, str]]:
    with (DATA_DIR / name).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def _valid_data() -> tuple[tuple[Comision, ...], tuple[Aula, ...]]:
    result = ValidateInputDataUseCase().execute(_read("aulas.csv"), _read("comisiones.csv"))
    assert result.is_valid
    return result.comisiones, result.aulas


def test_datos_sinteticos_no_tienen_conflictos_bloqueantes() -> None:
    comisiones, aulas = _valid_data()

    report, graph = DetectConflictsUseCase().execute(comisiones, aulas)

    assert report.is_feasible
    assert not report.errors
    assert graph.nodes == tuple(item.id_comision for item in comisiones)
    assert ("C001", "C002") in graph.edges


def test_detecta_comision_sin_aula_por_capacidad() -> None:
    comisiones, aulas = _valid_data()
    oversized = Comision(
        id_comision="C999",
        materia="Materia grande",
        carrera="Carrera de prueba",
        cantidad_estudiantes=100,
        dia="Jueves",
        hora_inicio=comisiones[0].hora_inicio,
        hora_fin=comisiones[0].hora_fin,
    )

    report, _ = DetectConflictsUseCase().execute((*comisiones, oversized), aulas)

    assert any(conflict.code == "NO_COMPATIBLE_ROOM" for conflict in report.errors)


def test_detecta_falta_de_aulas_para_comisiones_simultaneas() -> None:
    comisiones, aulas = _valid_data()
    first = Comision(
        id_comision="C997",
        materia="Materia A",
        carrera="Carrera de prueba",
        cantidad_estudiantes=48,
        dia="Jueves",
        hora_inicio=comisiones[0].hora_inicio,
        hora_fin=comisiones[0].hora_fin,
    )
    second = Comision(
        id_comision="C998",
        materia="Materia B",
        carrera="Carrera de prueba",
        cantidad_estudiantes=49,
        dia="Jueves",
        hora_inicio=first.hora_inicio,
        hora_fin=first.hora_fin,
    )

    report, _ = DetectConflictsUseCase().execute((first, second), aulas)

    assert any(conflict.code == "SIMULTANEOUS_ROOM_SHORTAGE" for conflict in report.errors)


def test_superposicion_sin_falta_de_aulas_es_advertencia() -> None:
    comisiones, aulas = _valid_data()

    report, _ = DetectConflictsUseCase().execute(comisiones, aulas)

    assert any(conflict.code == "TIME_OVERLAP" for conflict in report.warnings)

