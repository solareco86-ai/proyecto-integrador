"""Entidades puras del dominio de asignación de aulas."""

from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class Aula:
    """Aula disponible para una o más comisiones."""

    id_aula: str
    nombre: str
    capacidad: int
    edificio: str
    tipo_aula: str = "aula_comun"
    equipamiento: tuple[str, ...] = ()


@dataclass(frozen=True)
class Comision:
    """Comisión con horario previamente definido."""

    id_comision: str
    id_sesion: str
    materia: str
    carrera: str
    cantidad_estudiantes: int
    dia: str
    hora_inicio: time
    hora_fin: time
    requerimientos: tuple[str, ...] = ()


def room_can_host(room: Aula, commission: Comision) -> bool:
    """Indica si un aula cumple capacidad, tipo y equipamiento requerido."""
    if room.capacidad < commission.cantidad_estudiantes:
        return False
    available = {room.tipo_aula, *room.equipamiento}
    return set(commission.requerimientos).issubset(available)

