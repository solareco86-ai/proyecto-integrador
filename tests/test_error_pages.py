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
        assert "/carreras" in response.text
        assert "/contact" in response.text
@pytest.mark.asyncio
async def test_404_no_ofrece_contenido_comercial():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://isftn199.com.ar") as client:
        response = await client.get("/esta-ruta-no-existe-para-test-404")
    assert response.status_code == 404
    cuerpo = response.text
    for enlace_comercial in ("/landing/", "/pricing", "/planes"):
        assert f'href="{enlace_comercial}' not in cuerpo
    for texto_comercial in ("Precios y Financiamiento", "Retrofit IoT", "Factor de Potencia"):
        assert texto_comercial not in cuerpo
@pytest.mark.asyncio
async def test_404_accesos_rapidos_provienen_de_los_datos():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://isftn199.com.ar") as client:
        response = await client.get("/esta-ruta-no-existe-para-test-404")
    for destino in ("/carreras", "/cursos", "/inscripciones", "/contact"):
        assert f'href="{destino}"' in response.text


@pytest.mark.asyncio
async def test_500_error_page_handler():
    handler = app.exception_handlers.get(HTTPException)
    assert handler is not None
