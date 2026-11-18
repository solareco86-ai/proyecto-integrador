"""Cuenta regresiva del cierre de inscripción.

`dias_restantes` es una función pura del dominio: la portada la usa para mostrar
cuántos días faltan a partir de la fecha cargada en data/, sin escribir el
número a mano.
"""

from collections.abc import Iterator
from datetime import UTC, date, datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.dtos.content_dto import CierreInscripcionModel
from src.domain.common import fechas
from src.domain.common.fechas import dias_restantes
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import data_service, get_contenido

HOY = date(2026, 11, 18)


def test_cuenta_los_dias_que_faltan() -> None:
    assert dias_restantes("2026-11-28", hoy=HOY) == 10
    assert dias_restantes("2026-11-19", hoy=HOY) == 1


def test_el_mismo_dia_del_cierre_da_cero() -> None:
    assert dias_restantes("2026-11-18", hoy=HOY) == 0


def test_un_plazo_vencido_no_da_numeros_negativos() -> None:
    assert dias_restantes("2026-11-17", hoy=HOY) is None


@pytest.mark.parametrize("fecha", ["", "28 nov 2026", "2026-13-01", None])
def test_una_fecha_ilegible_no_rompe_la_portada(fecha: str) -> None:
    assert dias_restantes(fecha, hoy=HOY) is None


def test_hoy_es_la_fecha_argentina_y_no_la_de_utc(monkeypatch: pytest.MonkeyPatch) -> None:
    """A las 22:00 de Argentina en UTC ya es el día siguiente: no debe restar un día."""

    class RelojFijo(datetime):
        @classmethod
        def now(cls, tz=None):  # type: ignore[override]
            # 18-nov 22:00 en Argentina = 19-nov 01:00 en UTC
            instante = datetime(2026, 11, 19, 1, 0, tzinfo=UTC)
            return instante.astimezone(tz) if tz else instante.replace(tzinfo=None)

    monkeypatch.setattr(fechas, "datetime", RelojFijo)
    assert fechas.hoy_en_argentina() == date(2026, 11, 18)
    assert dias_restantes("2026-11-19") == 1


def _contenido_con_cierre(fecha: date) -> Iterator[None]:
    contenido = data_service.get_contenido().model_copy(deep=True)
    assert contenido.content.admision is not None
    contenido.content.admision.cierre = CierreInscripcionModel(
        fecha_iso=fecha.isoformat(), fecha_texto="FECHA-DE-PRUEBA"
    )
    app.dependency_overrides[get_contenido] = lambda: contenido
    yield
    app.dependency_overrides.pop(get_contenido, None)


@pytest.fixture
def cierre_en_cinco_dias() -> Iterator[None]:
    yield from _contenido_con_cierre(fechas.hoy_en_argentina() + timedelta(days=5))


@pytest.fixture
def cierre_vencido() -> Iterator[None]:
    yield from _contenido_con_cierre(fechas.hoy_en_argentina() - timedelta(days=1))


async def _portada() -> str:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        respuesta = await ac.get("/")
    assert respuesta.status_code == 200
    return respuesta.text


@pytest.mark.asyncio
@pytest.mark.usefixtures("cierre_en_cinco_dias")
async def test_la_portada_muestra_los_dias_que_faltan() -> None:
    html = await _portada()
    assert '<p class="contador__n">5</p>' in html
    assert "días para el cierre de la inscripción · FECHA-DE-PRUEBA" in html


@pytest.mark.asyncio
@pytest.mark.usefixtures("cierre_vencido")
async def test_la_portada_avisa_si_la_inscripcion_cerro() -> None:
    html = await _portada()
    assert "La inscripción cerró el FECHA-DE-PRUEBA" in html
    assert "para el cierre de la inscripción" not in html


@pytest.mark.asyncio
async def test_sin_fecha_oficial_no_hay_cuenta_regresiva() -> None:
    """Hoy data/ no trae fecha de cierre: la portada no inventa un plazo (AGENTS.md 7.5)."""
    html = await _portada()
    assert "para el cierre de la inscripción" not in html
    assert 'id="sedes"' in html
