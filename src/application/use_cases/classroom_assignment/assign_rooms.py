"""Caso de uso para generar una propuesta de asignación."""

from collections.abc import Iterable

from src.domain.classroom_assignment.assignment import AssignmentResult, assign_rooms
from src.domain.classroom_assignment.entities import Aula, Comision


class AssignRoomsUseCase:
    """Genera una propuesta explicable de aulas por franja horaria."""

    def execute(self, comisiones: Iterable[Comision], aulas: Iterable[Aula]) -> AssignmentResult:
        """Busca un matching máximo para cada franja horaria exacta."""
        return assign_rooms(tuple(comisiones), tuple(aulas))

