import pytest
from httpx import ASGITransport, AsyncClient
from starlette.exceptions import HTTPException

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_404_error_page():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://datamaq.com.ar") as client:
        response = await client.get("/esta-ruta-no-existe-para-test-404")
        assert response.status_code == 404
        assert "Página no encontrada" in response.text
        assert "Error 404" in response.text
        assert "/landing/calidad-energia" in response.text
        assert "/landing/telemetria-industrial" in response.text
        assert "wa.me" in response.text


@pytest.mark.asyncio
async def test_500_error_page_handler():
    handler = app.exception_handlers.get(HTTPException)
    assert handler is not None
