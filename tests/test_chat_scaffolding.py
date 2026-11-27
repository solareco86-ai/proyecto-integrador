from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient, Response

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_chat_health_endpoint() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        response: Response = await cliente.get("/api/v1/chat/health")

    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["modules"], dict)


@pytest.mark.asyncio
async def test_chat_text_valid_request() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "session_id": "test-session-123",
        "message": "¿Qué tecnicaturas se cursan en el ISFT 199?",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        response: Response = await cliente.post("/api/v1/chat/text", json=payload)

    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    assert "reply" in data
    assert "intent" in data
    assert "sources" in data
    assert "confidence" in data
    assert isinstance(data["reply"], str)
    assert len(data["reply"]) > 0
    assert isinstance(data["sources"], list)
    assert 0.0 <= float(data["confidence"]) <= 1.0


@pytest.mark.asyncio
async def test_chat_text_empty_message_returns_422() -> None:
    transport = ASGITransport(app=app)
    payload = {
        "session_id": "test-session-123",
        "message": "   ",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        response: Response = await cliente.post("/api/v1/chat/text", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_text_message_exceeding_max_length_returns_422(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CHAT_MAX_MESSAGE_LENGTH", "50")
    transport = ASGITransport(app=app)
    payload = {
        "session_id": "test-session-123",
        "message": "a" * 51,
    }
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        response: Response = await cliente.post("/api/v1/chat/text", json=payload)

    assert response.status_code == 422
