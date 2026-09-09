"""Tests de endurecimiento de logs del flujo transaccional (OBS-04, OBS-10, OBS-14)."""

import logging
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient  # type: ignore

from src.application.gateways.notification_gateway import NotificationGateway
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_lead_repository, get_notification_gateway
from src.infrastructure.fastapi.middleware import _rate_store

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _reset_rate_store() -> Iterator[None]:
    _rate_store.clear()
    yield


async def override_notification_ok() -> NotificationGateway:
    mock = AsyncMock(spec=NotificationGateway)
    mock.notify_lead.return_value = {"status": "sent", "channel": "email"}
    return mock


async def override_repo_falla() -> LeadRepository:
    mock = AsyncMock(spec=LeadRepository)
    mock.save.side_effect = ValueError("SECRETO_INTERNO_XYZ")
    return mock


async def override_repo_ok() -> LeadRepository:
    mock = AsyncMock(spec=LeadRepository)
    mock.save.return_value = None
    mock.is_healthy.return_value = True
    return mock


def _contact_payload() -> dict[str, str]:
    return {"name": "Juan", "comment": "Consulta", "email": "juan@test.com"}


@pytest.mark.asyncio
async def test_500_no_expone_internals() -> None:
    app.dependency_overrides[get_lead_repository] = override_repo_falla
    app.dependency_overrides[get_notification_gateway] = override_notification_ok
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post("/api/v1/contact", json=_contact_payload())
            assert resp.status_code == 500
            assert "SECRETO_INTERNO_XYZ" not in resp.text
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_500_loguea_stack_trace(caplog: pytest.LogCaptureFixture) -> None:
    app.dependency_overrides[get_lead_repository] = override_repo_falla
    app.dependency_overrides[get_notification_gateway] = override_notification_ok
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            with caplog.at_level(logging.ERROR, logger="app"):
                await client.post("/api/v1/contact", json=_contact_payload())
        assert any(r.exc_info is not None for r in caplog.records)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_request_id_se_loguea(caplog: pytest.LogCaptureFixture) -> None:
    app.dependency_overrides[get_lead_repository] = override_repo_ok
    app.dependency_overrides[get_notification_gateway] = override_notification_ok
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            with caplog.at_level(logging.INFO, logger="app"):
                await client.post(
                    "/api/v1/contact",
                    json=_contact_payload(),
                    headers={"X-Request-ID": "req_test_123"},
                )
        assert "req_test_123" in caplog.text
    finally:
        app.dependency_overrides.clear()


def test_dependencies_sin_fstring_en_warning() -> None:
    contenido = (REPO_ROOT / "src/infrastructure/fastapi/dependencies.py").read_text(encoding="utf-8")
    assert 'logger.warning(f"' not in contenido
