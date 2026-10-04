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
async def test_aprendizaje_automatico_cap3_estudiantes_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 3.1 Modelos de Costo
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-modelos-costos-suscripcion-vs-api")
        assert r1.status_code == 200
        assert "3.1 Economía de la IA Agéntica" in r1.text

        # 3.2 OpenCode Proveedores
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-opencode-instalacion-proveedores")
        assert r2.status_code == 200
        assert "3.2 OpenCode" in r2.text
        assert "Proveedores Gratuitos" in r2.text

        # 3.3 OpenCode Laboratorio
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-opencode-laboratorio-energy-ml")
        assert r3.status_code == 200
        assert "3.3 Taller Práctico con OpenCode" in r3.text
        assert "energy-ml" in r3.text

        # 3.4 Antigravity CLI Setup
        r4 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-antigravity-cli-setup-estudiantes")
        assert r4.status_code == 200
        assert "3.4 Antigravity CLI" in r4.text
        assert "5 USD" in r4.text

        # 3.5 Antigravity CLI Navegador
        r5 = await ac.get(
            "/cursos/procesamiento-aprendizaje-automatico/paa-ini-antigravity-cli-navegador-pair-programming"
        )
        assert r5.status_code == 200
        assert "3.5 AGY CLI en Acción" in r5.text
        assert "/browser" in r5.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_cap4_avanzado_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 4.1 Claude Code
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-claude-code-entorno-corporativo")
        assert r1.status_code == 200
        assert "4.1 Claude Code" in r1.text
        assert "corporativo" in r1.text

        # 4.2 Aider Repomap
        r2 = await ac.get(
            "/cursos/procesamiento-aprendizaje-automatico/paa-ini-aider-deepseek-api-arquitectura-interna"
        )
        assert r2.status_code == 200
        assert "4.2 Aider con DeepSeek API" in r2.text
        assert "Repomap" in r2.text

        # 4.3 Aider Optimización y Descuento Horario
        r3 = await ac.get(
            "/cursos/procesamiento-aprendizaje-automatico/paa-ini-aider-optimizacion-costos-descuento-horario"
        )
        assert r3.status_code == 200
        assert "4.3 Optimización y Cautela Financiera en Aider" in r3.text
        assert "2 USD" in r3.text

        # 4.4 Arneses (Codex, Kimi, DPH)
        r4 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-arneses-ia-codex-kimi-dph")
        assert r4.status_code == 200
        assert "4.4 Panorama de Arneses de IA Agéntica" in r4.text
        assert "DPH" in r4.text


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


@pytest.mark.asyncio
async def test_aprendizaje_automatico_cap5_fastapi_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 5.1 Fundamentos HTTP y JSON
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-fundamentos-http-json")
        assert r1.status_code == 200
        assert "5.1 Protocolo HTTP" in r1.text
        assert "energy-ml" in r1.text

        # 5.2 Primer servidor FastAPI
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-primer-servidor-fastapi")
        assert r2.status_code == 200
        assert "5.2 Servidor FastAPI" in r2.text
        assert "Swagger UI" in r2.text

        # 5.3 Endpoint con Pydantic y OpenCode
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-endpoint-calculo-opencode")
        assert r3.status_code == 200
        assert "5.3 Endpoint POST" in r3.text
        assert "Pydantic" in r3.text

        # 5.4 De if/else a Machine Learning
        r4 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ini-reglas-manuales-vs-datos")
        assert r4.status_code == 200
        assert "5.4 Del if/else de Firmas Eléctricas" in r4.text
        assert "Machine Learning" in r4.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit2_cap0_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 0.1 NumPy y Tensores
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-numpy-vectores-telemetria")
        assert r1.status_code == 200
        assert "Álgebra Matricial Intuitiva" in r1.text
        assert "NumPy" in r1.text
        assert "energy-ml" in r1.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit2_cap1_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1.1 Pydantic y Features
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-pydantic-esquemas-ml")
        assert r1.status_code == 200
        assert "Modelado de features con Pydantic" in r1.text
        assert "energy-ml" in r1.text

        # 1.2 Lifespan y Memoria
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-fastapi-lifespan-modelos")
        assert r2.status_code == 200
        assert "Gestión de memoria en FastAPI" in r2.text
        assert "lifespan" in r2.text

        # 1.3 Joblib y Persistencia
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-serializacion-joblib")
        assert r3.status_code == 200
        assert "Serialización y persistencia" in r3.text
        assert "joblib" in r3.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit2_cap2_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 2.1 Deducción vs. Inducción
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-deduccion-vs-induccion")
        assert r1.status_code == 200
        assert "Razonamiento deductivo del LLM" in r1.text
        assert "energy-ml" in r1.text

        # 2.2 Subtareas del aprendizaje y Data Leakage
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-subtareas-del-aprendizaje")
        assert r2.status_code == 200
        assert "Subtareas del aprendizaje" in r2.text
        assert "data leakage" in r2.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit2_cap3_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 3.1 Teorema de Bayes
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-teorema-bayes-clasificacion")
        assert r1.status_code == 200
        assert "Teorema de Bayes" in r1.text
        assert "energy-ml" in r1.text

        # 3.2 Endpoint Naive Bayes con OpenCode
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-endpoint-naive-bayes-opencode")
        assert r2.status_code == 200
        assert "POST /api/v1/classify/bayes" in r2.text
        assert "OpenCode" in r2.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit2_cap4_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 4.1 Algoritmo k-NN
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-knn-distancias-normalizacion")
        assert r1.status_code == 200
        assert "Algoritmo k-NN" in r1.text
        assert "energy-ml" in r1.text

        # 4.2 Endpoint k-NN en FastAPI
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-endpoint-knn-fastapi")
        assert r2.status_code == 200
        assert "POST /api/v1/classify/knn" in r2.text
        assert "FastAPI" in r2.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit2_cap5_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 5.1 Matriz de confusión y F1
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-metricas-confusion-f1")
        assert r1.status_code == 200
        assert "Matriz de confusión" in r1.text
        assert "energy-ml" in r1.text

        # 5.2 Flujo TDD con Aider y AGY CLI
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-tdd-pytest-aider-agy")
        assert r2.status_code == 200
        assert "Flujo TDD en FastAPI" in r2.text
        assert "Aider" in r2.text

        # 5.3 Endpoint GET /metrics
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-int-endpoint-metricas-observabilidad")
        assert r3.status_code == 200
        assert "GET /api/v1/metrics" in r3.text
        assert "Observabilidad" in r3.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit3_cap1_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1.1 Candidate-Elimination
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-espacio-versiones-ce")
        assert r1.status_code == 200
        assert "Candidate-Elimination" in r1.text
        assert "energy-ml" in r1.text

        # 1.2 Endpoint version-space/step
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-endpoint-version-space-step")
        assert r2.status_code == 200
        assert "POST /api/v1/version-space/step" in r2.text
        assert "VersionSpaceLearner" in r2.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit3_cap2_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 2.1 Algoritmo AQ y cobertura secuencial
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-algoritmo-aq-cobertura")
        assert r1.status_code == 200
        assert "Algoritmo AQ" in r1.text
        assert "Separate-and-Conquer" in r1.text

        # 2.2 FOIL
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-programacion-logica-inductiva-foil")
        assert r2.status_code == 200
        assert "FOIL" in r2.text
        assert "cláusulas de Horn" in r2.text

        # 2.3 Endpoint GET /rules
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-endpoint-rules-auditoria")
        assert r3.status_code == 200
        assert "GET /api/v1/rules" in r3.text
        assert "ReglaOperativaDTO" in r3.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit3_cap3_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 3.1 Entropía y Gini
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-entropia-ganancia-gini")
        assert r1.status_code == 200
        assert "Impureza de Gini" in r1.text
        assert "Entropía de Shannon" in r1.text

        # 3.2 Árboles de regresión
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-arboles-regresion-continuos")
        assert r2.status_code == 200
        assert "Árboles de Regresión" in r2.text
        assert "ccp_alpha" in r2.text

        # 3.3 Exportación JSON
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-exportacion-arbol-json")
        assert r3.status_code == 200
        assert "GET /api/v1/explain/tree" in r3.text
        assert "NodoArbolDTO" in r3.text


@pytest.mark.asyncio
async def test_aprendizaje_automatico_unit3_cap4_lessons_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 4.1 AST y Poda de Contexto
        r1 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-ast-poda-contexto-agentes")
        assert r1.status_code == 200
        assert "Árboles de Sintaxis Abstracta (AST)" in r1.text
        assert "ASTContextPruner" in r1.text

        # 4.2 Servidor MCP en FastAPI
        r2 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-servidor-mcp-fastapi")
        assert r2.status_code == 200
        assert "Model Context Protocol" in r2.text
        assert "tools/list" in r2.text

        # 4.3 Taller Integrador Final
        r3 = await ac.get("/cursos/procesamiento-aprendizaje-automatico/paa-ava-proyecto-integrador-agentes")
        assert r3.status_code == 200
        assert "Taller Integrador" in r3.text
        assert "ISFT N° 199" in r3.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "slug",
    [
        # Lecciones originales (Unidad 2)
        "paa-int-subtareas-del-aprendizaje",
        "paa-int-knn-distancias-normalizacion",
        "paa-int-numpy-vectores-telemetria",
        # Lecciones nuevas Unidad 2
        "paa-int-pydantic-esquemas-ml",
        "paa-int-fastapi-lifespan-modelos",
        "paa-int-serializacion-joblib",
        "paa-int-teorema-bayes-clasificacion",
        "paa-int-endpoint-naive-bayes-opencode",
        "paa-int-endpoint-knn-fastapi",
        "paa-int-metricas-confusion-f1",
        "paa-int-tdd-pytest-aider-agy",
        "paa-int-endpoint-metricas-observabilidad",
        # Lecciones originales (Unidad 3)
        "paa-ava-espacio-versiones-ce",
        "paa-ava-arboles-regresion-continuos",
        # Lecciones nuevas Unidad 3
        "paa-ava-endpoint-version-space-step",
        "paa-ava-algoritmo-aq-cobertura",
        "paa-ava-programacion-logica-inductiva-foil",
        "paa-ava-endpoint-rules-auditoria",
        "paa-ava-exportacion-arbol-json",
        "paa-ava-servidor-mcp-fastapi",
        "paa-ava-proyecto-integrador-agentes",
    ],
)
async def test_aprendizaje_automatico_lecciones_con_caza_de_alucinaciones(slug: str):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.get(f"/cursos/procesamiento-aprendizaje-automatico/{slug}")
        assert r.status_code == 200
        assert "Autoevaluación Formativa" in r.text
        assert "Caza de Código Alucinado" in r.text
