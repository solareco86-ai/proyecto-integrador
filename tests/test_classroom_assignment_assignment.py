"""Pruebas de asignación automática mediante matching."""

import csv
from pathlib import Path

from src.application.use_cases.classroom_assignment.assign_rooms import AssignRoomsUseCase
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


def test_asigna_todas_las_comisiones_sinteticas() -> None:
    comisiones, aulas = _valid_data()

    result = AssignRoomsUseCase().execute(comisiones, aulas)

    assert result.is_complete
    assert len(result.assignments) == 8
    assert {item.id_comision for item in result.assignments} == {item.id_comision for item in comisiones}


def test_reutiliza_un_aula_en_horarios_diferentes() -> None:
    comisiones, aulas = _valid_data()

    result = AssignRoomsUseCase().execute(comisiones, aulas)
    assignments_by_room: dict[str, list[str]] = {}
    for assignment in result.assignments:
        assignments_by_room.setdefault(assignment.id_aula, []).append(assignment.id_comision)

    assert any(len(commission_ids) > 1 for commission_ids in assignments_by_room.values())


def test_informa_comision_sin_aula_por_capacidad() -> None:
    comisiones, aulas = _valid_data()
    impossible = Comision(
        id_comision="C999",
        materia="Materia grande",
        carrera="Carrera de prueba",
        cantidad_estudiantes=100,
        dia="Jueves",
        hora_inicio=comisiones[0].hora_inicio,
        hora_fin=comisiones[0].hora_fin,
    )

    result = AssignRoomsUseCase().execute((*comisiones, impossible), aulas)

    assert not result.is_complete
    assert result.unassigned[0].id_comision == "C999"
    assert "capacidad" in result.unassigned[0].reason


def test_matching_resuelve_dos_comisiones_que_comparten_alternativas() -> None:
    comisiones, aulas = _valid_data()
    first = Comision(
        id_comision="C997",
        materia="Materia A",
        carrera="Carrera de prueba",
        cantidad_estudiantes=45,
        dia="Jueves",
        hora_inicio=comisiones[0].hora_inicio,
        hora_fin=comisiones[0].hora_fin,
    )
    second = Comision(
        id_comision="C998",
        materia="Materia B",
        carrera="Carrera de prueba",
        cantidad_estudiantes=28,
        dia="Jueves",
        hora_inicio=first.hora_inicio,
        hora_fin=first.hora_fin,
    )

    result = AssignRoomsUseCase().execute((first, second), aulas)

    assert result.is_complete
    assert len({item.id_aula for item in result.assignments}) == 2
