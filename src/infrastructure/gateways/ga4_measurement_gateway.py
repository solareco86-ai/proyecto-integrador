"""Gateway de Server-Side Tracking para Google Analytics 4 vía Measurement Protocol."""

from typing import Any

import httpx

from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)


class GA4MeasurementGateway(NotificationGateway):
    """Envía eventos de conversión directamente a GA4 mediante Measurement Protocol."""

    def __init__(self, measurement_id: str, api_secret: str, timeout: float = 5.0) -> None:
        self._measurement_id = measurement_id
        self._api_secret = api_secret
        self._timeout = timeout
        self._endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={self._measurement_id}&api_secret={self._api_secret}"

    async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        """Envía el evento generate_lead a GA4 del lado del servidor."""
        client_id = lead_data.get("client_id") or "555.datamaq_server"

        event_params: dict[str, Any] = {
            "lead_source": lead_data.get("lead_source") or "formulario_contacto",
            "traffic_source": lead_data.get("traffic_source") or "direct",
            "page_location": lead_data.get("page_location") or config.BASE_URL,
            "engagement_time_msec": 100,
        }
        if lead_data.get("utm_campaign"):
            event_params["campaign"] = lead_data.get("utm_campaign")
        if lead_data.get("gclid"):
            event_params["gclid"] = lead_data.get("gclid")

        payload: dict[str, Any] = {
            "client_id": client_id,
            "events": [
                {
                    "name": "generate_lead",
                    "params": event_params,
                }
            ],
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.post(self._endpoint, json=payload)
                if response.status_code < 300:
                    logger.info("[GA4MeasurementGateway] Evento generate_lead enviado exitosamente a GA4")
                    return {
                        "status": "sent",
                        "channel": "ga4_measurement_protocol",
                        "status_code": response.status_code,
                    }
                else:
                    logger.warning(
                        "[GA4MeasurementGateway] Respuesta no exitosa de GA4: status=%s, body=%s",
                        response.status_code,
                        response.text,
                    )
                    return {
                        "status": "failed",
                        "channel": "ga4_measurement_protocol",
                        "status_code": response.status_code,
                    }
            except Exception as e:
                logger.warning("[GA4MeasurementGateway] Error no bloqueante al enviar a GA4: %s", e)
                return {"status": "error", "channel": "ga4_measurement_protocol", "error": str(e)}

    async def notify_whatsapp_click(self, click_data: dict[str, Any]) -> dict[str, Any]:
        """Envía el evento whatsapp_click a GA4 del lado del servidor."""
        client_id = "555.datamaq_server"
        event_params: dict[str, Any] = {
            "event_category": "engagement",
            "event_label": click_data.get("element") or "whatsapp_cta",
            "page_location": click_data.get("page_location") or config.BASE_URL,
            "traffic_source": click_data.get("traffic_source") or "direct",
            "engagement_time_msec": 50,
        }
        if click_data.get("utm_campaign"):
            event_params["campaign"] = click_data.get("utm_campaign")
        if click_data.get("gclid"):
            event_params["gclid"] = click_data.get("gclid")

        payload: dict[str, Any] = {
            "client_id": client_id,
            "events": [
                {
                    "name": "whatsapp_click",
                    "params": event_params,
                }
            ],
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.post(self._endpoint, json=payload)
                return {
                    "status": "sent" if response.status_code < 300 else "failed",
                    "channel": "ga4_measurement_protocol",
                }
            except Exception as e:
                logger.warning("[GA4MeasurementGateway] Error no bloqueante en whatsapp_click: %s", e)
                return {"status": "error", "channel": "ga4_measurement_protocol", "error": str(e)}
