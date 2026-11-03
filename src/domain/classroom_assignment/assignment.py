"""Asignación de aulas mediante matching bipartito por franja horaria."""

from collections.abc import Iterable
from dataclasses import dataclass

from src.domain.classroom_assignment.compatibility import room_can_host
from src.domain.classroom_assignment.entities import Aula, Comision


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
    """Asigna aulas compatibles dentro de cada franja horaria exacta.

    El MVP considera una franja como la combinación exacta de día, hora de
    inicio y hora de fin. Las aulas pueden reutilizarse en franjas diferentes.
    Dentro de cada franja se busca un matching máximo entre comisiones y aulas.
    """
    commission_list = tuple(comisiones)
    room_list = tuple(aulas)
    assignments: list[RoomAssignment] = []
    unassigned: list[UnassignedCommission] = []

    groups = _group_by_slot(commission_list)
    for group in groups.values():
        candidates = {
            commission.id_sesion: tuple(
                room.id_aula for room in room_list if room_can_host(room, commission)
            )
            for commission in group
        }
        matching = _maximum_matching(group, candidates)
        for commission in group:
            room_id = matching.get(commission.id_sesion)
            if room_id is None:
                reason = (
                    "No existe un aula compatible disponible en esta franja horaria."
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


def _group_by_slot(comisiones: tuple[Comision, ...]) -> dict[tuple[str, str, str], tuple[Comision, ...]]:
    groups: dict[tuple[str, str, str], list[Comision]] = {}
    for commission in comisiones:
        key = (
            commission.dia,
            commission.hora_inicio.strftime("%H:%M"),
            commission.hora_fin.strftime("%H:%M"),
        )
        groups.setdefault(key, []).append(commission)
    return {key: tuple(value) for key, value in groups.items()}


def _maximum_matching(
    commissions: tuple[Comision, ...], candidates: dict[str, tuple[str, ...]]
) -> dict[str, str]:
    """Encuentra un matching máximo con búsqueda aumentante."""
    room_to_commission: dict[str, str] = {}

    def visit(commission_id: str, visited_rooms: set[str]) -> bool:
        for room_id in candidates[commission_id]:
            if room_id in visited_rooms:
                continue
            visited_rooms.add(room_id)
            assigned_commission = room_to_commission.get(room_id)
            if assigned_commission is None or visit(assigned_commission, visited_rooms):
                room_to_commission[room_id] = commission_id
                return True
        return False

    ordered = sorted(commissions, key=lambda item: (len(candidates[item.id_sesion]), item.id_sesion))
    for commission in ordered:
        visit(commission.id_sesion, set())
    return {session_id: room_id for room_id, session_id in room_to_commission.items()}

