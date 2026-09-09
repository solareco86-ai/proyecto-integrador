"""Tests del endpoint /metrics y del registro de métricas operativas (OBS-06)."""

from collections.abc import Iterator
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient  # type: ignore

from src.application.gateways.notification_gateway import NotificationGateway
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_lead_repository, get_notification_gateway
from src.infrastructure.fastapi.metrics import Counter, MetricsRegistry, Summary, registry
from src.infrastructure.fastapi.middleware import _rate_store


@pytest.fixture(autouse=True)
def _reset_metrics() -> Iterator[None]:
    _rate_store.clear()
    registry.leads_created_total = Counter("leads_created_total", "Total de leads persistidos")
    registry.smtp_send_failures_total = Counter("smtp_send_failures_total", "Fallos de notificación")
    registry.http_requests_total = Counter("http_requests_total", "Requests HTTP", labels=("method", "path", "status"))
    registry.http_request_duration_seconds = Summary("http_request_duration_seconds", "Duración de requests")
    yield


async def override_get_notification_gateway_ok() -> NotificationGateway:
    mock = AsyncMock(spec=NotificationGateway)
    mock.notify_lead.return_value = {"status": "sent", "channel": "email"}
    return mock


async def override_get_notification_gateway_fail() -> NotificationGateway:
    mock = AsyncMock(spec=NotificationGateway)
    mock.notify_lead.side_effect = RuntimeError("SMTP caído")
    return mock


async def override_get_lead_repository_ok() -> LeadRepository:
    mock = AsyncMock(spec=LeadRepository)
    mock.save.return_value = None
    mock.is_healthy.return_value = True
    return mock


def _contact_payload() -> dict[str, str]:
    return {"name": "Juan", "comment": "Consulta", "email": "juan@test.com"}


# --- Contadores puros ---


def test_counter_sin_labels_incrementa_y_renderiza() -> None:
    c = Counter("leads_created_total", "Total de leads persistidos")
    c.inc(3)
    assert c.get() == 3.0
    assert "leads_created_total 3.0" in c._render()[0]


def test_counter_con_labels_renderiza_labels() -> None:
    c = Counter("http_requests_total", "Requests HTTP", labels=("method", "path", "status"))
    c.inc(label_values=("GET", "/", "200"))
    rendered = "\n".join(c._render())
    assert 'http_requests_total{method="GET",path="/",status="200"} 1.0' in rendered


def test_summary_observa_suma_y_conteo() -> None:
    s = Summary("http_request_duration_seconds", "Duración de requests")
    s.observe(0.5)
    s.observe(0.25)
    rendered = "\n".join(s._render())
    assert "http_request_duration_seconds_sum 0.75" in rendered
    assert "http_request_duration_seconds_count 2.0" in rendered


# --- Endpoint y middleware ---


@pytest.mark.asyncio
async def test_metrics_endpoint_formato_prometheus() -> None:
    app.dependency_overrides[get_lead_repository] = override_get_lead_repository_ok
    app.dependency_overrides[get_notification_gateway] = override_get_notification_gateway_ok
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/metrics")
            assert resp.status_code == 200
            assert resp.headers["content-type"].startswith("text/plain")
            assert "# TYPE leads_created_total counter" in resp.text
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_post_contact_incrementa_leads_created() -> None:
    app.dependency_overrides[get_lead_repository] = override_get_lead_repository_ok
    app.dependency_overrides[get_notification_gateway] = override_get_notification_gateway_ok
    try:
        before = registry.leads_created_total.get()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post("/api/v1/contact", json=_contact_payload())
            assert resp.status_code == 201
        assert registry.leads_created_total.get() == before + 1.0
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_post_contact_fallo_notificacion_incrementa_smtp_failures() -> None:
    app.dependency_overrides[get_lead_repository] = override_get_lead_repository_ok
    app.dependency_overrides[get_notification_gateway] = override_get_notification_gateway_fail
    try:
        before = registry.smtp_send_failures_total.get()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post("/api/v1/contact", json=_contact_payload())
            assert resp.status_code == 201
        assert registry.smtp_send_failures_total.get() == before + 1.0
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_metrics_no_se_autocuenta() -> None:
    app.dependency_overrides[get_lead_repository] = override_get_lead_repository_ok
    app.dependency_overrides[get_notification_gateway] = override_get_notification_gateway_ok
    try:
        before = registry.http_requests_total.get(label_values=("GET", "/metrics", "200"))
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await client.get("/metrics")
        after = registry.http_requests_total.get(label_values=("GET", "/metrics", "200"))
        assert after == before
    finally:
        app.dependency_overrides.clear()


def test_registry_es_instancia_de_metrics_registry() -> None:
    assert isinstance(registry, MetricsRegistry)
