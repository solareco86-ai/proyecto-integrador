import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio  # type: ignore
async def test_guias_list_endpoint_returns_200() -> None:
    """Verifica que el listado /guias retorne 200 OK y liste las guías técnicas."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/guias")

    assert response.status_code == 200
    text = response.text
    assert "Trámites y Guías para Estudiantes" in text or "Guías" in text
    assert "Resolución ENRE 544/2024" in text
    assert "Optimización de Potencia Contratada" in text
    assert "Retrofit IoT Industrial" in text


@pytest.mark.asyncio  # type: ignore
async def test_guia_detail_endpoint_returns_200() -> None:
    """Verifica que la página de detalle /guias/{slug} y /{slug}.html retorne 200 OK."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Test sin .html
        response1 = await ac.get("/guias/enre-544-2024-evitar-cortes-cos-phi")
        assert response1.status_code == 200
        assert "Resolución ENRE 544/2024" in response1.text
        assert "Artículo 9" in response1.text
        assert "TechArticle" in response1.text

        # Test con .html
        response2 = await ac.get("/guias/guia-calculo-potencia-contratada-t2-t3.html")
        assert response2.status_code == 200
        assert "Optimización de Potencia Contratada" in response2.text

        response3 = await ac.get("/guias/como-digitalizar-maquinas-modbus-gateway-iot.html")
        assert response3.status_code == 200
        assert "Retrofit IoT Industrial" in response3.text


@pytest.mark.asyncio  # type: ignore
async def test_guia_not_found_returns_404() -> None:
    """Verifica que una guía inexistente retorne 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/guias/guia-inexistente-12345")
        assert response.status_code == 404


def test_data_service_guias() -> None:
    """Verifica que DataService cargue y parse correctamente las guías."""
    service = DataService()
    guias = service.get_guias()
    assert len(guias) >= 3

    slugs = [g.slug for g in guias]
    assert "enre-544-2024-evitar-cortes-cos-phi" in slugs
    assert "guia-calculo-potencia-contratada-t2-t3" in slugs
    assert "como-digitalizar-maquinas-modbus-gateway-iot" in slugs

    guia_enre = service.get_guia_por_slug("enre-544-2024-evitar-cortes-cos-phi")
    assert guia_enre is not None
    assert guia_enre.category == "Regulación Eléctrica & Penalidades"
    assert guia_enre.content is not None
    assert "<h2>1. El Nuevo Escenario Regulatorio" in guia_enre.content
