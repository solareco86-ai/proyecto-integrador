"""Pruebas unitarias de exportadores e informe de patrones de aulas."""

import csv
from pathlib import Path
from xml.etree.ElementTree import parse

from src.adapters.classroom_assignment.assignment_exporter import (
    export_assignments_csv,
    export_unassigned_csv,
)
from src.adapters.classroom_assignment.graph_exporter import (
    export_compatibility_dot,
    export_compatibility_graphml,
    export_overlap_dot,
    export_overlap_graphml,
)
from src.adapters.classroom_assignment.pattern_report import write_pattern_report
from src.domain.classroom_assignment.assignment import (
    AssignmentResult,
    RoomAssignment,
    UnassignedCommission,
)
from src.domain.classroom_assignment.conflicts import Conflict, ConflictReport
from src.domain.classroom_assignment.graph import CompatibilityGraph, OverlapGraph


def _result() -> AssignmentResult:
    return AssignmentResult(
        assignments=(
            RoomAssignment("C1", "S1", "A1", "Lunes", "18:30", "20:00"),
        ),
        unassigned=(
            UnassignedCommission("C2", "S2", "No existe un aula compatible."),
        ),
    )


def _graphs() -> tuple[OverlapGraph, CompatibilityGraph]:
    return (
        OverlapGraph(nodes=("S1", "S2"), edges=(("S1", "S2"),)),
        CompatibilityGraph(
            commission_nodes=("S1", "S2"),
            room_nodes=("A1", "A2"),
            edges=(("S1", "A1"), ("S1", "A2")),
        ),
    )


def test_exporta_asignaciones_csv_con_encabezados_y_datos(tmp_path: Path) -> None:
    path = tmp_path / "asignaciones.csv"

    export_assignments_csv(_result(), path)

    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows == [
        {
            "id_comision": "C1",
            "id_sesion": "S1",
            "id_aula": "A1",
            "dia": "Lunes",
            "hora_inicio": "18:30",
            "hora_fin": "20:00",
        }
    ]


def test_exporta_sesiones_sin_asignar_con_motivo(tmp_path: Path) -> None:
    path = tmp_path / "sin-asignar.csv"

    export_unassigned_csv(_result(), path)

    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows[0]["id_sesion"] == "S2"
    assert rows[0]["motivo"] == "No existe un aula compatible."


def test_exporta_grafos_en_graphml_con_nodos_y_aristas(tmp_path: Path) -> None:
    overlap, compatibility = _graphs()
    overlap_path = tmp_path / "superposicion.graphml"
    compatibility_path = tmp_path / "compatibilidad.graphml"

    export_overlap_graphml(overlap, overlap_path)
    export_compatibility_graphml(compatibility, compatibility_path)

    assert len(parse(overlap_path).findall(".//{*}node")) == 2
    assert len(parse(overlap_path).findall(".//{*}edge")) == 1
    assert len(parse(compatibility_path).findall(".//{*}node")) == 4
    assert len(parse(compatibility_path).findall(".//{*}edge")) == 2


def test_exporta_grafos_dot_con_nombres_y_formas(tmp_path: Path) -> None:
    overlap, compatibility = _graphs()
    overlap_path = tmp_path / "superposicion.dot"
    compatibility_path = tmp_path / "compatibilidad.dot"

    export_overlap_dot(overlap, overlap_path)
    export_compatibility_dot(compatibility, compatibility_path)

    overlap_text = overlap_path.read_text(encoding="utf-8")
    compatibility_text = compatibility_path.read_text(encoding="utf-8")
    assert '"S1" -- "S2"' in overlap_text
    assert '"A1" [shape=box' in compatibility_text
    assert '"S1" -- "A1"' in compatibility_text


def test_informe_de_patrones_resume_conflictos_y_sesiones_sin_aula(
    tmp_path: Path,
) -> None:
    overlap, compatibility = _graphs()
    report = ConflictReport(
        conflicts=(
            Conflict(
                code="TIME_OVERLAP",
                severity="warning",
                message="Superposición",
                comision_ids=("S1", "S2"),
            ),
        )
    )
    path = tmp_path / "patrones.md"

    write_pattern_report(report, overlap, compatibility, path, _result())

    content = path.read_text(encoding="utf-8")
    assert "Conflictos bloqueantes: **0**" in content
    assert "Advertencias: **1**" in content
    assert "Aulas compatibles con más comisiones" in content
    assert "`S2` (C2): No existe un aula compatible." in content
    assert "Los patrones son indicadores" in content

