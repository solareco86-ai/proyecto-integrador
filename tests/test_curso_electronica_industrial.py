"""Pruebas RED del curso "Electrónica Industrial: Nivel Inicial".

Validan el contenido de datos (data/core/cursos/electronica-industrial-inicial/)
contra el modelo de dominio existente (CourseModel) y el loader DataService,
sin modificar src/. Siguen el patrón de tests/test_cursos.py y
tests/test_yaml_integrity.py.
"""

import os
from typing import cast

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.data_service import DataService
from src.application.dtos import CourseModel, LessonModel, QuizModel
from src.infrastructure.fastapi.app import app

CURSO_SLUG = "electronica-industrial-inicial"
CURSO_TITLE = "Electrónica Industrial: Nivel Inicial"
CURSO_OG_IMAGE = "/static/media/cursos/og-electronica-industrial-inicial.webp"

SECCIONES_ESPERADAS = [
    "Sección A: Automatización Industrial y Control Lógico",
    "Sección B: Circuitos Electrónicos y Regulación Automática",
    "Sección C: Interpretación de Planos y Robótica",
]

TITULOS_LECCIONES_ESPERADOS = [
    "1.1 ¿Qué es la automatización industrial? Evolución y beneficios",
    "1.2 Niveles de automatización y pirámide CIM",
    "2.1 Sistemas de control: lazo abierto y lazo cerrado",
    "2.2 Lógica cableada vs lógica programada: relés, contactores y PLC",
    "2.3 Arquitectura del PLC y ciclo de scan",
    "2.4 Operadores lógicos y funciones básicas (AND, OR, NOT, temporizadores)",
    "3.1 Análisis funcional-estructural: bloques y funciones en procesos productivos",
    "3.2 Tipos y características: circuitos analógicos, digitales y de potencia",
    "3.3 Sensores, transductores y acondicionamiento de señal",
    "3.4 Actuadores: motores, válvulas y variadores de frecuencia",
    "4.1 Regulación automática: variable de proceso, consigna y perturbación",
    "4.2 Control todo-nada (on-off) y control proporcional",
    "4.3 Acciones integral y derivativa: control PID",
    "4.4 Aplicación de la regulación a la automatización industrial",
    "5.1 Simbología eléctrica y electrónica normalizada (IEC/ANSI)",
    "5.2 Planos de circuitos de mando y fuerza",
    "5.3 Diagramas de bloques, esquemáticos y layout de tableros",
    "6.1 Fundamentos de robótica industrial: tipos y clasificación",
    "6.2 Componentes del robot: actuadores, sensores y controlador",
    "6.3 Aplicaciones de la robótica en procesos productivos",
]


def _data_service() -> DataService:
    return DataService(data_dir="data")


def _curso() -> CourseModel | None:
    return _data_service().get_curso_por_slug(CURSO_SLUG)


def _lecciones(curso: CourseModel) -> list[LessonModel | QuizModel]:
    items: list[LessonModel | QuizModel] = []
    for seccion in curso.sections:
        for chapter in seccion.chapters:
            items.extend(chapter.items)
    return items


def _lessons(curso: CourseModel) -> list[LessonModel]:
    lecciones: list[LessonModel] = []
    for seccion in curso.sections:
        for chapter in seccion.chapters:
            for item in chapter.items:
                if item.type == "lesson":
                    lecciones.append(cast(LessonModel, item))
    return lecciones


# ---------------------------------------------------------------------------
# T1-T8: pruebas unitarias de datos (DataService)
# ---------------------------------------------------------------------------


def test_curso_existe_en_catalogo():
    curso = _curso()
    assert curso is not None, f"No se encontró el curso con slug '{CURSO_SLUG}'"


def test_curso_campos_basicos():
    curso = _curso()
    assert curso is not None
    assert curso.title == CURSO_TITLE
    assert curso.level == "Inicial"
    assert curso.duration == "48 horas de cursada"
    assert curso.price == 0.0
    assert curso.academic_only is True
    assert curso.language == "Español"
    assert curso.instructor.id == "agustin-bustos"


def test_curso_tiene_tres_secciones_correctas():
    curso = _curso()
    assert curso is not None
    titulos = [seccion.title for seccion in curso.sections]
    assert titulos == SECCIONES_ESPERADAS


def test_curso_tiene_veinte_lecciones_y_cero_quizzes():
    curso = _curso()
    assert curso is not None
    items = _lecciones(curso)
    assert len(items) == 20
    assert all(item.type == "lesson" for item in items)


def test_curso_titulos_lecciones_correctos():
    curso = _curso()
    assert curso is not None
    titulos = [item.title for item in _lecciones(curso)]
    assert titulos == TITULOS_LECCIONES_ESPERADOS


def test_curso_lecciones_content_file_existen_y_no_vacios():
    curso = _curso()
    assert curso is not None
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    curso_dir = os.path.join(base, "data", "core", "cursos", CURSO_SLUG, "lecciones")
    for item in _lessons(curso):
        assert item.content_file is not None
        file_path = os.path.join(curso_dir, item.content_file)
        assert os.path.isfile(file_path), f"No existe el archivo de contenido {file_path}"
        with open(file_path, encoding="utf-8") as f:
            contenido = f.read()
        assert len(contenido.strip()) > 0, f"El archivo {file_path} está vacío"


def test_curso_og_image_placeholder():
    curso = _curso()
    assert curso is not None
    assert curso.og_image == CURSO_OG_IMAGE
    assert curso.og_image_width == 1200
    assert curso.og_image_height == 630


def test_curso_slugs_unicos_globales():
    service = _data_service()
    slugs: dict[str, list[str]] = {}
    for c in service.get_cursos():
        for seccion in c.sections:
            for chapter in seccion.chapters:
                for item in chapter.items:
                    slugs.setdefault(item.slug, []).append(c.slug)
    duplicados = {slug: cursos for slug, cursos in slugs.items() if len(cursos) > 1}
    assert duplicados == {}, f"Slugs duplicados entre cursos: {duplicados}"


def test_curso_ids_unicos_globales():
    service = _data_service()
    ids: dict[str, list[str]] = {}
    for c in service.get_cursos():
        for seccion in c.sections:
            for chapter in seccion.chapters:
                for item in chapter.items:
                    ids.setdefault(item.id, []).append(c.slug)
    duplicados = {iid: cursos for iid, cursos in ids.items() if len(cursos) > 1}
    assert duplicados == {}, f"Ids duplicados entre cursos: {duplicados}"


# ---------------------------------------------------------------------------
# T9-T12: pruebas de integración de rutas (HTTP)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_curso_electronica_detail_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/cursos/{CURSO_SLUG}")

    assert response.status_code == 200
    assert CURSO_TITLE in response.text
    assert "Sección A: Automatización Industrial y Control Lógico" in response.text
    assert "Cap 1: Introducción a la Automatización Industrial" in response.text


@pytest.mark.asyncio
async def test_curso_electronica_lesson_rendered():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/cursos/{CURSO_SLUG}/que-es-automatizacion-industrial")

    assert response.status_code == 200
    assert "1.1 ¿Qué es la automatización industrial? Evolución y beneficios" in response.text
    assert "noindex, nofollow" in response.text


@pytest.mark.asyncio
async def test_curso_electronica_academic_access():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        catalog_res = await ac.get("/cursos")
        assert CURSO_TITLE not in catalog_res.text

        detail_res = await ac.get(f"/cursos/{CURSO_SLUG}")
        assert detail_res.status_code == 200
        assert CURSO_TITLE in detail_res.text
        assert "noindex, nofollow" in detail_res.text


@pytest.mark.asyncio
async def test_sitemap_excludes_curso_electronica():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    assert f"https://datamaq.com.ar/cursos/{CURSO_SLUG}" not in response.text
