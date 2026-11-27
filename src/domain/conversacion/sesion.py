import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.domain.conversacion.consulta import Consulta
from src.domain.conversacion.respuesta import Respuesta


@dataclass
class SesionConversacion:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    consultas: list[Consulta] = field(default_factory=lambda: list[Consulta]())
    respuestas: list[Respuesta] = field(default_factory=lambda: list[Respuesta]())
    creado_en: datetime = field(default_factory=lambda: datetime.now(UTC))
