import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio  # type: ignore
async def test_guias_list_endpoint_returns_200() -> None:
    """Verifica que el listado /guias siga disponible, sin guías retiradas."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/guias")

    assert response.status_code == 200
    text = response.text
    assert "Resolución ENRE 544/2024" not in text
    assert "Optimización de Potencia Contratada" not in text
    assert "Retrofit IoT Industrial" not in text


@pytest.mark.asyncio  # type: ignore
async def test_guia_detail_retirada_responde_404() -> None:
    """Las guías retiradas no se sirven, ni con slug ni con sufijo .html."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response1 = await ac.get("/guias/enre-544-2024-evitar-cortes-cos-phi")
        response2 = await ac.get("/guias/guia-calculo-potencia-contratada-t2-t3.html")
        response3 = await ac.get("/guias/como-digitalizar-maquinas-modbus-gateway-iot.html")

    assert response1.status_code == 404
    assert response2.status_code == 404
    assert response3.status_code == 404


@pytest.mark.asyncio  # type: ignore
async def test_guia_not_found_returns_404() -> None:
    """Verifica que una guía inexistente retorne 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/guias/guia-inexistente-12345")
        assert response.status_code == 404


def test_data_service_guias() -> None:
    """Las guías fueron retiradas del portal: DataService no debe cargar ninguna."""
    service = DataService()
    assert service.get_guias() == []
    assert service.get_guia_por_slug("enre-544-2024-evitar-cortes-cos-phi") is None
