from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.gateways.notification_gateway import NotificationGateway
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_lead_repository, get_notification_gateway
from src.infrastructure.fastapi.middleware import _rate_store


@pytest.fixture(autouse=True)
def setup_test_dependencies():
    _rate_store.clear()
    mock_repo = AsyncMock(spec=LeadRepository)
    mock_repo.save.return_value = None
    mock_gateway = AsyncMock(spec=NotificationGateway)
    mock_gateway.notify_lead.return_value = {"status": "sent", "channel": "telegram"}

    app.dependency_overrides[get_lead_repository] = lambda: mock_repo
    app.dependency_overrides[get_notification_gateway] = lambda: mock_gateway
    try:
        yield
    finally:
        _rate_store.clear()
        app.dependency_overrides.pop(get_lead_repository, None)
        app.dependency_overrides.pop(get_notification_gateway, None)


@pytest.mark.asyncio  # type: ignore
async def test_submit_contact_with_honeypot_discards_silently() -> None:
    """Verifica que si un bot completa el campo honeypot website_url_hp, se descarte silenciosamente sin guardar."""
    transport = ASGITransport(app=app)
    payload = {
        "name": "Spam Bot",
        "email": "spambot@example.com",
        "phone": "+1234567890",
        "comment": "Compre viagra barato en http://spam.com",
        "website_url_hp": "http://spam.com/bot-filled-this",
        "leadSource": "formulario_contacto",
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["submissionId"] == "lead_hp_ignored"
    assert data["submitStatus"] == "success"


@pytest.mark.asyncio  # type: ignore
async def test_submit_contact_normal_proceeds() -> None:
    """Verifica que un envío legítimo sin honeypot procede normalmente."""
    transport = ASGITransport(app=app)
    payload = {
        "name": "Ingeniero Planta",
        "email": "ingeniero@empresa.com.ar",
        "phone": "+54 11 4444 5555",
        "comment": "Consulta por analizador SmartPlus en Pilar.",
        "website_url_hp": None,
        "leadSource": "formulario_contacto",
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["submissionId"].startswith("lead_")
    assert data["submissionId"] != "lead_hp_ignored"
    assert data["submitStatus"] == "success"


@pytest.mark.asyncio  # type: ignore
async def test_contact_page_renders_honeypot_and_email_protect() -> None:
    """Verifica que la plantilla de contacto renderiza el campo señuelo honeypot y la clase js-email-protect."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")

    assert response.status_code == 200
    html = response.text
    assert "website_url_hp" in html
    assert "js-email-protect" in html
    assert 'data-u="ifst199alumnos"' in html
    assert 'data-d="gmail.com"' in html
