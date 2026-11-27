from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class Respuesta:
    texto: str
    intencion: str
    fuentes: list[str]
    confianza: float
    creado_en: datetime = field(default_factory=lambda: datetime.now(UTC))
