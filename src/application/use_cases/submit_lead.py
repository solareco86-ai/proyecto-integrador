"""Caso de uso para envío de un nuevo lead."""

from dataclasses import dataclass
from typing import Any

from src.application.gateways.notification_gateway import NotificationGateway
from src.domain.entities.lead import Lead
from src.domain.repositories.lead_repository import LeadRepository
from src.domain.value_objects.contact_info import ContactInfo
from src.domain.value_objects.lead_submission_result import LeadSubmissionResult


@dataclass(frozen=True)
class SubmitLeadInput:
    """Datos de entrada del caso de uso, desacoplados de la capa HTTP."""

    name: str
    comment: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    preferred_contact_channel: str | None = "whatsapp"
    page_location: str | None = None
    traffic_source: str | None = None
    user_agent: str | None = None
    geographic_location: str | None = None
    captcha_token: str | None = None
    gclid: str | None = None
    fbclid: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    lead_source: str | None = None
    honeypot: str | None = None


class SubmitLeadUseCase:
    """Orquesta la persistencia y notificación de un lead."""

    def __init__(
        self,
        repository: LeadRepository,
        notification_gateway: NotificationGateway,
    ) -> None:
        self._repository = repository
        self._notification_gateway = notification_gateway

    async def execute(self, input: SubmitLeadInput) -> LeadSubmissionResult:
        """Ejecuta el envío completo: crea la entidad, persiste y notifica."""
        # Protección Honeypot: si el campo señuelo viene completado, descartar silenciosamente
        if input.honeypot and input.honeypot.strip():
            return LeadSubmissionResult(
                status="success",
                lead_id="lead_hp_ignored",
                notifications=["silent_discard"],
                errors=[],
            )

        contact = ContactInfo(
            name=input.name,
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
            phone=input.phone,
            company=input.company,
        )

        lead = Lead.create(
            contact=contact,
            comment=input.comment,
            preferred_contact_channel=input.preferred_contact_channel or "whatsapp",
            page_location=input.page_location,
            traffic_source=input.traffic_source,
            user_agent=input.user_agent,
            geographic_location=input.geographic_location,
            captcha_token=input.captcha_token,
            gclid=input.gclid,
            fbclid=input.fbclid,
            utm_source=input.utm_source,
            utm_medium=input.utm_medium,
            utm_campaign=input.utm_campaign,
            lead_source=input.lead_source,
        )

        await self._repository.save(lead)

        notification_payload: dict[str, Any] = {
            "name": lead.contact.name,
            "email": lead.contact.email,
            "phone": lead.contact.phone,
            "company": lead.contact.company,
            "comment": lead.comment,
            "page_location": lead.page_location,
            "traffic_source": lead.traffic_source,
            "lead_source": lead.lead_source,
            "utm_source": lead.utm_source,
            "utm_medium": lead.utm_medium,
            "utm_campaign": lead.utm_campaign,
            "gclid": lead.gclid,
            "fbclid": lead.fbclid,
        }

        notifications: list[str] = []
        errors: list[str] = []

        try:
            result = await self._notification_gateway.notify_lead(notification_payload)
            if result and result.get("status") in {"sent", "completed"}:
                channel = result.get("channel", "unknown")
                notifications.append(channel)
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

        status = "success" if not errors else "partial_success"
        return LeadSubmissionResult(
            status=status,
            lead_id=f"lead_{lead.id}",
            notifications=notifications,
            errors=errors,
        )
