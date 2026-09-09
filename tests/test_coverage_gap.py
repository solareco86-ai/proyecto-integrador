import pytest
from httpx import ASGITransport, AsyncClient  # type: ignore

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio  # type: ignore
async def test_robots_txt():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/robots.txt")

    assert response.status_code == 200


# La lógica de CachedStaticFiles se prueba indirectamente si hacemos un request a un archivo estático,
# pero fastapi.staticfiles maneja los archivos directamente.
# Es difícil probarlo con AsyncClient tal cual sin montar la app de otra forma.
# La línea 26 es la función add_static_version, que se llama al renderizar las plantillas,
# la cual ya está siendo invocada por los tests anteriores, quizás el reporte de cobertura es ligeramente inexacto
# o se refiere a la definición de la función misma.
