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
    optimal: bool = True
    search_nodes: int = 0
    limit_reached: bool = False

    @property
    def is_complete(self) -> bool:
        """Indica si todas las comisiones recibieron un aula."""
        return not self.unassigned


@dataclass(frozen=True)
class MatchingConfig:
    """Límites deterministas para evitar exploraciones no acotadas."""

    max_search_nodes: int = 100_000


def assign_rooms(
    comisiones: Iterable[Comision],
    aulas: Iterable[Aula],
    config: MatchingConfig = MatchingConfig(),
) -> AssignmentResult:
    """Asigna aulas compatibles sin reutilizarlas durante intervalos superpuestos."""
    commission_list = tuple(comisiones)
    room_list = tuple(aulas)
    assignments: list[RoomAssignment] = []
    unassigned: list[UnassignedCommission] = []
    optimal = True
    search_nodes = 0
    limit_reached = False

    groups = _group_by_day(commission_list)
    for group in groups.values():
        candidates = {
            commission.id_sesion: tuple(
                room.id_aula for room in room_list if room_can_host(room, commission)
            )
            for commission in group
        }
        matching = _maximum_interval_matching(group, candidates, config)
        optimal = optimal and matching.optimal
        search_nodes += matching.search_nodes
        limit_reached = limit_reached or matching.limit_reached
        for commission in group:
            room_id = matching.assignments.get(commission.id_sesion)
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
    return AssignmentResult(
        tuple(assignments),
        tuple(unassigned),
        optimal=optimal,
        search_nodes=search_nodes,
        limit_reached=limit_reached,
    )


def _group_by_day(comisiones: tuple[Comision, ...]) -> dict[str, tuple[Comision, ...]]:
    groups: dict[str, list[Comision]] = {}
    for commission in comisiones:
        key = commission.dia
        groups.setdefault(key, []).append(commission)
    return {
        key: tuple(sorted(value, key=lambda item: (item.hora_inicio, item.hora_fin, item.id_sesion)))
        for key, value in groups.items()
    }


@dataclass(frozen=True)
class _MatchingSearchResult:
    assignments: dict[str, str]
    optimal: bool
    search_nodes: int
    limit_reached: bool


def _maximum_interval_matching(
    commissions: tuple[Comision, ...],
    candidates: dict[str, tuple[str, ...]],
    config: MatchingConfig,
) -> _MatchingSearchResult:
    """Busca un matching máximo respetando superposiciones parciales."""
    ordered = tuple(sorted(commissions, key=lambda item: (len(candidates[item.id_sesion]), item.hora_inicio, item.id_sesion)))
    best: dict[str, str] = {}
    by_session = {commission.id_sesion: commission for commission in ordered}
    assigned_by_room: dict[str, list[str]] = {}
    search_nodes = 0
    limit_reached = False

    def visit(index: int, assigned: dict[str, str]) -> None:
        nonlocal best, search_nodes, limit_reached
        if search_nodes >= config.max_search_nodes:
            limit_reached = True
            return
        search_nodes += 1
        if len(assigned) > len(best):
            best = dict(assigned)
        if index >= len(ordered) or len(assigned) + len(ordered) - index <= len(best):
            return

        commission = ordered[index]
        for room_id in candidates[commission.id_sesion]:
            if _room_is_available(room_id, commission, assigned_by_room, by_session):
                assigned[commission.id_sesion] = room_id
                assigned_by_room.setdefault(room_id, []).append(commission.id_sesion)
                visit(index + 1, assigned)
                assigned_by_room[room_id].pop()
                if not assigned_by_room[room_id]:
                    del assigned_by_room[room_id]
                del assigned[commission.id_sesion]
        visit(index + 1, assigned)

    visit(0, {})
    return _MatchingSearchResult(best, not limit_reached, search_nodes, limit_reached)


def _room_is_available(
    room_id: str,
    commission: Comision,
    assigned_by_room: dict[str, list[str]],
    by_session: dict[str, Comision],
) -> bool:
    return all(
        not _overlaps(commission, by_session[session_id])
        for session_id in assigned_by_room.get(room_id, ())
    )


def _overlaps(first: Comision, second: Comision) -> bool:
    return first.hora_inicio < second.hora_fin and second.hora_inicio < first.hora_fin

