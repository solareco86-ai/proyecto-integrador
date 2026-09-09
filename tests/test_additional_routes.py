from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient  # type: ignore

from src.application.dtos import ContenidoModel
from src.application.gateways.notification_gateway import NotificationGateway
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido, get_lead_repository, get_notification_gateway


# Mock data actualizado a la nueva estructura
# Mock data actualizado a la nueva estructura
async def override_get_contenido():
    return ContenidoModel.model_validate(
        {
            "brand": {
                "brandName": "Test",
                "brandAriaLabel": "Test",
                "baseOperativa": "Test",
                "contactEmail": "test@test.com",
                "whatsappUrl": "http://test.com",
                "technician": {"name": "Test", "role": "Test", "photo": {"src": "test.jpg", "alt": "Test"}},
                "footerDescription": "Test footer description",
            },
            "content": {
                "hero": {
                    "badge": "Test",
                    "title": "Test",
                    "subtitle": "Test",
                    "responseNote": "Test",
                    "primaryCta": {"label": "Test", "href": "http://test.com"},
                    "secondaryCta": {"label": "Test", "href": "http://test.com"},
                    "benefits": [],
                    "image": {"src": "test.jpg", "alt": "Test"},
                },
                "services": {"title": "Test", "cards": []},
                "navbar": {"links": []},
                "faq": {"questions": []},
                "about": {"title": "Test", "paragraphs": [], "image": {"src": "test.jpg", "alt": "Test"}},
                "profile": {"bullets": []},
                "legal": {"text": "Test"},
                "cookie_banner": {
                    "title": "Test",
                    "text": "Test",
                    "accept_label": "Aceptar",
                    "reject_label": "Rechazar",
                    "more_info_label": "Ver más",
                    "more_info_link": "/terminos-y-condiciones",
                },
                "contact": {
                    "title": "Solicitá asistencia técnica híbrida",
                    "subtitle": "Test",
                    "cta": "Test",
                    "alt_email": {"label": "Test", "title": "Test", "email": "test@test.com"},
                    "progress_text": "Test",
                    "privacy_note": "Test",
                    "error_message": "Test",
                    "optional_text": "Test",
                    "steps": [],
                },
                "assistance_modes": {
                    "on_site": {"label": "Campo", "description": "Test", "icon": "geo-alt-fill"},
                    "remote": {"label": "Remoto", "description": "Test", "icon": "wifi"},
                },
                "proof_strip": {"items": [{"label": "Test", "text": "Test proof text"}]},
                "process": {
                    "eyebrow": "Test",
                    "title": "Test process",
                    "steps": [{"title": "Step 1", "text": "Test step"}],
                },
                "courses": {
                    "badge": "Capacitaciones de cortesía",
                    "title": "Cursos y capacitaciones técnicas gratuitas",
                    "subtitle": "Test",
                    "assistance_cta_label": "Necesitás asistencia técnica",
                    "assistance_cta_href": "/contact",
                },
                "cases": {"badge": "Casos de aplicación", "title": "Casos técnicos", "subtitle": "Test"},
            },
            "seo": {
                "title": "Test",
                "description": "Test",
                "site_name": "Test",
                "canonical_url": "http://test.com",
                "og_image": "http://test.com/og.png",
            },
            "legal_pages": {
                "terms": {
                    "title": "Términos y condiciones",
                    "last_updated": "2026-06-19",
                    "introduction": "Test",
                    "sections": [{"title": "Test", "paragraphs": ["Test"]}],
                }
            },
            "footer": {
                "navigation_groups": [
                    {
                        "title": "Navegación",
                        "links": [
                            {"label": "Inicio", "href": "/"},
                            {"label": "Cursos", "href": "/cursos"},
                            {"label": "Contacto", "href": "/contact"},
                        ],
                    }
                ],
                "cta_title": "Test CTA Title",
                "cta_label": "Test CTA Label",
                "whatsapp_text": "Test WhatsApp text",
                "terms_label": "Test Terms Label",
                "terms_href": "/terminos-y-condiciones",
                "copyright_suffix": "Test copyright suffix",
            },
        }
    )


@pytest.fixture(autouse=True)
def setup_dependency_overrides():
    app.dependency_overrides[get_contenido] = override_get_contenido
    app.dependency_overrides[get_notification_gateway] = override_get_notification_gateway
    app.dependency_overrides[get_lead_repository] = override_get_lead_repository
    yield
    app.dependency_overrides.clear()


async def override_get_notification_gateway():
    mock = AsyncMock(spec=NotificationGateway)
    mock.notify_lead.return_value = {"status": "sent", "message": "Mocked"}
    return mock


async def override_get_lead_repository():
    mock = AsyncMock(spec=LeadRepository)
    mock.save.return_value = None
    return mock


@pytest.mark.asyncio  # type: ignore
async def test_sitemap_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]


@pytest.mark.asyncio  # type: ignore
async def test_terms_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/terminos-y-condiciones")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Términos y condiciones" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_contact_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Solicitá asistencia técnica híbrida" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_custom_404_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response_unknown = await ac.get("/pagina-que-no-existe")
        response_business = await ac.get("/cursos/curso-que-no-existe")

    assert response_unknown.status_code == 404
    assert "text/html" in response_unknown.headers["content-type"]
    assert "Página no encontrada" in response_unknown.text

    assert response_business.status_code == 404
    assert "text/html" in response_business.headers["content-type"]
    assert "Página no encontrada" in response_business.text


@pytest.mark.asyncio  # type: ignore
async def test_sitemap_includes_contact():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "https://datamaq.com.ar/contact" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_localidad_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/buenos-aires/escobar/garin.html")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Garín" in response.text
    assert "Telemetría y calidad de energía" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_industria_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/industria/grafica.html")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Industria Gráfica" in response.text
    assert "Telemetría y calidad de energía" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_localidad_tigre_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/buenos-aires/tigre/general-pacheco.html")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "General Pacheco" in response.text
    assert "Telemetría y calidad de energía" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_industria_plastica_page_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/industria/plastica.html")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Industria Plástica" in response.text
    assert "Telemetría y calidad de energía" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_casos_list_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/casos")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Casos técnicos" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_caso_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/casos/madygraf-eficiencia-y-vision-40")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "MadyGraf" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_submit_contact_returns_success():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Test User",
        "comment": "Test comment",
        "email": "test@example.com",
        "pageLocation": "http://test/contact",
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["submitStatus"] == "success"
    assert "requestId" in data
    assert "submissionId" in data
    assert data["submissionId"].startswith("lead_")


@pytest.mark.asyncio  # type: ignore
async def test_submit_contact_returns_partial_success_when_notification_fails():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Test User",
        "comment": "Test comment",
        "email": "test@example.com",
        "createdAt": "2026-06-20T00:00:00Z",
        "pageLocation": "http://test/contact",
    }

    # Override the notification gateway to raise an exception
    async def failing_notification_gateway():
        mock = AsyncMock(spec=NotificationGateway)
        mock.notify_lead.side_effect = Exception("Notification down")
        return mock

    app.dependency_overrides[get_notification_gateway] = failing_notification_gateway
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/contact", json=payload)
    finally:
        # Restore the default override
        app.dependency_overrides[get_notification_gateway] = override_get_notification_gateway

    assert response.status_code == 201
    data = response.json()
    assert data["submitStatus"] == "partial_success"
    assert "requestId" in data
    assert "submissionId" in data
    assert data["submissionId"].startswith("lead_")


@pytest.mark.asyncio  # type: ignore
async def test_track_whatsapp_click_success():
    transport = ASGITransport(app=app)
    payload = {
        "pageLocation": "http://test/cobertura/escobar",
        "trafficSource": "WhatsApp FAB Escobar",
        "element": "Botón Flotante (FAB)",
        "cookieConsent": "accepted",
        "utmSource": "google",
        "utmMedium": "cpc",
        "utmCampaign": "calidad-energia",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/events/whatsapp-click", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["tracked"] is True
    assert "leadId" in data
    assert data["leadId"].startswith("lead_")


@pytest.mark.asyncio  # type: ignore
async def test_track_direct_contact_success():
    transport = ASGITransport(app=app)
    payload = {
        "action": "email_click",
        "targetValue": "info@datamaq.com.ar",
        "pageLocation": "http://test/industria/energia.html",
        "trafficSource": "📱 Redes Sociales (LinkedIn)",
        "element": "Footer",
        "cookieConsent": "accepted",
        "utmSource": "linkedin",
        "utmMedium": "social",
        "utmCampaign": "retrofit-iot",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/events/direct-contact", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["tracked"] is True
    assert "leadId" in data
    assert data["leadId"].startswith("lead_")


@pytest.mark.asyncio  # type: ignore
async def test_monitoreo_redirects_301():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/monitoreo")

    assert response.status_code == 301
    assert response.headers["location"] == "/cursos"


@pytest.mark.asyncio  # type: ignore
async def test_sitemap_excludes_hidden_monitoreo():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "https://datamaq.com.ar/monitoreo" not in response.text
