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
    assert "Instalaciones y Aplicaciones de la Energía" in response.text


@pytest.mark.asyncio
async def test_curso_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-intermedio")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Desarrollo de APIs con FastAPI y Python" in response.text
    assert "Sección A: Fundamentos de Python y Entorno" in response.text
    assert "Cap 1: Entorno de Desarrollo de Python" in response.text
    assert 'content="noindex, nofollow"' in response.text or "noindex, nofollow" in response.text


@pytest.mark.asyncio
async def test_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-intermedio/instalacion-distribucion-python-pyenv")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "1.1 Instalación de una Distribución de Python con pyenv" in response.text
    assert "### 1.1" not in response.text


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
    assert "https://datamaq.com.ar/cursos/instalaciones-aplicaciones-energia" in response.text
    # Cursos académicos para alumnos no se indexan en sitemap
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
    assert "Instalaciones y Aplicaciones de la Energía" in response.text


@pytest.mark.asyncio
async def test_invalid_instructor_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instructor/inexistente")

    assert response.status_code == 404
    assert "Página no encontrada" in response.text


@pytest.mark.asyncio
async def test_energia_course_catalog_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos")

    assert response.status_code == 200
    assert "Instalaciones y Aplicaciones de la Energía" in response.text


@pytest.mark.asyncio
async def test_energia_course_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia")

    assert response.status_code == 200
    assert "Instalaciones y Aplicaciones de la Energía" in response.text
    assert "Sección A: Media Tensión y Conversión de Energía" in response.text
    assert "Líneas de Distribución en 13.2 kV" in response.text


@pytest.mark.asyncio
async def test_energia_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/lineas-13-2kv")

    assert response.status_code == 200
    assert "Características y tipos de líneas de 13.2 kV" in response.text
    assert "Conductores Desnudos" in response.text


@pytest.mark.asyncio
async def test_energia_new_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Puesta a Tierra
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/puesta-a-tierra")
        assert response.status_code == 200
        assert "Diseño de Puesta a Tierra y Seguridad Eléctrica" in response.text
        assert "Tensión de Contacto" in response.text

        # Coordinación y Selectividad
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/coordinacion-selectividad")
        assert response.status_code == 200
        assert "Coordinación de Protecciones y Selectividad" in response.text
        assert "ANSI 50" in response.text

        # Ensayos y Mantenimiento
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/ensayos-mantenimiento")
        assert response.status_code == 200
        assert "Ensayos de Campo y Mantenimiento Predictivo" in response.text
        assert "DGA" in response.text

        # Calidad de Energía
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/calidad-energia")
        assert response.status_code == 200
        assert "Calidad de Energía y Compensación de Reactiva" in response.text
        assert "THD-I" in response.text

        # Sistemas de Gestión de Energía
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/sistemas-gestion-energia-iot")
        assert response.status_code == 200
        assert "Sistemas de Gestión de Energía (SGE) e IoT" in response.text
        assert "Modbus" in response.text

        # Generación Distribuida
        response = await ac.get("/cursos/instalaciones-aplicaciones-energia/generacion-distribuida")
        assert response.status_code == 200
        assert "Transición Energética y Generación Distribuida" in response.text
        assert "BESS" in response.text


@pytest.mark.asyncio
async def test_curso_detail_includes_image_dimensions():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/fastapi-intermedio")
    assert response.status_code == 200
    assert 'width="1200"' in response.text
    assert 'height="630"' in response.text


@pytest.mark.asyncio
async def test_cursos_pages_do_not_render_footer():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for url in [
            "/cursos",
            "/cursos/fastapi-intermedio",
            "/cursos/fastapi-intermedio/instalacion-distribucion-python-pyenv",
            "/cursos/instructor/agustin-bustos",
        ]:
            response = await ac.get(url)
            assert response.status_code == 200
            assert 'class="c-home-footer"' not in response.text


@pytest.mark.asyncio
async def test_lenguajes_basico_academic_access():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # No aparece en el catálogo público
        catalog_res = await ac.get("/cursos")
        assert "Lenguajes Electrónicos: Nivel Básico" not in catalog_res.text

        # Pero es accesible mediante URL directa para alumnos con noindex
        detail_res = await ac.get("/cursos/lenguajes-electronicos-basico")
        assert detail_res.status_code == 200
        assert "Lenguajes Electrónicos: Nivel Básico" in detail_res.text
        assert "noindex, nofollow" in detail_res.text


@pytest.mark.asyncio
async def test_lenguajes_basico_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/lenguajes-electronicos-basico")

    assert response.status_code == 200
    assert "Lenguajes Electrónicos: Nivel Básico" in response.text
    assert "Sección A: Fundamentos de la Programación" in response.text
    assert "Algoritmos y Pseudo Código" in response.text


@pytest.mark.asyncio
async def test_lenguajes_basico_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/lenguajes-electronicos-basico/algoritmos-pseudocodigo")

    assert response.status_code == 200
    assert "Algoritmos y Pseudo Código" in response.text
    assert "noindex, nofollow" in response.text


@pytest.mark.asyncio
async def test_lenguajes_intermedio_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/lenguajes-electronicos-intermedio")

    assert response.status_code == 200
    assert "Lenguajes Electrónicos: Nivel Intermedio" in response.text
    assert "El Microcontrolador y el ESP32" in response.text
    assert "Comunicación I2C y Pantalla OLED" in response.text


@pytest.mark.asyncio
async def test_lenguajes_intermedio_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/lenguajes-electronicos-intermedio/instalacion-micropython-esp32")

    assert response.status_code == 200
    assert "Instalación de MicroPython en ESP32-WROOM y la consola REPL" in response.text
    assert "REPL" in response.text


@pytest.mark.asyncio
async def test_lenguajes_avanzado_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/lenguajes-electronicos-avanzado")

    assert response.status_code == 200
    assert "Lenguajes Electrónicos: Nivel Avanzado" in response.text
    assert "Arquitectura Limpia y DDD" in response.text
    assert "Construcción del Pac-Man" in response.text


@pytest.mark.asyncio
async def test_lenguajes_avanzado_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/lenguajes-electronicos-avanzado/arquitectura-limpia-regla-dependencia")

    assert response.status_code == 200
    assert "Arquitectura limpia que grita: capas y regla de dependencia" in response.text
    assert "regla de dependencia" in response.text


@pytest.mark.asyncio
async def test_lenguajes_ddd_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/lenguajes-electronicos-avanzado/ddd-modelado-dominio-pacman")

    assert response.status_code == 200
    assert "Modelado del dominio con DDD" in response.text
    assert "Entidad" in response.text


@pytest.mark.asyncio
async def test_sitemap_excludes_lenguajes_courses():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "https://datamaq.com.ar/cursos/lenguajes-electronicos-basico" not in response.text
    assert "https://datamaq.com.ar/cursos/lenguajes-electronicos-intermedio" not in response.text
    assert "https://datamaq.com.ar/cursos/lenguajes-electronicos-avanzado" not in response.text


@pytest.mark.asyncio
async def test_laboratorio_so_academic_access():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # No aparece en el catálogo público
        catalog_res = await ac.get("/cursos")
        assert "Laboratorio de Sistemas Operativos: Nivel Inicial" not in catalog_res.text

        # Pero es accesible mediante URL directa para alumnos
        detail_res = await ac.get("/cursos/laboratorio-sistemas-operativos-inicial")
        assert detail_res.status_code == 200
        assert "Laboratorio de Sistemas Operativos: Nivel Inicial" in detail_res.text
        assert "noindex, nofollow" in detail_res.text


@pytest.mark.asyncio
async def test_laboratorio_so_inicial_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/laboratorio-sistemas-operativos-inicial")

    assert response.status_code == 200
    assert "Laboratorio de Sistemas Operativos: Nivel Inicial" in response.text
    assert "Sección A: Concepto de Sistema Operativo" in response.text
    assert "Sección C: Terminal, Archivos y Arranque" in response.text


@pytest.mark.asyncio
async def test_laboratorio_so_inicial_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/laboratorio-sistemas-operativos-inicial/funciones-estructura-so")

    assert response.status_code == 200
    assert "Funciones y estructura de un sistema operativo" in response.text
    assert "Micro-desafío práctico" in response.text


@pytest.mark.asyncio
async def test_laboratorio_so_intermedio_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/laboratorio-sistemas-operativos-intermedio")

    assert response.status_code == 200
    assert "Laboratorio de Sistemas Operativos: Nivel Intermedio" in response.text
    assert "Sección B: Memoria y Procesos" in response.text
    assert "Sección C: Impresión, Tipografías y Panel de Control" in response.text


@pytest.mark.asyncio
async def test_laboratorio_so_intermedio_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/laboratorio-sistemas-operativos-intermedio/impresion-diferida-spool-cups")

    assert response.status_code == 200
    assert "La impresión diferida al procesamiento y el spool (CUPS)" in response.text
    assert "CUPS" in response.text


@pytest.mark.asyncio
async def test_laboratorio_so_avanzado_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/laboratorio-sistemas-operativos-avanzado")

    assert response.status_code == 200
    assert "Laboratorio de Sistemas Operativos: Nivel Avanzado" in response.text
    assert "Sección B: Seguridad" in response.text
    assert "Sección C: Arquitecturas y Sistemas de Archivos" in response.text


@pytest.mark.asyncio
async def test_laboratorio_so_avanzado_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/laboratorio-sistemas-operativos-avanzado/sistemas-abiertos-vs-propietarios")

    assert response.status_code == 200
    assert "Sistemas abiertos vs cerrados/propietarios: características y comparación" in response.text
    assert "Propietario" in response.text


@pytest.mark.asyncio
async def test_sitemap_excludes_laboratorio_so_courses():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert "https://datamaq.com.ar/cursos/laboratorio-sistemas-operativos-inicial" not in response.text
    assert "https://datamaq.com.ar/cursos/laboratorio-sistemas-operativos-intermedio" not in response.text
    assert "https://datamaq.com.ar/cursos/laboratorio-sistemas-operativos-avanzado" not in response.text
