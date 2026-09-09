"""Tests de privacidad y hardening frontend (OBS-12, OBS-13, OBS-15, OBS-16)."""

from collections.abc import Iterator
from pathlib import Path

import pytest
import yaml
from httpx import ASGITransport, AsyncClient  # type: ignore

from src.application.dtos import ContenidoModel
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_contenido
from src.infrastructure.settings import config

REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC_JS = REPO_ROOT / "static/js/modules"
CONTENT_YAML = REPO_ROOT / "data/content/home_sections.yaml"


@pytest.fixture
def _override_contenido(mock_contenido: ContenidoModel) -> Iterator[None]:
    app.dependency_overrides[get_contenido] = lambda: mock_contenido
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_preview_telemetry_no_cargado_en_prod(_override_contenido: None, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", False)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/contact")
        assert resp.status_code == 200
        assert "preview-telemetry.js" not in resp.text


@pytest.mark.asyncio
async def test_preview_telemetry_cargado_en_debug(_override_contenido: None, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", True)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/contact")
        assert resp.status_code == 200
        assert "preview-telemetry.js" in resp.text


def test_cookie_manager_fail_closed() -> None:
    contenido = (STATIC_JS / "CookieManager.js").read_text(encoding="utf-8")
    # El bloque catch no debe invocar loadScripts() (fail-closed)
    indice_catch = contenido.index("catch")
    bloque_catch = contenido[indice_catch:]
    assert "loadScripts()" not in bloque_catch


def test_cookie_manager_expone_revocacion() -> None:
    contenido = (STATIC_JS / "CookieManager.js").read_text(encoding="utf-8")
    assert "revokeConsent" in contenido
    assert "removeItem('userConsent')" in contenido


def test_form_manager_no_loguea_payload() -> None:
    contenido = (STATIC_JS / "FormManager.js").read_text(encoding="utf-8")
    assert "console.debug('Enviando payload:" not in contenido


def test_head_sin_beacon_cloudflare() -> None:
    head = (REPO_ROOT / "templates/partials/head.html").read_text(encoding="utf-8")
    assert "beacon.min.js" not in head
    assert "cloudflareinsights.com" not in head


def test_third_party_manager_sin_cloudflare() -> None:
    contenido = (STATIC_JS / "ThirdPartyScriptsManager.js").read_text(encoding="utf-8")
    assert "cloudflare" not in contenido.lower()


def test_banner_cookies_sin_mencion_chat() -> None:
    data = yaml.safe_load(CONTENT_YAML.read_text(encoding="utf-8"))
    texto = data["cookie_banner"]["text"].lower()
    assert "chat" not in texto


def test_modulos_sin_console_debug() -> None:
    """Los módulos de telemetría no deben llamar console.debug directamente."""
    third_party = (STATIC_JS / "ThirdPartyScriptsManager.js").read_text(encoding="utf-8")
    direct_contact = (STATIC_JS / "DirectContactTracker.js").read_text(encoding="utf-8")
    assert "console.debug" not in third_party
    assert "console.debug" not in direct_contact


def test_form_manager_sin_console_info() -> None:
    """El envío exitoso del formulario no debe usar console.info (ruido en producción)."""
    contenido = (STATIC_JS / "FormManager.js").read_text(encoding="utf-8")
    assert "console.info" not in contenido


def test_third_party_manager_emite_tp_blocked() -> None:
    """El bloqueo de scripts de terceros debe despachar el evento de telemetría tp:blocked."""
    contenido = (STATIC_JS / "ThirdPartyScriptsManager.js").read_text(encoding="utf-8")
    assert "tp:blocked" in contenido
    assert "third_party_blocked" in contenido


def test_third_party_manager_dedupe_sesion() -> None:
    """Los avisos de bloqueo deben deduplicarse por sesión (sessionStorage)."""
    contenido = (STATIC_JS / "ThirdPartyScriptsManager.js").read_text(encoding="utf-8")
    assert "sessionStorage" in contenido
    assert "tp:warned:" in contenido
