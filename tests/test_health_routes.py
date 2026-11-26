"""Contrato HTTP de liveness y readiness, con repositorio doble y sin conexiones reales."""

from typing import cast
from unittest.mock import AsyncMock, Mock

import pytest
from httpx import ASGITransport, AsyncClient, Response

from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.fastapi import dependencies
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.routes import main_routes


@pytest.fixture
def repositorio_salud(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    repositorio: AsyncMock = AsyncMock(spec=LeadRepository)

    def obtener_repositorio() -> LeadRepository:
        return cast(LeadRepository, repositorio)

    # /ready importa esta función dentro del endpoint, sin Depends.
    monkeypatch.setattr(dependencies, "get_lead_repository", obtener_repositorio)
    return repositorio


@pytest.mark.asyncio
async def test_healthz_responde_sin_comprobar_la_base(repositorio_salud: AsyncMock) -> None:
    repositorio_salud.is_healthy.side_effect = RuntimeError("Base de prueba no disponible")
    transport: ASGITransport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        respuesta: Response = await cliente.get("/healthz")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "ok"}
    repositorio_salud.is_healthy.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("disponible", [True, False], ids=["base-disponible", "base-no-disponible"])
async def test_ready_refleja_disponibilidad_de_la_base(repositorio_salud: AsyncMock, disponible: bool) -> None:
    repositorio_salud.is_healthy.return_value = disponible
    transport: ASGITransport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        respuesta: Response = await cliente.get("/ready")

    assert respuesta.status_code == (200 if disponible else 503)
    assert respuesta.json() == {
        "status": "ok" if disponible else "not_ready",
        "checks": {"db_accessible": disponible},
    }
    repositorio_salud.is_healthy.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_ready_devuelve_503_si_falla_la_comprobacion(
    repositorio_salud: AsyncMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    registrar_excepcion: Mock = Mock()
    monkeypatch.setattr(main_routes.logger, "exception", registrar_excepcion)
    repositorio_salud.is_healthy.side_effect = RuntimeError("Fallo simulado al comprobar la base")
    transport: ASGITransport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        respuesta: Response = await cliente.get("/ready")

    assert respuesta.status_code == 503
    assert respuesta.json() == {"status": "not_ready", "checks": {"db_accessible": False}}
    registrar_excepcion.assert_called_once_with("Error al comprobar la disponibilidad de la base de datos")
    repositorio_salud.is_healthy.assert_awaited_once_with()
