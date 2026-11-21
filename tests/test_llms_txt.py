import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
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
    assert "datamaq.com.ar" not in text


@pytest.mark.asyncio  # type: ignore
@pytest.mark.parametrize("path", ["/llms.txt", "/llms-full.txt"])  # type: ignore
async def test_llms_files_match_official_data(path: str) -> None:
    """Las resoluciones citadas coinciden con carreras.yaml y no queda contenido heredado.

    No compara nombres de carreras: la sexta tiene una denominación distinta entre
    carreras.yaml y los llms hasta que se confirme la oficial.
    """
    carreras = DataService(data_dir="data").get_carreras()
    resoluciones: list[str] = [
        c.resolucion.removeprefix("Resolución ") for c in carreras if c.resolucion is not None
    ]
    assert len(resoluciones) == 6, "carreras.yaml debe declarar la resolución de las 6 carreras"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(path)

    assert response.status_code == 200
    text: str = response.text
    for resolucion in resoluciones:
        assert resolucion in text, f"{path} no cita {resolucion}"

    texto_minusculas: str = text.lower()
    for heredado in ("datamaq", "powermeter", "xubio", "enre 544"):
        assert heredado not in texto_minusculas, f"{path} conserva contenido heredado: {heredado!r}"


@pytest.mark.asyncio  # type: ignore
async def test_llms_full_lists_official_subjects_and_job_profiles() -> None:
    """llms-full.txt reproduce textualmente las materias y la salida laboral de carreras.yaml."""
    carreras = DataService(data_dir="data").get_carreras()
    esperados: list[str] = [item for c in carreras for item in (*c.materias_destacadas, *c.salida_laboral)]
    assert len(esperados) > 0, "carreras.yaml no declara materias ni salida laboral"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/llms-full.txt")

    assert response.status_code == 200
    faltantes: list[str] = [item for item in esperados if item not in response.text]
    assert faltantes == [], f"llms-full.txt no refleja carreras.yaml: {faltantes}"
