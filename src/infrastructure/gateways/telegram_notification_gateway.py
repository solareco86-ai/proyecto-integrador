import html
from typing import Any

import httpx

from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)


def parse_device_info(user_agent: str | None) -> str:
    """Extrae un resumen legible del dispositivo y navegador a partir del User-Agent."""
    if not user_agent or user_agent in {"No especificado", "unknown", "None"}:
        return "Dispositivo no identificado"
    ua = user_agent.lower()
    if "iphone" in ua:
        device = "iPhone"
    elif "ipad" in ua:
        device = "iPad"
    elif "android" in ua:
        device = "Android Mobile" if "mobi" in ua else "Android Tablet"
    elif "mobi" in ua:
        device = "Mobile"
    else:
        device = "Desktop"

    browser = "Navegador Web"
    if "edg" in ua:
        browser = "Edge"
    elif "chrome" in ua or "crios" in ua:
        browser = "Chrome"
    elif "safari" in ua:
        browser = "Safari"
    elif "firefox" in ua or "fxios" in ua:
        browser = "Firefox"

    os_name = ""
    if "windows" in ua:
        os_name = "Windows"
    elif "macintosh" in ua or "mac os" in ua:
        os_name = "macOS"
    elif "linux" in ua and "android" not in ua:
        os_name = "Linux"

    if os_name:
        return f"{device} ({browser} / {os_name})"
    return f"{device} ({browser})"


def format_cookie_status(consent: str | None) -> str:
    """Formatea el estado de consentimiento de cookies para el reporte en Telegram."""
    if consent == "accepted":
        return "✅ Aceptadas (Sesión en Clarity & GA4)"
    elif consent == "rejected":
        return "❌ Rechazadas (Solo telemetría directa)"
    return "⏳ No respondido / Pendiente (Solo telemetría directa)"


class TelegramNotificationGateway(NotificationGateway):
    """Envía notificaciones de nuevos leads y clics de WhatsApp mediante el Bot API de Telegram."""

    def __init__(self, bot_token: str, chat_id: str):
        self._bot_token = bot_token
        self._chat_id = chat_id
        self._api_url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"

    async def _send_telegram_message(self, message: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "chat_id": self._chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(self._api_url, json=payload)
                response.raise_for_status()
                logger.info("[TelegramNotificationGateway] Notificación enviada exitosamente a Telegram")
                return {"status": "sent", "channel": "telegram", "chat_id": self._chat_id}
            except Exception as e:
                logger.error("[TelegramNotificationGateway] Error al enviar mensaje a Telegram: %s", e)
                raise

    async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        """Formatea y envía una notificación limpia de nuevo lead (formulario de contacto)."""
        logger.info(
            "[TelegramNotificationGateway] Enviando notificación de lead a chat Telegram %s",
            self._chat_id,
        )

        name = lead_data.get("name")
        email = lead_data.get("email")
        phone = lead_data.get("phone")
        company = lead_data.get("company")
        role = lead_data.get("role")
        service = lead_data.get("service")
        comment = lead_data.get("comment", "")
        page_location = lead_data.get("page_location")
        traffic_source = lead_data.get("traffic_source")

        phone_clean = "".join(c for c in str(phone) if c.isdigit()) if phone else ""
        wa_link = f"https://wa.me/{phone_clean}" if phone_clean else None

        message_lines = ["🔔 <b>NUEVO LEAD</b> (Formulario Web)\n"]
        if name and str(name).strip() and str(name) not in {"No proporcionado", "Sin nombre"}:
            message_lines.append(f"👤 <b>Nombre:</b> {html.escape(str(name).strip())}")
        if company and str(company).strip() and str(company) not in {"No proporcionada", "No especificada"}:
            message_lines.append(f"🏢 <b>Empresa:</b> {html.escape(str(company).strip())}")
        if role and str(role).strip() and str(role) not in {"No especificado"}:
            message_lines.append(f"💼 <b>Cargo:</b> {html.escape(str(role).strip())}")
        if email and str(email).strip() and str(email) not in {"No proporcionado"}:
            message_lines.append(f"📧 <b>Email:</b> {html.escape(str(email).strip())}")
        if phone and str(phone).strip() and str(phone) not in {"No proporcionado"}:
            message_lines.append(f"📞 <b>Teléfono:</b> {html.escape(str(phone).strip())}")
        if service and str(service).strip() and str(service) not in {"No especificado"}:
            message_lines.append(f"🛠️ <b>Servicio:</b> {html.escape(str(service).strip())}")
        if traffic_source and str(traffic_source).strip() and str(traffic_source) not in {"No especificado"}:
            message_lines.append(f"📍 <b>Origen:</b> {html.escape(str(traffic_source).strip())}")
        if page_location and str(page_location).strip() and str(page_location) not in {"No especificada"}:
            message_lines.append(f"🌐 <b>Página:</b> {html.escape(str(page_location).strip())}")
        if comment and str(comment).strip():
            message_lines.append(f"\n💬 <b>Consulta:</b>\n<i>{html.escape(str(comment).strip())}</i>\n")
        if wa_link:
            message_lines.append(f'📲 <b>Contacto rápido:</b> <a href="{wa_link}">Abrir Chat WhatsApp</a>')

        message = "\n".join(message_lines)
        return await self._send_telegram_message(message)

    async def notify_whatsapp_click(self, click_data: dict[str, Any]) -> dict[str, Any]:
        """Formatea y envía una notificación concisa y sin ruido para clics en WhatsApp/CTA."""
        logger.info(
            "[TelegramNotificationGateway] Enviando notificación de clic en WhatsApp a Telegram %s",
            self._chat_id,
        )
        page_location = click_data.get("page_location") or "No especificada"
        traffic_source = click_data.get("traffic_source") or "Directo / Desconocido"
        element = click_data.get("element") or "Botón Flotante (FAB)"
        cookie_consent = click_data.get("cookie_consent")
        user_agent = click_data.get("user_agent")
        utm_campaign = click_data.get("utm_campaign")

        cookie_status_text = format_cookie_status(cookie_consent)
        device_text = parse_device_info(user_agent)

        origen_text = traffic_source
        if utm_campaign and str(utm_campaign) not in str(origen_text):
            origen_text += f" — Campaña: {utm_campaign}"

        message_lines = [
            "⚡ <b>CLIC EN WHATSAPP (CTA)</b>\n",
            f"🌐 <b>Página:</b> {html.escape(str(page_location))}",
            f"📍 <b>Origen:</b> {html.escape(str(origen_text))}",
            f"🔘 <b>Elemento:</b> {html.escape(str(element))}",
            f"🍪 <b>Cookies:</b> {cookie_status_text}",
            f"📱 <b>Dispositivo:</b> {html.escape(device_text)}",
        ]
        message = "\n".join(message_lines)
        return await self._send_telegram_message(message)

    async def notify_direct_contact(self, contact_data: dict[str, Any]) -> dict[str, Any]:
        """Formatea y envía una alerta instantánea cuando un usuario clickea o copia email/teléfono."""
        logger.info(
            "[TelegramNotificationGateway] Enviando notificación de contacto directo a Telegram %s",
            self._chat_id,
        )
        action = contact_data.get("action") or "direct_contact"
        target_value = contact_data.get("target_value") or config.NOTIFICATION_EMAIL
        page_location = contact_data.get("page_location") or "No especificada"
        traffic_source = contact_data.get("traffic_source") or "Directo / Desconocido"
        element = contact_data.get("element") or "Enlace Directo"
        cookie_consent = contact_data.get("cookie_consent")
        user_agent = contact_data.get("user_agent")
        utm_campaign = contact_data.get("utm_campaign")

        cookie_status_text = format_cookie_status(cookie_consent)
        device_text = parse_device_info(user_agent)

        action_labels: dict[str, str] = {
            "email_click": f"Clic en Email ({target_value})",
            "email_copy": f"Copia de Email al Portapapeles ({target_value})",
            "phone_click": f"Clic en Teléfono ({target_value})",
            "phone_copy": f"Copia de Teléfono al Portapapeles ({target_value})",
        }
        action_text = action_labels.get(action, f"Contacto Directo: {action}")

        origen_text = traffic_source
        if utm_campaign and str(utm_campaign) not in str(origen_text):
            origen_text += f" — Campaña: {utm_campaign}"

        message_lines = [
            "📧 <b>INTENCIÓN DE CONTACTO DIRECTO</b>\n",
            f"🔘 <b>Acción:</b> {html.escape(str(action_text))}",
            f"🌐 <b>Página:</b> {html.escape(str(page_location))}",
            f"📍 <b>Origen:</b> {html.escape(str(origen_text))}",
            f"🏷️ <b>Elemento:</b> {html.escape(str(element))}",
            f"🍪 <b>Cookies:</b> {cookie_status_text}",
            f"📱 <b>Dispositivo:</b> {html.escape(device_text)}",
            "\n💡 <i>Un prospecto corporativo interactuó con los datos de contacto directo.</i>",
        ]
        message = "\n".join(message_lines)
        return await self._send_telegram_message(message)


class CompositeNotificationGateway(NotificationGateway):
    """Agrupa múltiples NotificationGateway para notificar por varios canales (Email, Telegram, etc.)."""

    def __init__(self, gateways: list[NotificationGateway]):
        self._gateways = gateways

    async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        for gateway in self._gateways:
            try:
                res = await gateway.notify_lead(lead_data)
                results.append(res)
            except Exception as e:
                logger.error(
                    "[CompositeNotificationGateway] Error en gateway %s: %s",
                    type(gateway).__name__,
                    e,
                )
        return {"status": "completed", "results": results}

    async def notify_whatsapp_click(self, click_data: dict[str, Any]) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        for gateway in self._gateways:
            try:
                res = await gateway.notify_whatsapp_click(click_data)
                results.append(res)
            except Exception as e:
                logger.error(
                    "[CompositeNotificationGateway] Error en gateway %s: %s",
                    type(gateway).__name__,
                    e,
                )
        return {"status": "completed", "results": results}

    async def notify_direct_contact(self, contact_data: dict[str, Any]) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        for gateway in self._gateways:
            try:
                res = await gateway.notify_direct_contact(contact_data)
                results.append(res)
            except Exception as e:
                logger.error(
                    "[CompositeNotificationGateway] Error en gateway %s: %s",
                    type(gateway).__name__,
                    e,
                )
        return {"status": "completed", "results": results}
