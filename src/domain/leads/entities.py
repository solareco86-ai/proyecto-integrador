"""Entidad de dominio Lead del sistema de captación de leads."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from src.domain.leads.value_objects import ContactInfo


@dataclass
class Lead:
    """Lead captado a través del formulario de contacto."""

    id: UUID
    contact: ContactInfo
    comment: str
    preferred_contact_channel: str = "whatsapp"
    page_location: str | None = None
    traffic_source: str | None = None
    user_agent: str | None = None
    geographic_location: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    captcha_token: str | None = None
    gclid: str | None = None
    fbclid: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    lead_source: str | None = None

    @classmethod
    def create(
        cls,
        contact: ContactInfo,
        comment: str,
        preferred_contact_channel: str = "whatsapp",
        **kwargs: Any,
    ) -> "Lead":
        """Crea una instancia de Lead con un id nuevo."""
        return cls(
            id=uuid4(),
            contact=contact,
            comment=comment,
            preferred_contact_channel=preferred_contact_channel,
            **kwargs,
        )
