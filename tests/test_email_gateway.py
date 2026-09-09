"""Tests del gateway de email SMTP (cubre el 29% faltante de email_notification_gateway.py)."""

from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.gateways.email_notification_gateway import EmailNotificationGateway


@pytest.mark.asyncio
async def test_notify_lead_sends_email():
    """Verifica que notify_lead llama a smtplib.SMTP con los parametros correctos."""
    gateway = EmailNotificationGateway(
        host="smtp.test.com",
        port=587,
        username="user@test.com",
        password="secret",
        to_email="notify@test.com",
    )

    lead_data = {
        "name": "Juan Perez",
        "email": "juan@example.com",
        "phone": "15-1234-5678",
        "company": "TestCorp",
        "comment": "Consulta de prueba",
        "source": "direct",
        "preferred_contact_channel": "whatsapp",
    }

    mock_server = MagicMock()
    mock_smtp = MagicMock()
    mock_smtp.__enter__ = MagicMock(return_value=mock_server)
    mock_smtp.__exit__ = MagicMock(return_value=None)

    with patch("smtplib.SMTP", return_value=mock_smtp):
        result = await gateway.notify_lead(lead_data)

    # Verifica que se envio el email via send_message
    mock_server.send_message.assert_called_once()
    msg = mock_server.send_message.call_args[0][0]
    assert msg["Subject"].startswith("Nuevo lead de DataMaq")
    assert msg["To"] == "notify@test.com"

    # Verifica el cuerpo del email
    body = msg.get_content()
    assert "Juan Perez" in body
    assert "juan@example.com" in body
    assert "TestCorp" in body

    # Verifica resultado
    assert result["status"] == "sent"
    assert result["to"] == "notify@test.com"


@pytest.mark.asyncio
async def test_notify_lead_handles_smtp_error():
    """Verifica que un error SMTP propaga la excepcion."""
    gateway = EmailNotificationGateway(
        host="smtp.test.com",
        port=587,
        username="user@test.com",
        password="secret",
        to_email="notify@test.com",
    )

    lead_data = {"name": "Test", "email": "t@t.com", "phone": "", "company": "", "comment": "", "source": ""}

    mock_failing_smtp = MagicMock()
    mock_failing_smtp.__enter__ = MagicMock(side_effect=Exception("Connection refused"))
    mock_failing_smtp.__exit__ = MagicMock(return_value=None)

    with patch("smtplib.SMTP", return_value=mock_failing_smtp):
        with pytest.raises(Exception, match="Connection refused"):
            await gateway.notify_lead(lead_data)


@pytest.mark.asyncio
async def test_notify_lead_empty_optional_fields():
    """Verifica que el email se envia omitiendo campos opcionales ausentes (formato limpio)."""
    gateway = EmailNotificationGateway(
        host="smtp.test.com",
        port=587,
        username="user@test.com",
        password="secret",
        to_email="notify@test.com",
    )

    lead_data = {
        "name": "Minimal",
        "comment": "",
        "source": "desconocido",
    }

    mock_server = MagicMock()
    mock_smtp = MagicMock()
    mock_smtp.__enter__ = MagicMock(return_value=mock_server)
    mock_smtp.__exit__ = MagicMock(return_value=None)

    with patch("smtplib.SMTP", return_value=mock_smtp):
        result = await gateway.notify_lead(lead_data)

    assert result["status"] == "sent"
    msg = mock_server.send_message.call_args[0][0]
    body = msg.get_content()
    assert "Nombre: Minimal" in body
    assert "Origen: desconocido" in body
    # Formato limpio: no debe incluir textos como "No proporcionado" o "No especificado"
    assert "No proporcionado" not in body
    assert "No especificado" not in body


@pytest.mark.asyncio
async def test_notify_lead_default_source():
    """Verifica que si no se envia source ni campos opcionales, se omiten limpiamente."""
    gateway = EmailNotificationGateway(
        host="smtp.test.com",
        port=587,
        username="user@test.com",
        password="secret",
        to_email="notify@test.com",
    )

    lead_data = {
        "name": "Test",
        "email": "t@t.com",
        "phone": "",
        "company": "",
        "comment": "",
    }

    mock_server = MagicMock()
    mock_smtp = MagicMock()
    mock_smtp.__enter__ = MagicMock(return_value=mock_server)
    mock_smtp.__exit__ = MagicMock(return_value=None)

    with patch("smtplib.SMTP", return_value=mock_smtp):
        result = await gateway.notify_lead(lead_data)

    assert result["status"] == "sent"
    msg = mock_server.send_message.call_args[0][0]
    body = msg.get_content()
    assert "Nombre: Test" in body
    assert "Email: t@t.com" in body
    assert "Empresa:" not in body
    assert "Teléfono:" not in body


@pytest.mark.asyncio
async def test_notify_whatsapp_click_skips_email():
    """Verifica que notify_whatsapp_click no envia emails SMTP y retorna status skipped."""
    gateway = EmailNotificationGateway(
        host="smtp.test.com",
        port=587,
        username="user@test.com",
        password="secret",
        to_email="notify@test.com",
    )

    result = await gateway.notify_whatsapp_click({"element": "FAB"})
    assert result["status"] == "skipped"
    assert result["reason"] == "email_not_sent_for_clicks"
