"""La pantalla /campus muestra la estructura del campus virtual con datos de muestra.

El módulo todavía no existe: no hay estudiantes, notas ni asistencias reales.
Por eso la ruta solo está disponible con DEBUG=true y nunca puede publicarse
como si fuera información de una persona.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app
from src.infrastructure.settings import config


def cliente() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


def test_los_datos_de_muestra_validan_contra_el_modelo() -> None:
    campus = DataService(data_dir="data").get_campus_muestra()

    assert campus.estudiante.nombre == "Nombre Apellido"
    assert campus.materias, "la tabla de materias no puede quedar vacía"
    assert campus.finales
    assert all(0 <= materia.asistencia <= 100 for materia in campus.materias)


@pytest.mark.asyncio
async def test_campus_no_existe_en_produccion(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", False)
    async with cliente() as ac:
        respuesta = await ac.get("/campus")

    assert respuesta.status_code == 404
    assert "Nombre Apellido" not in respuesta.text


@pytest.mark.asyncio
async def test_campus_en_debug_muestra_la_estructura(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", True)
    async with cliente() as ac:
        respuesta = await ac.get("/campus")

    assert respuesta.status_code == 200
    html = respuesta.text
    assert "Mi cursada" in html
    assert "Materias en curso" in html
    assert "Finales disponibles" in html
    assert "Mis trámites" in html
    assert "css/campus.css" in html


@pytest.mark.asyncio
async def test_campus_avisa_que_los_datos_son_de_muestra(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "DEBUG", True)
    async with cliente() as ac:
        respuesta = await ac.get("/campus")

    html = respuesta.text
    assert 'class="banda-prototipo"' in html
    assert "no corresponden a ninguna persona" in html
    assert '<meta name="robots" content="noindex, nofollow">' in html
