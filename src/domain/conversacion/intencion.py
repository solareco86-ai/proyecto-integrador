"""Entidad de dominio que modela la intención detectada en una consulta."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Intencion:
    """Resultado del análisis semántico de una consulta del usuario."""

    nombre: str
    """Nombre canónico de la intención (ej. 'consulta_carreras')."""

    entidades: list[str] = field(default_factory=lambda: list[str]())
    """Entidades extraídas del texto (ej. categorías del léxico)."""

    carrera_detectada: str | None = None
    """Slug de la carrera detectada, si aplica."""

    confianza: float = 0.0
    """Nivel de confianza de la clasificación (0.0 a 1.0)."""
