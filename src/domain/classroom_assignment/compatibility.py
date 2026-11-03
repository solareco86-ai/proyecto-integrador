"""Reglas compartidas para decidir si un aula puede recibir una sesión."""

from src.domain.classroom_assignment.entities import Aula, Comision


def room_can_host(room: Aula, commission: Comision) -> bool:
    """Indica si capacidad y recursos del aula satisfacen la comisión."""
    if room.capacidad < commission.cantidad_estudiantes:
        return False
    available_capabilities = {room.tipo_aula, *room.equipamiento}
    return set(commission.requerimientos).issubset(available_capabilities)
