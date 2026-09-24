import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio
async def test_cursos_catalog_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Aulas y Materiales de Cátedra en Línea" in response.text or "Campus Virtual" in response.text
    assert "Técnicas de Procesamiento Digital de Imágenes" in response.text


@pytest.mark.asyncio
async def test_curso_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-imagenes-python-opencv")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Técnicas de Procesamiento Digital de Imágenes con Python y OpenCV" in response.text
    assert "Sección 0: Preparación del Entorno de Desarrollo" in response.text
    assert "Cap 0: Entorno Virtual y Dependencias" in response.text


@pytest.mark.asyncio
async def test_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-imagenes-python-opencv/entorno-virtual-requirements")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "0.1 Entorno virtual (.venv) y gestión de dependencias con requirements.txt" in response.text
    assert "### 0.1" not in response.text


@pytest.mark.asyncio
async def test_invalid_course_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/curso-inexistente")

    assert response.status_code == 404
    assert "Página no encontrada" in response.text


@pytest.mark.asyncio
async def test_invalid_lesson_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-intermedio/leccion-inexistente")

    assert response.status_code == 404
    assert "Página no encontrada" in response.text


@pytest.mark.asyncio
async def test_sitemap_includes_courses():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "https://datamaq.com.ar/cursos" in response.text
    assert "https://datamaq.com.ar/cursos/procesamiento-imagenes-python-opencv" in response.text
    # Cursos académicos para alumnos no se indexan en sitemap
    assert "https://datamaq.com.ar/cursos/instalaciones-aplicaciones-energia" not in response.text
    assert "https://datamaq.com.ar/cursos/fastapi-intermedio" not in response.text
    assert "https://datamaq.com.ar/cursos/fastapi-avanzado" not in response.text


@pytest.mark.asyncio
async def test_default_instructor_redirects():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instructor", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/cursos/instructor/agustin-bustos"


@pytest.mark.asyncio
async def test_instructor_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instructor/agustin-bustos")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Agustin Bustos" in response.text
    assert "Ciencia de Datos" in response.text
    assert "Técnicas de Procesamiento Digital de Imágenes" in response.text


@pytest.mark.asyncio
async def test_invalid_instructor_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instructor/inexistente")

    assert response.status_code == 404
    assert "Página no encontrada" in response.text


@pytest.mark.asyncio
async def test_curso_detail_includes_image_dimensions():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-imagenes-python-opencv")
    assert response.status_code == 200
    assert 'width="1200"' in response.text
    assert 'height="630"' in response.text


@pytest.mark.asyncio
async def test_cursos_pages_do_not_render_footer():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for url in [
            "/cursos",
            "/cursos/procesamiento-imagenes-python-opencv",
            "/cursos/procesamiento-imagenes-python-opencv/entorno-virtual-requirements",
            "/cursos/instructor/agustin-bustos",
        ]:
            response = await ac.get(url)
            assert response.status_code == 200
            assert 'class="c-home-footer"' not in response.text
