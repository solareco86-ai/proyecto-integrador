import logging
from datetime import UTC, datetime
from uuid import uuid4

from src.application.dtos.lead_dto import ContactSubmitPayload
from src.domain.entities.lead import Lead
from src.domain.value_objects.contact_info import ContactInfo

logger = logging.getLogger(__name__)


def payload_to_lead(payload: ContactSubmitPayload) -> Lead:
    """Traduce el payload de entrada del formulario en una entidad de dominio Lead."""
    logger.debug("[lead_mapper] Mapeando ContactSubmitPayload a Lead")

    lead = Lead(
        id=uuid4(),
        contact=ContactInfo(
            name=payload.name,
            first_name=payload.firstName,
            last_name=payload.lastName,
            email=payload.email,
            phone=payload.phone,
            company=payload.company,
        ),
        comment=payload.comment,
        preferred_contact_channel=payload.preferredContactChannel or "whatsapp",
        page_location=payload.pageLocation,
        traffic_source=payload.trafficSource,
        user_agent=payload.userAgent,
        geographic_location=payload.geographicLocation,
        created_at=datetime.now(UTC),
        captcha_token=payload.captchaToken,
        gclid=payload.gclid,
        fbclid=payload.fbclid,
        utm_source=payload.utmSource,
        utm_medium=payload.utmMedium,
        utm_campaign=payload.utmCampaign,
        lead_source=payload.leadSource,
    )

    logger.debug(
        "[lead_mapper] Lead generado: id=%s, canales=%s, page=%s",
        str(lead.id),
        lead.preferred_contact_channel,
        lead.page_location,
    )
    return lead
