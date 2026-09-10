import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio  # type: ignore
async def test_llms_txt_endpoint_returns_200() -> None:
    """Verifica que el endpoint /llms.txt retorne 200 OK con texto Markdown válido."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/llms.txt")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    text = response.text
    assert "# ISFT N° 199" in text
    assert "Ciencia de Datos" in text
    assert "DGCyE" in text
    assert "+54 11 5629 7160" in text


@pytest.mark.asyncio  # type: ignore
async def test_llms_full_txt_endpoint_returns_200() -> None:
    """Verifica que el endpoint /llms-full.txt retorne 200 OK con documentación técnica extendida."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/llms-full.txt")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    text = response.text
    assert "Ciencia de Datos e Inteligencia Artificial" in text
    assert "Mecatrónica" in text
    assert "Logística" in text
    assert "Higiene y Seguridad" in text
    assert "Agustín Bustos" in text


@pytest.mark.asyncio  # type: ignore
async def test_robots_txt_allows_ai_bots() -> None:
    """Verifica que robots.txt incluya directivas para agentes de IA."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/robots.txt")

    assert response.status_code == 200
    text = response.text
    assert "User-agent: GPTBot" in text
    assert "User-agent: ClaudeBot" in text
    assert "User-agent: PerplexityBot" in text
    assert "Sitemap: https://isftn199.com.ar/sitemap.xml" in text
