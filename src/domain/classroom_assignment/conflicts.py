"""Detección de conflictos de capacidad y simultaneidad."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import time
from itertools import combinations
from typing import Literal

from src.domain.classroom_assignment.compatibility import room_can_host
from src.domain.classroom_assignment.entities import Aula, Comision

ConflictSeverity = Literal["error", "warning"]


@dataclass(frozen=True)
class Conflict:
    """Conflicto o advertencia explicable para una o más comisiones."""

    code: str
    severity: ConflictSeverity
    message: str
    comision_ids: tuple[str, ...]
    aula_ids: tuple[str, ...] = ()
    dia: str | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None


@dataclass(frozen=True)
class ConflictReport:
    """Resultado del análisis de conflictos."""

    conflicts: tuple[Conflict, ...]

    @property
    def errors(self) -> tuple[Conflict, ...]:
        """Devuelve solamente los conflictos que impiden una asignación."""
        return tuple(conflict for conflict in self.conflicts if conflict.severity == "error")

    @property
    def warnings(self) -> tuple[Conflict, ...]:
        """Devuelve advertencias útiles para análisis y visualizaciones."""
        return tuple(conflict for conflict in self.conflicts if conflict.severity == "warning")

    @property
    def is_feasible(self) -> bool:
        """Indica si no se detectaron conflictos que impidan asignar."""
        return not self.errors


def detect_conflicts(comisiones: Iterable[Comision], aulas: Iterable[Aula]) -> ConflictReport:
    """Detecta falta de capacidad y competencia por aulas en horarios superpuestos.

    La superposición de horarios se informa como advertencia porque no es un
    problema por sí misma: dos comisiones pueden cursar simultáneamente si
    existen aulas diferentes. Se convierte en error cuando no existe una
    asignación posible de aulas compatibles para el grupo simultáneo.
    """
    commission_list = tuple(comisiones)
    room_list = tuple(aulas)
    conflicts: list[Conflict] = []
    compatible_rooms = {
        commission.id_sesion: tuple(
            room.id_aula for room in room_list if room_can_host(room, commission)
        )
        for commission in commission_list
    }

    for commission in commission_list:
        candidates = compatible_rooms[commission.id_sesion]
        if not candidates:
            conflicts.append(
                Conflict(
                    code="NO_COMPATIBLE_ROOM",
                    severity="error",
                    message=(
                        f"La sesión '{commission.id_sesion}' no tiene un aula compatible."
                    ),
                    comision_ids=(commission.id_sesion,),
                    dia=commission.dia,
                    hora_inicio=commission.hora_inicio,
                    hora_fin=commission.hora_fin,
                )
            )

    for first, second in combinations(commission_list, 2):
        if first.dia != second.dia or not _overlaps(first, second):
            continue
        shared_candidate_rooms = tuple(
            sorted(set(compatible_rooms[first.id_sesion]) | set(compatible_rooms[second.id_sesion]))
        )
        conflicts.append(
            Conflict(
                code="TIME_OVERLAP",
                severity="warning",
                message="Las comisiones se dictan simultáneamente y necesitan aulas diferentes.",
                comision_ids=(first.id_sesion, second.id_sesion),
                aula_ids=shared_candidate_rooms,
                dia=first.dia,
                hora_inicio=max(first.hora_inicio, second.hora_inicio),
                hora_fin=min(first.hora_fin, second.hora_fin),
            )
        )

    conflicts.extend(_detect_room_shortages(commission_list, compatible_rooms))
    return ConflictReport(conflicts=tuple(conflicts))


def _detect_room_shortages(
    commissions: tuple[Comision, ...], compatible_rooms: dict[str, tuple[str, ...]]
) -> list[Conflict]:
    shortages: list[Conflict] = []
    days = {commission.dia for commission in commissions}
    for day in days:
        day_commissions = [commission for commission in commissions if commission.dia == day]
        start_times = {commission.hora_inicio for commission in day_commissions}
        seen_groups: set[tuple[str, ...]] = set()
        for start_time in start_times:
            active = tuple(
                commission
                for commission in day_commissions
                if commission.hora_inicio <= start_time < commission.hora_fin
            )
            if len(active) < 2 or any(not compatible_rooms[item.id_sesion] for item in active):
                continue
            group_ids = tuple(sorted(item.id_sesion for item in active))
            if group_ids in seen_groups:
                continue
            seen_groups.add(group_ids)
            matching = _maximum_room_matching(active, compatible_rooms)
            if matching == len(active):
                continue
            room_ids = tuple(sorted({room for item in active for room in compatible_rooms[item.id_sesion]}))
            shortages.append(
                Conflict(
                    code="SIMULTANEOUS_ROOM_SHORTAGE",
                    severity="error",
                    message=(
                        f"{len(active)} comisiones simultáneas compiten por {len(room_ids)} aulas compatibles."
                    ),
                    comision_ids=group_ids,
                    aula_ids=room_ids,
                    dia=day,
                    hora_inicio=min(item.hora_inicio for item in active),
                    hora_fin=max(item.hora_fin for item in active),
                )
            )
    return shortages


def _maximum_room_matching(
    commissions: tuple[Comision, ...], compatible_rooms: dict[str, tuple[str, ...]]
) -> int:
    room_to_commission: dict[str, str] = {}

    def visit(commission_id: str, visited: set[str]) -> bool:
        for room_id in compatible_rooms[commission_id]:
            if room_id in visited:
                continue
            visited.add(room_id)
            assigned = room_to_commission.get(room_id)
            if assigned is None or visit(assigned, visited):
                room_to_commission[room_id] = commission_id
                return True
        return False

    return sum(visit(commission.id_sesion, set()) for commission in commissions)


def _overlaps(first: Comision, second: Comision) -> bool:
    return first.hora_inicio < second.hora_fin and second.hora_inicio < first.hora_fin

