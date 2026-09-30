"""Pruebas de la validación de campos obligatorios del formulario de contacto.

Cubren la regla de negocio: nombre obligatorio, tecnicatura y situación de
estudios secundarios obligatorias, y "al menos un canal de contacto" (email o
teléfono) en el backend; más una auditoría del código fuente de
FormManager.js y home_sections.yaml para verificar que la validación de UI y
la fuente única de configuración (`required`) están presentes.
"""

from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import yaml
from httpx import ASGITransport, AsyncClient

from src.application.gateways.notification_gateway import NotificationGateway
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_lead_repository, get_notification_gateway
from src.infrastructure.fastapi.middleware import _rate_store

REPO_ROOT = Path(__file__).resolve().parent.parent
FORM_MANAGER_JS = REPO_ROOT / "static/js/modules/FormManager.js"
CONTACT_FORM_TEMPLATE = REPO_ROOT / "templates/partials/components/contact_form.html"
CONTENT_YAML = REPO_ROOT / "data/content/home_sections.yaml"


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


# --- Backend: nombre obligatorio ---


@pytest.mark.asyncio  # type: ignore
async def test_backend_rechaza_nombre_vacio() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "name": "",
        "comment": "Consulta real",
        "email": "aspirante@example.com",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio  # type: ignore
async def test_backend_rechaza_nombre_demasiado_corto() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "name": "A",
        "comment": "Consulta real",
        "email": "aspirante@example.com",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 422


# --- Backend: al menos un canal de contacto (email o teléfono) ---


@pytest.mark.asyncio  # type: ignore
async def test_backend_rechaza_sin_email_ni_telefono() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "name": "Aspirante Real",
        "comment": "Quiero info sobre la tecnicatura",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 422
    assert "correo" in response.text.lower() or "teléfono" in response.text.lower() or "telefono" in response.text.lower()


@pytest.mark.asyncio  # type: ignore
async def test_backend_acepta_email_sin_telefono() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "name": "Aspirante Real",
        "comment": "",
        "email": "aspirante@example.com",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    assert response.json()["submitStatus"] == "success"


@pytest.mark.asyncio  # type: ignore
async def test_backend_acepta_telefono_sin_email() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "name": "Aspirante Real",
        "comment": "",
        "phone": "+54 11 5000 1234",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    assert response.json()["submitStatus"] == "success"


@pytest.mark.asyncio  # type: ignore
async def test_backend_acepta_email_y_telefono() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "name": "Aspirante Real",
        "comment": "Consulta con ambos canales",
        "email": "aspirante@example.com",
        "phone": "+54 11 5000 1234",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201
    assert response.json()["submitStatus"] == "success"


@pytest.mark.asyncio  # type: ignore
async def test_backend_acepta_campos_opcionales_vacios_cuando_se_cumplen_obligatorios() -> None:
    """Company, empresa/cargo (comment) y demás campos opcionales vacíos no deben bloquear el envío."""
    transport = ASGITransport(app=app)
    payload = {
        "name": "Aspirante Real",
        "comment": "",
        "email": "aspirante@example.com",
        "company": None,
        "phone": None,
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/contact", json=payload)

    assert response.status_code == 201


# --- Auditoría de fuente única de configuración (home_sections.yaml) ---


def test_home_sections_yaml_define_required_por_campo() -> None:
    data = yaml.safe_load(CONTENT_YAML.read_text(encoding="utf-8"))
    steps = data["contact"]["steps"]

    campo_a_required = {
        field["id"]: field.get("required", False) for step in steps for field in step["fields"]
    }

    assert campo_a_required["contacto-nombre"] is True
    assert campo_a_required["contacto-empresa"] is False
    assert campo_a_required["contacto-cargo"] is False
    assert campo_a_required["contacto-servicio"] is True
    assert campo_a_required["contacto-tarifa"] is True
    assert campo_a_required["contacto-comentario"] is False
    # Email y teléfono NO deben ser individualmente required=true:
    # la regla es "al menos uno de los dos" (validación de grupo).
    assert campo_a_required["contacto-email"] is False
    assert campo_a_required["contacto-telefono"] is False


def test_home_sections_yaml_incluye_mensajes_de_validacion() -> None:
    data = yaml.safe_load(CONTENT_YAML.read_text(encoding="utf-8"))
    contact = data["contact"]

    assert "required_text" in contact
    assert "contact_channel_note" in contact
    assert "validation_messages" in contact
    assert "contacto-nombre" in contact["validation_messages"]
    assert "contacto-servicio" in contact["validation_messages"]
    assert "contacto-tarifa" in contact["validation_messages"]
    assert "contact_channel" in contact["validation_messages"]


# --- Auditoría del template: atributos required/aria-required por campo ---


@pytest.mark.asyncio  # type: ignore
async def test_contact_page_renderiza_atributos_required_en_campos_obligatorios() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")

    assert response.status_code == 200
    html = response.text

    assert 'data-field-id="contacto-nombre"' in html
    assert 'data-required="true"' in html
    assert 'data-field-id="contacto-email"' in html
    assert 'data-required="false"' in html


@pytest.mark.asyncio  # type: ignore
async def test_contact_page_email_y_telefono_no_aparecen_como_solo_opcional() -> None:
    """El Paso 3 debe mostrar la ayuda condicional en vez de un simple 'Opcional',
    para que quede claro que se exige al menos uno de los dos canales."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact")

    assert response.status_code == 200
    html = response.text

    assert "Obligatorio si no ingresás teléfono." in html
    assert "Obligatorio si no ingresás correo." in html

    # El texto genérico "Opcional" no debe ser el que se muestra para email/teléfono:
    # se busca específicamente en el bloque del Paso 3 (Canales de Contacto).
    inicio_paso3 = html.index("3. Canales de Contacto")
    bloque_paso3 = html[inicio_paso3:]
    assert "Opcional</small>" not in bloque_paso3


# --- Auditoría de FormManager.js: validación de paso presente y sin placeholders ---


def test_form_manager_valida_pasos_antes_de_avanzar_o_enviar() -> None:
    contenido = FORM_MANAGER_JS.read_text(encoding="utf-8")
    assert "validateStep(" in contenido
    assert "handleNextOrSubmit()" in contenido
    indice_handle = contenido.index("handleNextOrSubmit() {")
    bloque_handle = contenido[indice_handle : indice_handle + 400]
    assert "this.validateStep(this.currentStep)" in bloque_handle


def test_form_manager_no_disfraza_campos_vacios_con_placeholders() -> None:
    contenido = FORM_MANAGER_JS.read_text(encoding="utf-8")
    assert "'Contacto Web'" not in contenido
    assert "'Consulta desde formulario web'" not in contenido


def test_form_manager_valida_regla_de_grupo_email_o_telefono() -> None:
    contenido = FORM_MANAGER_JS.read_text(encoding="utf-8")
    assert "contacto-email" in contenido
    assert "contacto-telefono" in contenido
    assert "hasChannel" in contenido


def test_contact_form_template_incluye_nota_de_canal_de_contacto() -> None:
    contenido = CONTACT_FORM_TEMPLATE.read_text(encoding="utf-8")
    assert "contact_channel_note" in contenido
    assert "contact_channel-error" in contenido
