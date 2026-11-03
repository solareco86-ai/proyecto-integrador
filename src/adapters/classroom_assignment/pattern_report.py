"""Generación de un informe Markdown de patrones observados en los grafos."""

from pathlib import Path

from src.domain.classroom_assignment.assignment import AssignmentResult
from src.domain.classroom_assignment.conflicts import ConflictReport
from src.domain.classroom_assignment.graph import CompatibilityGraph, OverlapGraph


def write_pattern_report(
    report: ConflictReport,
    overlap_graph: OverlapGraph,
    compatibility_graph: CompatibilityGraph,
    path: Path,
    assignment: AssignmentResult | None = None,
) -> None:
    """Escribe indicadores iniciales para interpretar los grafos exportados."""
    lines = _build_report_lines(report, overlap_graph, compatibility_graph, assignment)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _build_report_lines(
    report: ConflictReport,
    overlap_graph: OverlapGraph,
    compatibility_graph: CompatibilityGraph,
    assignment: AssignmentResult | None,
) -> list[str]:
    overlap_degrees = {node: 0 for node in overlap_graph.nodes}
    for first, second in overlap_graph.edges:
        overlap_degrees[first] += 1
        overlap_degrees[second] += 1
    compatible_degrees = {node: 0 for node in compatibility_graph.commission_nodes}
    room_degrees = {node: 0 for node in compatibility_graph.room_nodes}
    for commission, room in compatibility_graph.edges:
        compatible_degrees[commission] += 1
        room_degrees[room] += 1

    busiest_commissions = _top_nodes(overlap_degrees)
    most_compatible_rooms = _top_nodes(room_degrees)
    without_room = [node for node, degree in compatible_degrees.items() if degree == 0]

    return [
        "# Informe inicial de patrones: asignación de aulas",
        "",
        "> Este informe se generó a partir de datos sintéticos. No representa una conclusión institucional.",
        "",
        *_summary_lines(report, overlap_graph, compatibility_graph, assignment),
        *_pattern_lines(busiest_commissions, most_compatible_rooms, without_room, assignment),
        *_decision_lines(),
    ]


def _summary_lines(
    report: ConflictReport,
    overlap_graph: OverlapGraph,
    compatibility_graph: CompatibilityGraph,
    assignment: AssignmentResult | None,
) -> list[str]:
    lines = [
        "## Resumen", "", f"- Conflictos bloqueantes: **{len(report.errors)}**",
        f"- Advertencias: **{len(report.warnings)}**", f"- Comisiones: **{len(overlap_graph.nodes)}**",
        f"- Aulas: **{len(compatibility_graph.room_nodes)}**",
        f"- Relaciones de superposición: **{len(overlap_graph.edges)}**",
        f"- Relaciones comisión-aula compatibles: **{len(compatibility_graph.edges)}**",
    ]
    if assignment is not None:
        lines.extend([
            f"- Comisiones asignadas: **{len(assignment.assignments)}**",
            f"- Comisiones sin asignar: **{len(assignment.unassigned)}**",
        ])
    return [*lines, ""]


def _pattern_lines(
    busiest_commissions: list[tuple[str, int]],
    most_compatible_rooms: list[tuple[str, int]],
    without_room: list[str],
    assignment: AssignmentResult | None,
) -> list[str]:
    unassigned = (
        [f"- `{item.id_sesion}` ({item.id_comision}): {item.reason}" for item in assignment.unassigned]
        if assignment is not None and assignment.unassigned
        else ["- Todas las sesiones recibieron un aula en el matching."]
    )
    return [
        "## Patrones observados", "", "### Superposición horaria", "",
        *_format_ranking("Comisiones con más superposiciones", busiest_commissions), "",
        "### Compatibilidad comisión-aula", "",
        *_format_ranking("Aulas compatibles con más comisiones", most_compatible_rooms), "",
        "### Comisiones sin aula compatible", "",
        f"- {', '.join(without_room) if without_room else 'No se encontraron comisiones sin aula compatible.'}",
        "", "### Sesiones sin asignación", "", *unassigned, "",
    ]


def _decision_lines() -> list[str]:
    return [
        "## Decisiones tomadas", "",
        "1. Una superposición horaria se informa como advertencia porque puede resolverse usando aulas distintas.",
        "2. La falta de un aula compatible se informa como conflicto bloqueante.",
        "3. Los grafos se exportan en GraphML para poder abrirlos en Gephi, y en DOT para renderizarlos con Graphviz.",
        "4. Los patrones son indicadores para orientar el análisis; no constituyen todavía una asignación óptima.",
    ]


def _top_nodes(degrees: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(degrees.items(), key=lambda item: (-item[1], item[0]))[:5]


def _format_ranking(title: str, ranking: list[tuple[str, int]]) -> list[str]:
    lines = [f"**{title}:**"]
    lines.extend(f"- `{node}`: {degree}" for node, degree in ranking if degree > 0)
    if len(lines) == 1:
        lines.append("- No hay relaciones para analizar.")
    return lines
