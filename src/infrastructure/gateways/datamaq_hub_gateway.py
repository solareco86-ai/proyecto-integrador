"""Gateway para integración webhook con Datamaq Hub (/api/v1/leads/ingest)."""

from typing import Any

import httpx

from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)


class DatamaqHubGateway(NotificationGateway):
    """Envía leads entrantes al endpoint de ingest de Datamaq Hub de forma asíncrona y fail-safe."""

    def __init__(self, hub_url: str, api_key: str | None = None, timeout: float = 5.0) -> None:
        self._hub_url = hub_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout
        self._endpoint = f"{self._hub_url}/api/v1/leads/ingest"

    async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        """Inyecta el lead estructurado en Datamaq Hub."""
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "User-Agent": "www-datamaq/1.0",
        }
        if self._api_key:
            headers["X-Api-Key"] = self._api_key

        payload: dict[str, Any] = {
            "name": lead_data.get("name"),
            "email": lead_data.get("email"),
            "phone": lead_data.get("phone"),
            "company": lead_data.get("company"),
            "role": lead_data.get("role"),
            "service": lead_data.get("service"),
            "comment": lead_data.get("comment"),
            "page_location": lead_data.get("page_location"),
            "traffic_source": lead_data.get("traffic_source"),
            "lead_source": lead_data.get("lead_source") or "web_form",
            "metadata": {
                "utm_source": lead_data.get("utm_source"),
                "utm_medium": lead_data.get("utm_medium"),
                "utm_campaign": lead_data.get("utm_campaign"),
                "gclid": lead_data.get("gclid"),
            },
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.post(self._endpoint, json=payload, headers=headers)
                if response.status_code < 300:
                    logger.info("[DatamaqHubGateway] Lead inyectado exitosamente en Datamaq Hub")
                    return {"status": "sent", "channel": "datamaq_hub", "status_code": response.status_code}
                else:
                    logger.warning(
                        "[DatamaqHubGateway] Datamaq Hub respondió con status=%s: %s",
                        response.status_code,
                        response.text,
                    )
                    return {"status": "failed", "channel": "datamaq_hub", "status_code": response.status_code}
            except Exception as e:
                logger.warning("[DatamaqHubGateway] Error no bloqueante al comunicar con Datamaq Hub: %s", e)
                return {"status": "error", "channel": "datamaq_hub", "error": str(e)}
