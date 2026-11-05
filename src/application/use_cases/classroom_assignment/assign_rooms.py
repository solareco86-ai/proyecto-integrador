"""Caso de uso para generar una propuesta de asignación."""

from collections.abc import Iterable

from src.domain.classroom_assignment.assignment import AssignmentResult, assign_rooms
from src.domain.classroom_assignment.entities import Aula, Comision


class AssignRoomsUseCase:
    """Genera una propuesta explicable de aulas por intervalos horarios."""

    def execute(self, comisiones: Iterable[Comision], aulas: Iterable[Aula]) -> AssignmentResult:
        """Busca un matching máximo sin reutilizar aulas en intervalos superpuestos."""
        return assign_rooms(tuple(comisiones), tuple(aulas))

    def execute_for_session(self, comision: Comision, aulas: Iterable[Aula]) -> AssignmentResult:
        """Permite consultar la asignación de una sesión durante una revisión manual."""
        return self.execute((comision,), aulas)

