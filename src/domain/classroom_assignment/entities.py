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
    equipamiento: tuple[str, ...] = ()


@dataclass(frozen=True)
class Comision:
    """Comisión con horario previamente definido."""

    id_comision: str
    materia: str
    carrera: str
    cantidad_estudiantes: int
    dia: str
    hora_inicio: time
    hora_fin: time

