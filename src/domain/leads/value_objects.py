import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ContactInfo:
    """Value Object con los datos de contacto de un lead."""

    name: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None


@dataclass(frozen=True)
class LeadSubmissionResult:
    """Resultado inmutable de un envío de lead.

    Attributes:
        status: Estado general de la operación ("success" o "partial_success").
        lead_id: Identificador del lead persistido.
        notifications: Canales de notificación que se ejecutaron correctamente.
        errors: Errores ocurridos durante notificaciones u otras acciones no críticas.
        request_id: Identificador único de la solicitud de procesamiento.
    """

    status: str
    lead_id: str
    notifications: list[str] = field(default_factory=lambda: list[str]())
    errors: list[str] = field(default_factory=lambda: list[str]())
    request_id: str = field(default_factory=lambda: f"req_{uuid.uuid4().hex[:8]}")

    @property
    def submission_id(self) -> str:
        return self.lead_id

    @property
    def submit_status(self) -> str:
        return self.status
