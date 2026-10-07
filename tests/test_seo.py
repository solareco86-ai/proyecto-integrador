import pytest
from httpx import ASGITransport, AsyncClient  # type: ignore

from src.application.dtos import ContenidoModel
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido


async def override_get_contenido():
    return ContenidoModel(
        brand={
            "brandName": "Test",
            "brandAriaLabel": "Test",
            "baseOperativa": "Test",
            "contactEmail": "test@test.com",
            "whatsappUrl": "http://test.com",
            "technician": {"name": "Test", "role": "Test", "photo": {"src": "test.jpg", "alt": "Test"}},
            "footerDescription": "Test footer description",
            "address": {
                "streetAddress": "Test 123",
                "postalCode": "1234",
                "addressLocality": "Garín",
                "addressRegion": "Buenos Aires",
                "addressCountry": "AR",
            },
            "geo": {"lat": -34.423, "lng": -58.745},
            "openingHours": "Mo-Fr 08:00-18:00",
            "sameAs": ["https://www.linkedin.com/in/test"],
        },
        content={
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
            "services": {
                "title": "Test",
                "cards": [
                    {
                        "id": "test-service",
                        "title": "Monitoreo de energía",
                        "description": "Test description",
                        "problem": "Test problem",
                        "key_points": ["Punto 1"],
                    }
                ],
            },
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
                "title": "Test",
                "subtitle": "Test",
                "cta": "Test",
                "alt_email": {"label": "Test", "title": "Test", "email": "test@test.com"},
                "progress_text": "Test",
                "privacy_note": "Test",
                "error_message": "Test",
                "optional_text": "Test",
                "required_text": "Test",
                "contact_channel_note": "Test",
                "validation_messages": {},
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
        seo={
            "title": "Test",
            "description": "Test",
            "site_name": "Test",
            "canonical_url": "http://test.com",
            "og_image": "http://test.com/og.png",
        },
        legal_pages={
            "terms": {
                "title": "Términos y condiciones",
                "last_updated": "2026-06-19",
                "introduction": "Test",
                "sections": [{"title": "Test", "paragraphs": ["Test"]}],
            }
        },
        footer={
            "cta_title": "Test CTA Title",
            "cta_label": "Test CTA Label",
            "whatsapp_text": "Test WhatsApp text",
            "terms_label": "Test Terms Label",
            "terms_href": "/terminos-y-condiciones",
            "copyright_suffix": "Test copyright suffix",
        },
    )


@pytest.fixture(autouse=True)
def setup_dependency_overrides():
    app.dependency_overrides[get_contenido] = override_get_contenido
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio  # type: ignore
async def test_home_has_single_h1_and_meta_tags():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    text = response.text
    assert text.count("<h1") == 1
    assert "<meta name='description'" in text
    assert "<link rel='canonical'" in text
    assert "<meta property='og:title'" in text
    assert "<meta property='og:image'" in text
    assert "<meta property='og:image:width' content='1200'" in text
    assert "<meta property='og:image:height' content='630'" in text
    assert "application/ld+json" in text
    assert "https://datamaq.com.ar/" in text  # canonical forced to production base URL and no query params


@pytest.mark.asyncio  # type: ignore
async def test_contact_has_h1():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")

    assert response.status_code == 200
    assert response.text.count("<h1") == 1
    assert "contact-hero-title" in response.text


@pytest.mark.asyncio  # type: ignore
async def test_404_has_noindex():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response_unknown = await ac.get("/pagina-que-no-existe")
        response_business = await ac.get("/cursos/curso-que-no-existe")

    assert response_unknown.status_code == 404
    assert "noindex" in response_unknown.text

    assert response_business.status_code == 404
    assert "noindex" in response_business.text


@pytest.mark.asyncio  # type: ignore
async def test_service_cards_use_heading_tags():
    """Verifica que las tarjetas de contenido de la Home institucional (Noticias/Eventos/
    Comunicados, Carreras, Estudiantes, Sedes) usen headings semánticos <h3>, ya sin las
    tarjetas de "servicios" comerciales de DataMaq."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert 'c-inst-card__title"' in response.text
    assert "<h3" in response.text


import json
import re


def parse_json_ld_blocks(html: str) -> list:
    """
    Busca todos los bloques <script type="application/ld+json"> en el HTML
    y los carga como objetos JSON. Levanta AssertionError en caso de sintaxis inválida.
    """
    pattern = re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', re.DOTALL)
    blocks = pattern.findall(html)
    parsed = []
    for b in blocks:
        try:
            parsed.append(json.loads(b.strip()))
        except json.JSONDecodeError as e:
            pytest.fail(f"Sintaxis JSON-LD corrupta o inválida: {b}\nError: {e}")
    return parsed


def get_json_ld_by_type(json_ld_list, target_type):
    """
    Busca en una lista de diccionarios de JSON-LD el tipo especificado,
    manejando tanto estructuras planas como anidadas bajo @graph.
    """
    for item in json_ld_list:
        if isinstance(item, dict):
            if "@graph" in item:
                for sub_item in item["@graph"]:
                    if isinstance(sub_item, dict) and sub_item.get("@type") == target_type:
                        return sub_item
            elif item.get("@type") == target_type:
                return item
    return None


@pytest.mark.asyncio  # type: ignore
async def test_json_ld_syntax_and_schemas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Validar Home (Organization, WebPage, FAQPage)
        response_home = await ac.get("/")
        assert response_home.status_code == 200
        json_lds_home = parse_json_ld_blocks(response_home.text)
        assert len(json_lds_home) > 0, "No se encontraron bloques JSON-LD en la Home"

        org = get_json_ld_by_type(json_lds_home, "Organization")
        webpage = get_json_ld_by_type(json_lds_home, "WebPage")
        faq = get_json_ld_by_type(json_lds_home, "FAQPage")

        assert org is not None, "Falta JSON-LD de tipo Organization en la Home"
        assert webpage is not None, "Falta JSON-LD de tipo WebPage en la Home"
        assert faq is not None, "Falta JSON-LD de tipo FAQPage en la Home"

        assert org.get("name") is not None
        assert webpage.get("name") is not None
        assert faq.get("mainEntity") is not None


@pytest.mark.asyncio  # type: ignore
async def test_json_ld_cursos_and_breadcrumbs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Validar Detalle del Curso (Course, BreadcrumbList)
        response_detail = await ac.get("/cursos/procesamiento-imagenes-python-opencv")
        assert response_detail.status_code == 200
        json_lds_detail = parse_json_ld_blocks(response_detail.text)

        course = get_json_ld_by_type(json_lds_detail, "Course")
        breadcrumbs_detail = get_json_ld_by_type(json_lds_detail, "BreadcrumbList")

        assert course is not None, "Falta JSON-LD de tipo Course en el detalle del curso"
        assert breadcrumbs_detail is not None, "Falta JSON-LD de tipo BreadcrumbList en el detalle del curso"
        assert "Procesamiento Digital de Imágenes" in course.get("name", "")
        assert len(breadcrumbs_detail.get("itemListElement", [])) == 3

        # 2. Validar Lección (BreadcrumbList)
        response_lesson = await ac.get("/cursos/procesamiento-imagenes-python-opencv/entorno-virtual-requirements")
        assert response_lesson.status_code == 200
        json_lds_lesson = parse_json_ld_blocks(response_lesson.text)

        breadcrumbs_lesson = get_json_ld_by_type(json_lds_lesson, "BreadcrumbList")
        assert breadcrumbs_lesson is not None, "Falta JSON-LD de tipo BreadcrumbList en la página de lección"
        assert len(breadcrumbs_lesson.get("itemListElement", [])) == 3
        # Comprobar que el tercer elemento es la lección actual
        assert "Entorno virtual" in breadcrumbs_lesson["itemListElement"][2]["name"]


from src.infrastructure.settings import config


@pytest.mark.asyncio  # type: ignore
async def test_cache_control_and_gzip_headers():
    original_debug = config.DEBUG
    config.DEBUG = False
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/", headers={"Accept-Encoding": "gzip"})

        assert response.status_code == 200
        cache_control = response.headers.get("cache-control", "")
        assert "no-cache" in cache_control
        assert "must-revalidate" in cache_control
        assert "public" not in cache_control
    finally:
        config.DEBUG = original_debug


@pytest.mark.asyncio  # type: ignore
async def test_new_breadcrumbs_and_tech_article():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Validar /cursos listado
        res_cursos = await ac.get("/cursos")
        json_cursos = parse_json_ld_blocks(res_cursos.text)
        bc_cursos = get_json_ld_by_type(json_cursos, "BreadcrumbList")
        assert bc_cursos is not None

        # Validar /casos listado
        res_casos = await ac.get("/casos")
        json_casos = parse_json_ld_blocks(res_casos.text)
        bc_casos = get_json_ld_by_type(json_casos, "BreadcrumbList")
        assert bc_casos is not None

        # Validar /contact
        res_contact = await ac.get("/contact")
        json_contact = parse_json_ld_blocks(res_contact.text)
        bc_contact = get_json_ld_by_type(json_contact, "BreadcrumbList")
        assert bc_contact is not None

        # Validar /terminos-y-condiciones
        res_terms = await ac.get("/terminos-y-condiciones")
        json_terms = parse_json_ld_blocks(res_terms.text)
        bc_terms = get_json_ld_by_type(json_terms, "BreadcrumbList")
        assert bc_terms is not None


# --- Tests de rutas SEO dinámicas (provincia, municipio, localidad) ---


@pytest.mark.asyncio
async def test_provincia_inexistente_404():
    """Verifica que una provincia inexistente devuelve 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/provincia-que-no-existe")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_municipio_inexistente_404():
    """Verifica que un municipio inexistente devuelve 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/buenos-aires/municipio-que-no-existe")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_localidad_inexistente_404():
    """Verifica que una localidad inexistente devuelve 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/buenos-aires/escobar/localidad-que-no-existe.html")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_healthz_endpoint():
    """Verifica que el endpoint de liveness responde."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_ready_endpoint():
    """Verifica que el endpoint de readiness responde (DB check)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["checks"]["db_accessible"] is True


@pytest.mark.asyncio
async def test_request_id_header_present():
    """Verifica que el middleware X-Request-ID esta presente en las respuestas."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"].startswith("req_")


@pytest.mark.asyncio
async def test_security_headers_present():
    """Verifica que los security headers estan presentes."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert "max-age=31536000" in response.headers.get("Strict-Transport-Security", "")


@pytest.mark.asyncio
async def test_rate_limit_contact():
    """Verifica que el rate limiting responde 429 tras exceder el limite."""
    from unittest.mock import AsyncMock

    from src.application.gateways.notification_gateway import NotificationGateway
    from src.domain.repositories.lead_repository import LeadRepository
    from src.infrastructure.fastapi.dependencies import get_lead_repository, get_notification_gateway
    from src.infrastructure.fastapi.middleware import _rate_store

    # Limpiar store compartido de rate-limiting para partir de cero
    _rate_store.clear()

    # Mock del gateway para evitar RuntimeError por falta de SMTP
    async def mock_notification_gateway():
        mock = AsyncMock(spec=NotificationGateway)
        mock.notify_lead.return_value = {"status": "sent", "to": "test@test.com"}
        return mock

    app.dependency_overrides[get_notification_gateway] = mock_notification_gateway

    transport = ASGITransport(app=app)
    payload = {
        "name": "Test User",
        "comment": "Test comment",
        "email": "test@example.com",
        "pageLocation": "http://test/contact",
    }

    # Mock del repositorio de leads para evitar dependencia de MySQL
    async def mock_lead_repo():
        mock = AsyncMock(spec=LeadRepository)
        mock.save.return_value = None
        return mock

    app.dependency_overrides[get_lead_repository] = mock_lead_repo

    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # Las primeras 3 requests deberian ser aceptadas (201)
            for _ in range(3):
                r = await ac.post("/api/v1/contact", json=payload)
                assert r.status_code in (201, 500), f"Expected 201 or 500, got {r.status_code}"

            # La cuarta deberia ser rate-limited (429)
            response = await ac.post("/api/v1/contact", json=payload)
            assert response.status_code == 429, f"Expected 429, got {response.status_code}"
    finally:
        _rate_store.clear()
        app.dependency_overrides.pop(get_notification_gateway, None)
        app.dependency_overrides.pop(get_lead_repository, None)


