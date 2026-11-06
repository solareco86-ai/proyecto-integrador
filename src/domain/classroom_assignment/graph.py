"""Modelo de grafo para estudiar superposiciones de comisiones."""

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations

from src.domain.classroom_assignment.entities import Aula, Comision, room_can_host


@dataclass(frozen=True)
class OverlapGraph:
    """Grafo no dirigido de comisiones con horarios superpuestos."""

    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class CompatibilityGraph:
    """Grafo bipartito entre comisiones y aulas compatibles."""

    commission_nodes: tuple[str, ...]
    room_nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]


def build_overlap_graph(comisiones: Iterable[Comision]) -> OverlapGraph:
    """Construye un grafo donde cada arista representa competencia temporal."""
    commission_list = tuple(comisiones)
    edges: list[tuple[str, str]] = []
    for first, second in combinations(commission_list, 2):
        if first.dia == second.dia and _overlaps(first, second):
            edge = (first.id_sesion, second.id_sesion)
            edges.append(edge if edge[0] < edge[1] else (edge[1], edge[0]))
    return OverlapGraph(
        nodes=tuple(commission.id_sesion for commission in commission_list),
        edges=tuple(sorted(edges)),
    )


def build_compatibility_graph(
    comisiones: Iterable[Comision], aulas: Iterable[Aula]
) -> CompatibilityGraph:
    """Conecta una comisión con cada aula que tiene capacidad suficiente."""
    commission_list = tuple(comisiones)
    room_list = tuple(aulas)
    edges = tuple(
        (commission.id_sesion, room.id_aula)
        for commission in commission_list
        for room in room_list
        if room_can_host(room, commission)
    )
    return CompatibilityGraph(
        commission_nodes=tuple(commission.id_sesion for commission in commission_list),
        room_nodes=tuple(room.id_aula for room in room_list),
        edges=edges,
    )


def _overlaps(first: Comision, second: Comision) -> bool:
    return first.hora_inicio < second.hora_fin and second.hora_inicio < first.hora_fin

