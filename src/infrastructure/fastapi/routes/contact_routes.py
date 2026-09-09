from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_contenido
from src.application.dtos import (
    ContactSubmitPayload,
    ContenidoModel,
    DirectContactPayload,
    WhatsAppClickPayload,
)
from src.application.gateways.notification_gateway import NotificationGateway
from src.application.use_cases.submit_lead import SubmitLeadInput, SubmitLeadUseCase
from src.domain.entities.lead import Lead
from src.domain.repositories.lead_repository import LeadRepository
from src.domain.value_objects.contact_info import ContactInfo
from src.infrastructure.fastapi.dependencies import (
    get_contenido,
    get_lead_repository,
    get_notification_gateway,
    templates,
)
from src.infrastructure.fastapi.metrics import registry
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

router = APIRouter()
logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)


@router.get("/contact")
async def contact_page(request: Request, contenido: ContenidoModel = Depends(get_contenido)):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    contact_data = content_data["contact"]

    base_seo: dict[str, Any] = presented["seo"]
    seo: dict[str, Any] = {
        **base_seo,
        "title": f"{contact_data['title']} | {brand_data['brandName']}",
        "description": contact_data["subtitle"],
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "seo": seo,
        "footer": presented.get("footer"),
        "contact_hero": {
            "title": f"{contact_data['title']} con {brand_data['brandName']}",
            "subtitle": contact_data["subtitle"],
        },
    }
    return templates.TemplateResponse(request=request, name="contact.html", context=context)


@router.post("/api/v1/contact", status_code=201)
async def submit_contact(
    request: Request,
    payload: ContactSubmitPayload,
    repository: LeadRepository = Depends(get_lead_repository),
    notification_gateway: NotificationGateway = Depends(get_notification_gateway),
):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info("[submit_contact] Recibiendo POST /api/v1/contact (request_id=%s)", request_id)
    logger.debug(
        "[submit_contact] Payload validado: name presente=%s, email presente=%s, phone presente=%s",
        bool(payload.name),
        bool(payload.email),
        bool(payload.phone),
    )

    try:
        use_case = SubmitLeadUseCase(repository=repository, notification_gateway=notification_gateway)
        lead_input = SubmitLeadInput(
            name=payload.name,
            comment=payload.comment,
            first_name=payload.firstName,
            last_name=payload.lastName,
            email=payload.email,
            phone=payload.phone,
            company=payload.company,
            preferred_contact_channel=payload.preferredContactChannel,
            page_location=payload.pageLocation,
            traffic_source=payload.trafficSource,
            user_agent=payload.userAgent,
            geographic_location=payload.geographicLocation,
            captcha_token=payload.captchaToken,
            gclid=payload.gclid,
            fbclid=payload.fbclid,
            utm_source=payload.utmSource,
            utm_medium=payload.utmMedium,
            utm_campaign=payload.utmCampaign,
            lead_source=payload.leadSource,
            honeypot=payload.website_url_hp,
        )
        result = await use_case.execute(lead_input)
        logger.info(
            "[submit_contact] Lead procesado: submission_id=%s, status=%s, request_id=%s",
            result.submission_id,
            result.submit_status,
            request_id,
        )
        registry.leads_created_total.inc()
        if result.submit_status == "partial_success":
            registry.smtp_send_failures_total.inc()
        return {
            "requestId": result.request_id,
            "submissionId": result.submission_id,
            "submitStatus": result.submit_status,
        }
    except Exception:
        logger.exception("[submit_contact] Error inesperado al procesar lead (request_id=%s)", request_id)
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/api/v1/events/whatsapp-click", status_code=200)
async def track_whatsapp_click(
    request: Request,
    payload: WhatsAppClickPayload | None = None,
    repository: LeadRepository = Depends(get_lead_repository),
    notification_gateway: NotificationGateway = Depends(get_notification_gateway),
) -> dict[str, Any]:
    logger.info("[track_whatsapp_click] Recibiendo evento click en WhatsApp")
    page_url = (payload and payload.pageLocation) or request.headers.get("referer", "No especificada")
    traffic = (payload and payload.trafficSource) or "Botón WhatsApp CTA"
    element = (payload and payload.element) or "Botón Flotante (FAB)"
    user_agent = request.headers.get("user-agent", "No especificado")
    cookie_consent = payload.cookieConsent if payload else None

    # 1. Persistir el evento de clic en la base de datos de leads
    lead_id: str | None = None
    try:
        lead = Lead.create(
            contact=ContactInfo(
                name=f"⚡ Clic en {element}",
                email=None,
                phone=None,
                company=None,
            ),
            comment=f"Usuario hizo clic en {element} desde la página: {page_url}",
            preferred_contact_channel="whatsapp",
            page_location=page_url,
            traffic_source=traffic,
            user_agent=user_agent,
            gclid=payload.gclid if payload else None,
            utm_source=payload.utmSource if payload else None,
            utm_medium=payload.utmMedium if payload else None,
            utm_campaign=payload.utmCampaign if payload else None,
            lead_source="whatsapp_cta",
        )
        await repository.save(lead)
        lead_id = f"lead_{lead.id}"
        registry.leads_created_total.inc()
        logger.info("[track_whatsapp_click] Clic WhatsApp persistido: lead_id=%s", lead_id)
    except Exception as e:
        logger.warning("[track_whatsapp_click] Error no bloqueante al persistir clic WhatsApp: %s", e)

    # 2. Notificación instantánea a Telegram (formato conciso para eventos)
    click_data: dict[str, Any] = {
        "page_location": page_url,
        "traffic_source": traffic,
        "element": element,
        "cookie_consent": cookie_consent,
        "user_agent": user_agent,
        "utm_source": payload.utmSource if payload else None,
        "utm_medium": payload.utmMedium if payload else None,
        "utm_campaign": payload.utmCampaign if payload else None,
        "gclid": payload.gclid if payload else None,
    }

    try:
        await notification_gateway.notify_whatsapp_click(click_data)
    except Exception as e:
        logger.warning("[track_whatsapp_click] Error no bloqueante al notificar evento WhatsApp: %s", e)

    response_data: dict[str, Any] = {"status": "ok", "tracked": True}
    if lead_id:
        response_data["leadId"] = lead_id
    return response_data


@router.post("/api/v1/events/direct-contact", status_code=200)
async def track_direct_contact(
    request: Request,
    payload: DirectContactPayload,
    repository: LeadRepository = Depends(get_lead_repository),
    notification_gateway: NotificationGateway = Depends(get_notification_gateway),
) -> dict[str, Any]:
    logger.info("[track_direct_contact] Recibiendo evento contacto directo (%s)", payload.action)
    page_url = payload.pageLocation or request.headers.get("referer", "No especificada")
    traffic = payload.trafficSource or "Directo / Desconocido"
    element = payload.element or "Enlace Directo"
    target_value = payload.targetValue or config.NOTIFICATION_EMAIL
    user_agent = request.headers.get("user-agent", "No especificado")
    cookie_consent = payload.cookieConsent

    # 1. Persistir el evento en la base de datos de leads
    lead_id: str | None = None
    action_desc = {
        "email_click": f"Clic en Email mailto ({target_value})",
        "email_copy": f"Copia de Email al portapapeles ({target_value})",
        "phone_click": f"Clic en Teléfono tel ({target_value})",
        "phone_copy": f"Copia de Teléfono al portapapeles ({target_value})",
    }.get(payload.action, f"Interacción directa ({payload.action}) con {target_value}")

    pref_channel = "email" if "email" in payload.action else "phone"

    try:
        lead = Lead.create(
            contact=ContactInfo(
                name=f"⚡ {action_desc}",
                email=target_value if "email" in payload.action else None,
                phone=target_value if "phone" in payload.action else None,
                company=None,
            ),
            comment=f"Usuario interactuó con datos de contacto ({action_desc}) desde la página: {page_url}",
            preferred_contact_channel=pref_channel,
            page_location=page_url,
            traffic_source=traffic,
            user_agent=user_agent,
            gclid=payload.gclid,
            utm_source=payload.utmSource,
            utm_medium=payload.utmMedium,
            utm_campaign=payload.utmCampaign,
            lead_source=f"direct_contact_{payload.action}",
        )
        await repository.save(lead)
        lead_id = f"lead_{lead.id}"
        registry.leads_created_total.inc()
        logger.info("[track_direct_contact] Evento contacto directo persistido: lead_id=%s", lead_id)
    except Exception as e:
        logger.warning("[track_direct_contact] Error no bloqueante al persistir contacto directo: %s", e)

    # 2. Notificación instantánea a Telegram
    contact_data: dict[str, Any] = {
        "action": payload.action,
        "target_value": target_value,
        "page_location": page_url,
        "traffic_source": traffic,
        "element": element,
        "cookie_consent": cookie_consent,
        "user_agent": user_agent,
        "utm_source": payload.utmSource,
        "utm_medium": payload.utmMedium,
        "utm_campaign": payload.utmCampaign,
        "gclid": payload.gclid,
    }

    try:
        await notification_gateway.notify_direct_contact(contact_data)
    except Exception as e:
        logger.warning("[track_direct_contact] Error no bloqueante al notificar contacto directo: %s", e)

    response_data: dict[str, Any] = {"status": "ok", "tracked": True}
    if lead_id:
        response_data["leadId"] = lead_id
    return response_data
