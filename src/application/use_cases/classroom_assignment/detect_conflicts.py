"""Caso de uso para analizar conflictos antes de asignar aulas."""

from collections.abc import Iterable

from src.domain.classroom_assignment.conflicts import ConflictReport, detect_conflicts
from src.domain.classroom_assignment.entities import Aula, Comision
from src.domain.classroom_assignment.graph import OverlapGraph, build_overlap_graph


class DetectConflictsUseCase:
    """Devuelve conflictos explicables y el grafo de superposiciones."""

    def execute(self, comisiones: Iterable[Comision], aulas: Iterable[Aula]) -> tuple[ConflictReport, OverlapGraph]:
        """Analiza capacidad, simultaneidad y relaciones entre comisiones."""
        commission_list = tuple(comisiones)
        room_list = tuple(aulas)
        return detect_conflicts(commission_list, room_list), build_overlap_graph(commission_list)

