"""Asignación de aulas mediante matching con intervalos horarios."""

from collections.abc import Iterable
from dataclasses import dataclass

from src.domain.classroom_assignment.entities import Aula, Comision, room_can_host


@dataclass(frozen=True)
class RoomAssignment:
    """Asignación concreta de una comisión a un aula."""

    id_comision: str
    id_sesion: str
    id_aula: str
    dia: str
    hora_inicio: str
    hora_fin: str


@dataclass(frozen=True)
class UnassignedCommission:
    """Comisión que no pudo ser asignada en su franja horaria."""

    id_comision: str
    id_sesion: str
    reason: str


@dataclass(frozen=True)
class AssignmentResult:
    """Resultado del matching de comisiones y aulas."""

    assignments: tuple[RoomAssignment, ...]
    unassigned: tuple[UnassignedCommission, ...]

    @property
    def is_complete(self) -> bool:
        """Indica si todas las comisiones recibieron un aula."""
        return not self.unassigned


def assign_rooms(comisiones: Iterable[Comision], aulas: Iterable[Aula]) -> AssignmentResult:
    """Asigna aulas compatibles sin reutilizarlas durante intervalos superpuestos."""
    commission_list = tuple(comisiones)
    room_list = tuple(aulas)
    assignments: list[RoomAssignment] = []
    unassigned: list[UnassignedCommission] = []

    groups = _group_by_day(commission_list)
    for group in groups.values():
        candidates = {
            commission.id_sesion: tuple(
                room.id_aula for room in room_list if room_can_host(room, commission)
            )
            for commission in group
        }
        matching = _maximum_interval_matching(group, candidates)
        for commission in group:
            room_id = matching.get(commission.id_sesion)
            if room_id is None:
                reason = (
                    "No existe un aula compatible disponible en este intervalo."
                    if candidates[commission.id_sesion]
                    else "No existe un aula con capacidad suficiente."
                )
                unassigned.append(UnassignedCommission(commission.id_comision, commission.id_sesion, reason))
                continue
            assignments.append(
                RoomAssignment(
                    id_comision=commission.id_comision,
                    id_sesion=commission.id_sesion,
                    id_aula=room_id,
                    dia=commission.dia,
                    hora_inicio=commission.hora_inicio.strftime("%H:%M"),
                    hora_fin=commission.hora_fin.strftime("%H:%M"),
                )
            )
    assignments.sort(key=lambda item: item.id_sesion)
    unassigned.sort(key=lambda item: item.id_sesion)
    return AssignmentResult(tuple(assignments), tuple(unassigned))


def _group_by_day(comisiones: tuple[Comision, ...]) -> dict[str, tuple[Comision, ...]]:
    groups: dict[str, list[Comision]] = {}
    for commission in comisiones:
        key = commission.dia
        groups.setdefault(key, []).append(commission)
    return {
        key: tuple(sorted(value, key=lambda item: (item.hora_inicio, item.hora_fin, item.id_sesion)))
        for key, value in groups.items()
    }


def _maximum_interval_matching(
    commissions: tuple[Comision, ...], candidates: dict[str, tuple[str, ...]]
) -> dict[str, str]:
    """Busca un matching máximo respetando superposiciones parciales."""
    ordered = tuple(sorted(commissions, key=lambda item: (len(candidates[item.id_sesion]), item.hora_inicio, item.id_sesion)))
    best: dict[str, str] = {}

    def visit(index: int, assigned: dict[str, str]) -> None:
        nonlocal best
        if len(assigned) > len(best):
            best = dict(assigned)
        if index >= len(ordered) or len(assigned) + len(ordered) - index <= len(best):
            return

        commission = ordered[index]
        for room_id in candidates[commission.id_sesion]:
            if _room_is_available(room_id, commission, assigned, ordered):
                assigned[commission.id_sesion] = room_id
                visit(index + 1, assigned)
                del assigned[commission.id_sesion]
        visit(index + 1, assigned)

    visit(0, {})
    return best


def _room_is_available(
    room_id: str,
    commission: Comision,
    assigned: dict[str, str],
    commissions: tuple[Comision, ...],
) -> bool:
    by_session = {item.id_sesion: item for item in commissions}
    return all(
        assigned_session != room_id or not _overlaps(commission, by_session[session_id])
        for session_id, assigned_session in assigned.items()
    )


def _overlaps(first: Comision, second: Comision) -> bool:
    return first.hora_inicio < second.hora_fin and second.hora_inicio < first.hora_fin

