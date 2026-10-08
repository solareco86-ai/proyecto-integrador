"""La vista previa de componentes /dev/preview es una herramienta de desarrollo.
En producción (DEBUG=False) no debe existir: no basta con noindex, porque
/dev/preview/planes renderizaba el catálogo comercial de DataMaq (AGENTS.md §7.1).
"""
import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app
from src.infrastructure.settings import config

PARCIALES: tuple[str, ...] = ("planes", "process", "proof_strip", "icon", "no-existe")
def cliente() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
@pytest.mark.asyncio
@pytest.mark.parametrize("parcial", PARCIALES)
async def test_preview_no_existe_en_produccion(parcial: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", False)
    async with cliente() as ac:
        respuesta = await ac.get(f"/dev/preview/{parcial}")
    assert respuesta.status_code == 404
    assert "Instalación de Hardware" not in respuesta.text
    assert "A cotizar" not in respuesta.text
@pytest.mark.asyncio
async def test_preview_planes_no_muestra_catalogo_comercial_en_produccion(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", False)
    async with cliente() as ac:
        respuesta = await ac.get("/dev/preview/planes")
    for texto in ("Powermeter", "Banco Provincia", "Pactar"):
        assert texto not in respuesta.text
@pytest.mark.asyncio
async def test_preview_sigue_disponible_en_debug(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", True)
    async with cliente() as ac:
        respuesta = await ac.get("/dev/preview/icon")
    assert respuesta.status_code == 200
    assert respuesta.headers["x-robots-tag"] == "noindex, nofollow"
