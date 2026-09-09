"""Contrato: prioridades de la propuesta institucional y académica de ISFT N° 199 en la home.

Verifica que la home comunica Educación Pública Superior Técnica, con foco en Carreras y Tecnicaturas
(Ciencia de Datos e IA, Mecatrónica, Logística, Higiene y Seguridad) y el Campus Virtual.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.application.dtos.content_dto import ContentModel
from src.infrastructure.fastapi.app import app

ORDEN_TARJETAS_ACADEMICAS = [
    "ciencia-de-datos-ia",
    "mecatronica",
    "logistica",
    "higiene-y-seguridad",
]


def _contenido() -> ContentModel:
    return DataService().get_contenido().content


# --- Q1: el hero no contiene ofertas comerciales obsoletas ---
def test_q1_hero_es_institucional() -> None:
    hero = _contenido().hero
    assert "Xubio" not in hero.title
    assert "Educación Pública Superior" in hero.badge
    assert "ISFT N° 199" in hero.subtitle or "tecnicaturas" in hero.subtitle.lower()


# --- Q2: el CTA principal y secundario llevan a carreras e ingreso ---
def test_q2_ctas_hero_academicos() -> None:
    hero = _contenido().hero
    assert hero.primaryCta.href == "/carreras"
    assert hero.secondaryCta.href in ("#ingreso", "/contact")


# --- Q3: 4 tarjetas de ejes formativos académicos ---
def test_q3_tarjetas_ejes_academicos() -> None:
    ids = [card.id for card in _contenido().services.cards]
    assert ids == ORDEN_TARJETAS_ACADEMICAS


# --- Q4: la tarjeta de Ciencia de Datos e IA está completa ---
def test_q4_tarjeta_ciencia_de_datos_completa() -> None:
    cards = {card.id: card for card in _contenido().services.cards}
    datos = cards["ciencia-de-datos-ia"]
    assert "Ciencia de Datos" in datos.title
    assert len(datos.key_points) >= 3
    assert datos.proof is not None
    assert "DGCyE" in datos.proof
    assert datos.cta is not None and datos.cta.strip() != ""


# --- Q5: el formulario ofrece las tecnicaturas oficiales ---
def test_q5_select_offers_tecnicaturas() -> None:
    select = _contenido().contact.steps[1].fields[0]
    assert select.options is not None
    valores = [opcion.value for opcion in select.options]
    assert "ciencia-de-datos-ia" in valores
    assert "mecatronica" in valores
    assert "logistica" in valores
    assert "higiene-y-seguridad" in valores


# --- Q6: proceso, perfil y FAQ con foco académico y gratuito ---
def test_q6_proceso_perfil_faq_academico() -> None:
    contenido = _contenido()
    assert "Inscripción" in contenido.process.eyebrow or "Ingreso" in contenido.process.eyebrow
    assert contenido.profile.description is not None
    assert "docente" in contenido.profile.description.lower() or "académica" in contenido.profile.description.lower()
    faq_text = " ".join(p.answer for p in contenido.faq.questions)
    assert "gratuita" in faq_text.lower() or "pública" in faq_text.lower()


# --- Q7: el encabezado de servicios presenta áreas formativas ---
def test_q7_services_header_academico() -> None:
    servicios = _contenido().services
    assert "Tecnicaturas" in servicios.title or "académica" in servicios.title.lower()
    assert "Xubio" not in servicios.title


# --- Q8: el HTML renderiza ejes formativos y títulos oficiales ---
@pytest.mark.asyncio
async def test_q8_home_renders_ejes_academicos() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    html = response.text
    assert "Ciencia de Datos" in html
    assert "Mecatrónica" in html
    assert "Educación Pública Superior" in html


# --- Q9: el HTML del select renderiza la opción de Ciencia de Datos e IA ---
@pytest.mark.asyncio
async def test_q9_select_renders_ciencia_de_datos() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert 'value="ciencia-de-datos-ia"' in response.text

