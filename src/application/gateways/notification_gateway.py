from abc import ABC, abstractmethod
from typing import Any


class NotificationGateway(ABC):
    """Puerto de salida para notificaciones de leads y eventos comerciales."""

    @abstractmethod
    async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        """Notifica un nuevo lead completo de formulario al equipo comercial."""
        raise NotImplementedError

    async def notify_whatsapp_click(self, click_data: dict[str, Any]) -> dict[str, Any]:
        """Notifica un evento de clic en botón o CTA de WhatsApp."""
        return {"status": "skipped", "reason": "unsupported_channel"}

    async def notify_direct_contact(self, contact_data: dict[str, Any]) -> dict[str, Any]:
        """Notifica un evento de clic o copia de email/teléfono de contacto directo."""
        return {"status": "skipped", "reason": "unsupported_channel"}
