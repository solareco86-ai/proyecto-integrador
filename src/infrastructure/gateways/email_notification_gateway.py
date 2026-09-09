import asyncio
import smtplib
from email.message import EmailMessage
from typing import Any

from src.application.gateways.notification_gateway import NotificationGateway
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)


class EmailNotificationGateway(NotificationGateway):
    """Envía notificaciones de nuevos leads por email usando SMTP."""

    def __init__(self, host: str, port: int, username: str, password: str, to_email: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._to_email = to_email

    async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        logger.info("[EmailNotificationGateway] Enviando notificación de lead a %s", self._to_email)

        name = lead_data.get("name", "Sin nombre")
        msg = EmailMessage()
        msg["Subject"] = f"Nuevo lead de DataMaq: {name}"
        msg["From"] = self._username
        msg["To"] = self._to_email

        company = lead_data.get("company")
        role = lead_data.get("role")
        email = lead_data.get("email")
        phone = lead_data.get("phone")
        service = lead_data.get("service")
        traffic_source = lead_data.get("traffic_source") or lead_data.get("source")
        page_location = lead_data.get("page_location")
        comment = lead_data.get("comment", "")

        origin_host = config.BASE_URL.replace("https://", "").replace("http://", "").rstrip("/")
        lines = [f"Nuevo lead B2B recibido desde {origin_host}", ""]
        if name and str(name).strip() and str(name) not in {"No proporcionado", "Sin nombre"}:
            lines.append(f"Nombre: {str(name).strip()}")
        if company and str(company).strip() and str(company) not in {"No proporcionada", "No especificada"}:
            lines.append(f"Empresa: {str(company).strip()}")
        if role and str(role).strip() and str(role) not in {"No especificado"}:
            lines.append(f"Cargo/Rol: {str(role).strip()}")
        if email and str(email).strip() and str(email) not in {"No proporcionado"}:
            lines.append(f"Email: {str(email).strip()}")
        if phone and str(phone).strip() and str(phone) not in {"No proporcionado"}:
            lines.append(f"Teléfono: {str(phone).strip()}")
        if service and str(service).strip() and str(service) not in {"No especificado"}:
            lines.append(f"Servicio: {str(service).strip()}")
        if (
            traffic_source
            and str(traffic_source).strip()
            and str(traffic_source) not in {"No especificado", "No especificada"}
        ):
            lines.append(f"Origen: {str(traffic_source).strip()}")
        if page_location and str(page_location).strip() and str(page_location) not in {"No especificada"}:
            lines.append(f"Página: {str(page_location).strip()}")

        if comment and str(comment).strip():
            lines.append("")
            lines.append("Consulta:")
            lines.append(str(comment).strip())

        lines.append("")
        lines.append("---")
        lines.append("Este lead fue registrado en la base de datos de DataMaq.")

        body = "\n".join(lines)
        msg.set_content(body)

        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(
                None,
                self._send_email,
                msg,
            )
            logger.info("[EmailNotificationGateway] Notificación enviada a %s", self._to_email)
            return {"status": "sent", "to": self._to_email}
        except Exception as e:
            logger.error("[EmailNotificationGateway] Error al enviar email: %s", e)
            raise

    async def notify_whatsapp_click(self, click_data: dict[str, Any]) -> dict[str, Any]:
        """Los clics en WhatsApp no generan envío de correo electrónico."""
        return {"status": "skipped", "reason": "email_not_sent_for_clicks"}

    def _send_email(self, msg: EmailMessage) -> None:
        with smtplib.SMTP(self._host, self._port, timeout=15) as server:
            server.starttls()
            server.login(self._username, self._password)
            server.send_message(msg)


class ConsoleNotificationGateway(NotificationGateway):
    """Fallback para desarrollo local cuando SMTP no está configurado."""

    async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        logger.info("[ConsoleNotificationGateway] Lead recibido en modo local: %s", lead_data.get("name"))
        return {"status": "simulated", "to": "console"}

    async def notify_whatsapp_click(self, click_data: dict[str, Any]) -> dict[str, Any]:
        logger.info("[ConsoleNotificationGateway] Clic WhatsApp recibido en modo local: %s", click_data.get("element"))
        return {"status": "simulated", "to": "console"}
