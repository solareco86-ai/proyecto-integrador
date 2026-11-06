"""Exportación de resultados de asignación a CSV."""

import csv
from pathlib import Path

from src.domain.classroom_assignment.assignment import AssignmentResult


def export_assignments_csv(result: AssignmentResult, path: Path) -> None:
    """Guarda las asignaciones exitosas en un CSV."""
    fieldnames = ("id_comision", "id_sesion", "id_aula", "dia", "hora_inicio", "hora_fin")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(
            {
                "id_comision": assignment.id_comision,
                "id_sesion": assignment.id_sesion,
                "id_aula": assignment.id_aula,
                "dia": assignment.dia,
                "hora_inicio": assignment.hora_inicio,
                "hora_fin": assignment.hora_fin,
            }
            for assignment in result.assignments
        )


def export_unassigned_csv(result: AssignmentResult, path: Path) -> None:
    """Guarda las comisiones que no pudieron asignarse y el motivo."""
    fieldnames = ("id_comision", "id_sesion", "motivo")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(
            {
                "id_comision": item.id_comision,
                "id_sesion": item.id_sesion,
                "motivo": item.reason,
            }
            for item in result.unassigned
        )
