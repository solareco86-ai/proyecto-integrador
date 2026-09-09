from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.infrastructure.gateways.telegram_notification_gateway import (
    CompositeNotificationGateway,
    TelegramNotificationGateway,
    format_cookie_status,
    parse_device_info,
)


@pytest.mark.asyncio
async def test_telegram_notification_gateway_lead_success() -> None:
    gateway = TelegramNotificationGateway(bot_token="test_token", chat_id="123456")
    lead_data = {
        "name": "Juan Perez",
        "email": "juan@empresa.com",
        "phone": "+5411223344",
        "company": "Empresa S.A.",
        "role": "Jefe de Planta",
        "service": "Mantenimiento MT",
        "comment": "Consulta sobre MT",
        "page_location": "https://datamaq.com.ar/industria/energia.html",
        "traffic_source": "Google Ads (SEM)",
    }

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "sent"
        assert result["channel"] == "telegram"
        assert result["chat_id"] == "123456"
        mock_post.assert_called_once()

        payload = mock_post.call_args[1]["json"]
        text = payload["text"]
        assert "NUEVO LEAD" in text
        assert "Juan Perez" in text
        assert "Empresa S.A." in text
        assert "Jefe de Planta" in text
        assert "juan@empresa.com" in text
        assert "+5411223344" in text
        assert "Mantenimiento MT" in text
        assert "Google Ads (SEM)" in text
        assert "https://datamaq.com.ar/industria/energia.html" in text
        assert "https://wa.me/5411223344" in text


@pytest.mark.asyncio
async def test_telegram_notification_gateway_lead_clean_minimal() -> None:
    gateway = TelegramNotificationGateway(bot_token="test_token", chat_id="123456")
    lead_data = {
        "name": "Cliente Anónimo",
        "comment": "Solo consulta breve",
    }

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "sent"

        payload = mock_post.call_args[1]["json"]
        text = payload["text"]
        assert "Cliente Anónimo" in text
        assert "Solo consulta breve" in text
        # Verifica que los campos vacíos NO aparecen como "No especificado"
        assert "No especificado" not in text
        assert "No proporcionada" not in text


@pytest.mark.asyncio
async def test_telegram_notification_gateway_whatsapp_click_accepted() -> None:
    gateway = TelegramNotificationGateway(bot_token="test_token", chat_id="123456")
    click_data = {
        "page_location": "https://datamaq.com.ar/industria/energia.html",
        "traffic_source": "🎯 Google Ads (SEM)",
        "element": "Botón Flotante (FAB)",
        "cookie_consent": "accepted",
        "user_agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
        "utm_campaign": "calidad-energia",
    }

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_whatsapp_click(click_data)
        assert result["status"] == "sent"
        assert result["channel"] == "telegram"

        payload = mock_post.call_args[1]["json"]
        text = payload["text"]
        assert "CLIC EN WHATSAPP (CTA)" in text
        assert "https://datamaq.com.ar/industria/energia.html" in text
        assert "🎯 Google Ads (SEM) — Campaña: calidad-energia" in text
        assert "Botón Flotante (FAB)" in text
        assert "✅ Aceptadas (Sesión en Clarity & GA4)" in text
        assert "Android Mobile (Chrome)" in text


@pytest.mark.asyncio
async def test_telegram_notification_gateway_whatsapp_click_rejected_and_pending() -> None:
    gateway = TelegramNotificationGateway(bot_token="test_token", chat_id="123456")

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        # Rechazado
        await gateway.notify_whatsapp_click({"cookie_consent": "rejected"})
        payload_rejected = mock_post.call_args[1]["json"]["text"]
        assert "❌ Rechazadas (Solo telemetría directa)" in payload_rejected

        # Pendiente / None
        await gateway.notify_whatsapp_click({"cookie_consent": None})
        payload_pending = mock_post.call_args[1]["json"]["text"]
        assert "⏳ No respondido / Pendiente (Solo telemetría directa)" in payload_pending


def test_device_and_cookie_helpers() -> None:
    assert parse_device_info(None) == "Dispositivo no identificado"
    assert "iPhone" in parse_device_info("Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)")
    assert "Windows" in parse_device_info("Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0")
    assert format_cookie_status("accepted").startswith("✅")
    assert format_cookie_status("rejected").startswith("❌")
    assert format_cookie_status(None).startswith("⏳")


@pytest.mark.asyncio
async def test_composite_notification_gateway() -> None:
    mock_gw1 = AsyncMock()
    mock_gw1.notify_lead.return_value = {"status": "sent", "channel": "email"}
    mock_gw1.notify_whatsapp_click.return_value = {"status": "skipped", "channel": "email"}
    mock_gw2 = AsyncMock()
    mock_gw2.notify_lead.return_value = {"status": "sent", "channel": "telegram"}
    mock_gw2.notify_whatsapp_click.return_value = {"status": "sent", "channel": "telegram"}

    composite = CompositeNotificationGateway([mock_gw1, mock_gw2])

    result_lead = await composite.notify_lead({"name": "Test"})
    assert result_lead["status"] == "completed"
    assert len(result_lead["results"]) == 2

    result_click = await composite.notify_whatsapp_click({"element": "Hero"})
    assert result_click["status"] == "completed"
    assert len(result_click["results"]) == 2

    mock_gw1.notify_direct_contact.return_value = {"status": "skipped", "channel": "email"}
    mock_gw2.notify_direct_contact.return_value = {"status": "sent", "channel": "telegram"}
    result_direct = await composite.notify_direct_contact({"action": "email_click"})
    assert result_direct["status"] == "completed"
    assert len(result_direct["results"]) == 2


@pytest.mark.asyncio
async def test_telegram_notification_gateway_direct_contact_email_and_copy() -> None:
    gateway = TelegramNotificationGateway(bot_token="test_token", chat_id="123456")
    contact_data = {
        "action": "email_copy",
        "target_value": "info@datamaq.com.ar",
        "page_location": "https://datamaq.com.ar/industria/energia.html",
        "traffic_source": "📱 Redes Sociales (LinkedIn)",
        "element": "Selección y Copia de Texto",
        "cookie_consent": "accepted",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0",
        "utm_campaign": "retrofit-iot",
    }

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_direct_contact(contact_data)
        assert result["status"] == "sent"
        assert result["channel"] == "telegram"

        payload = mock_post.call_args[1]["json"]
        text = payload["text"]
        assert "INTENCIÓN DE CONTACTO DIRECTO" in text
        assert "Copia de Email al Portapapeles (info@datamaq.com.ar)" in text
        assert "https://datamaq.com.ar/industria/energia.html" in text
        assert "📱 Redes Sociales (LinkedIn) — Campaña: retrofit-iot" in text
        assert "Selección y Copia de Texto" in text
        assert "✅ Aceptadas (Sesión en Clarity & GA4)" in text
        assert "Desktop (Chrome / Windows)" in text
