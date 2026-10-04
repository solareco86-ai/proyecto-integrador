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
async def test_aprendizaje_automatico_entorno_os_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-entorno-os-gitbash-wsl-linux")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "1.1 El sistema operativo y la consola: GNU/Linux, WSL y Git Bash" in response.text
    assert "Git Bash" in response.text
    assert "WSL 2" in response.text
    assert "GNU/Linux" in response.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_git_clone_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-git-clone-proyecto-energy-ml")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "1.3 Control de versiones con Git, identidad y clonado del proyecto base" in response.text
    assert "energy-ml" in response.text
    assert "git clone https://github.com/datamaq-automation/energy-ml" in response.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_restore_reset_revert_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-git-restore-reset-revert")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "2.4 Marcha atrás y control de daños" in response.text
    assert "git restore" in response.text
    assert "git reset" in response.text
    assert "git revert" in response.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_github_cli_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-github-cli-gh-agentes-ia")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "2.5 GitHub CLI (gh)" in response.text
    assert "gh pr create" in response.text
    assert "gh issue" in response.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_cap3_cuarteto_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 3.1 Modelos de Costo
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-modelos-costos-suscripcion-vs-api")
        assert r1.status_code == 200
        assert "3.1 Economía de la IA Agéntica" in r1.text
        assert "DeepSeek" in r1.text

        # 3.2 OpenCode
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-opencode-agente-opensource")
        assert r2.status_code == 200
        assert "3.2 OpenCode" in r2.text
        assert "Open Source" in r2.text

        # 3.3 Antigravity CLI
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-antigravity-cli-setup-navegador")
        assert r3.status_code == 200
        assert "3.3 Antigravity CLI" in r3.text
        assert "5 USD" in r3.text
        assert "/browser" in r3.text

        # 3.4 Claude Code
        r4 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-claude-code-entorno-corporativo")
        assert r4.status_code == 200
        assert "3.4 Claude Code" in r4.text
        assert "corporativo" in r4.text

        # 3.5 Aider
        r5 = await ac.get(
            "/cursos/procesamiento-aprendizaje-automatico/paa-ini-aider-deepseek-api-arquitectura-interna"
        )
        assert r5.status_code == 200
        assert "3.5 Aider con DeepSeek API" in r5.text
        assert "2 USD" in r5.text

        # 3.6 Arneses (Codex, Kimi, DPH)
        r6 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-arneses-ia-codex-kimi-dph")
        assert r6.status_code == 200
        assert "3.6 Ecosistema de Arneses de IA Agéntica" in r6.text
        assert "Kimi Code" in r6.text
        assert "DPH" in r6.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_debate_audio_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-debate-terminal-o-agentes-ia")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "0.1 Debate Dialéctico: ¿Terminal manual o agentes de IA?" in response.text
    assert "c-lesson-audio-card" in response.text
    assert "/static/media/cursos/terminal-manual-o-agentes-ia.m4a" in response.text
    assert "<audio controls" in response.text


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
