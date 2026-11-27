from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class Consulta:
    mensaje: str
    session_id: str
    creado_en: datetime = field(default_factory=lambda: datetime.now(UTC))
