"""Prueba end-to-end del flujo completo de asignación de aulas."""

import csv
from pathlib import Path

from src.adapters.classroom_assignment.assignment_exporter import (
    export_assignments_csv,
    export_unassigned_csv,
)
from src.adapters.classroom_assignment.csv_reader import read_csv_rows
from src.adapters.classroom_assignment.graph_exporter import (
    export_compatibility_dot,
    export_compatibility_graphml,
    export_overlap_dot,
    export_overlap_graphml,
)
from src.adapters.classroom_assignment.pattern_report import write_pattern_report
from src.application.use_cases.classroom_assignment.assign_rooms import AssignRoomsUseCase
from src.application.use_cases.classroom_assignment.detect_conflicts import DetectConflictsUseCase
from src.application.use_cases.classroom_assignment.validate_input_data import ValidateInputDataUseCase
from src.domain.classroom_assignment.graph import build_compatibility_graph

DATA_DIR = Path(__file__).parents[1] / "data" / "asignacion_aulas"


def test_ejecuta_flujo_completo_y_exporta_resultados(tmp_path: Path) -> None:
    aulas_rows = read_csv_rows(DATA_DIR / "aulas.csv")
    comisiones_rows = read_csv_rows(DATA_DIR / "comisiones.csv")

    validation = ValidateInputDataUseCase().execute(aulas_rows, comisiones_rows)
    assert validation.is_valid

    conflict_report, overlap_graph = DetectConflictsUseCase().execute(
        validation.comisiones,
        validation.aulas,
    )
    assert any(conflict.code == "SIMULTANEOUS_ROOM_SHORTAGE" for conflict in conflict_report.errors)

    assignment = AssignRoomsUseCase().execute(validation.comisiones, validation.aulas)
    compatibility_graph = build_compatibility_graph(validation.comisiones, validation.aulas)

    assignments_path = tmp_path / "asignaciones.csv"
    unassigned_path = tmp_path / "comisiones-sin-asignar.csv"
    overlap_graphml_path = tmp_path / "grafo-superposicion.graphml"
    compatibility_graphml_path = tmp_path / "grafo-comision-aula.graphml"
    overlap_dot_path = tmp_path / "grafo-superposicion.dot"
    compatibility_dot_path = tmp_path / "grafo-comision-aula.dot"
    report_path = tmp_path / "patrones.md"

    export_assignments_csv(assignment, assignments_path)
    export_unassigned_csv(assignment, unassigned_path)
    export_overlap_graphml(overlap_graph, overlap_graphml_path)
    export_compatibility_graphml(compatibility_graph, compatibility_graphml_path)
    export_overlap_dot(overlap_graph, overlap_dot_path)
    export_compatibility_dot(compatibility_graph, compatibility_dot_path)
    write_pattern_report(
        conflict_report,
        overlap_graph,
        compatibility_graph,
        report_path,
        assignment,
    )

    expected_files = (
        assignments_path,
        unassigned_path,
        overlap_graphml_path,
        compatibility_graphml_path,
        overlap_dot_path,
        compatibility_dot_path,
        report_path,
    )
    assert all(path.exists() for path in expected_files)

    with assignments_path.open(encoding="utf-8", newline="") as file:
        assignments_rows = list(csv.DictReader(file))
    with unassigned_path.open(encoding="utf-8", newline="") as file:
        unassigned_rows = list(csv.DictReader(file))

    assert len(assignments_rows) == len(assignment.assignments)
    assert len(unassigned_rows) == len(assignment.unassigned)
    assert "S008" in {row["id_sesion"] for row in unassigned_rows}
    assert "<graphml" in overlap_graphml_path.read_text(encoding="utf-8")
    assert "graph superposicion" in overlap_dot_path.read_text(encoding="utf-8")
    assert "# Informe inicial de patrones" in report_path.read_text(encoding="utf-8")
