"""Fixtures compartidas para los tests de datamaq.com.ar."""

import os

# SECRET_KEY de prueba, aislada del entorno real: se setea ANTES de que
# cualquier test module importe `src.infrastructure.settings.config` (que la
# exige con fail-fast cuando DEBUG=False, como es el caso en la suite de
# tests). No es una clave real ni se usa fuera de este proceso de test.
os.environ.setdefault("SECRET_KEY", "test-only-secret-key-not-for-production-use")

import pytest

from src.application.dtos import ContenidoModel


@pytest.fixture
def mock_contenido() -> ContenidoModel:
    """ContenidoModel mínimo y válido para tests de rutas."""
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
                "services": {
                    "title": "Test",
                    "cards": [
                        {
                            "id": "test-service",
                            "title": "Test",
                            "description": "Test",
                            "problem": "Test problem",
                            "key_points": [],
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
                    "steps": [],
                },
                "assistance_modes": {
                    "on_site": {"label": "Campo", "description": "Test", "icon": "geo-alt-fill"},
                    "remote": {"label": "Remoto", "description": "Test", "icon": "wifi"},
                },
                "proof_strip": {"items": [{"label": "Test", "text": "Test"}]},
                "process": {
                    "eyebrow": "Test",
                    "title": "Test",
                    "steps": [{"title": "Step 1", "text": "Test"}],
                },
                "courses": {
                    "badge": "Test",
                    "title": "Test",
                    "subtitle": "Test",
                    "assistance_cta_label": "Test",
                    "assistance_cta_href": "/contact",
                },
                "cases": {"badge": "Test", "title": "Test", "subtitle": "Test"},
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
                },
            },
            "footer": {
                "navigation_groups": [
                    {
                        "title": "Navegación",
                        "links": [
                            {"label": "Inicio", "href": "/"},
                            {"label": "Contacto", "href": "/contact"},
                        ],
                    },
                ],
                "cta_title": "Test",
                "cta_label": "Test",
                "whatsapp_text": "Test",
                "terms_label": "Test",
                "terms_href": "/terminos-y-condiciones",
                "copyright_suffix": "Test",
            },
        }
    )
