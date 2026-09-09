from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from src.adapters.presenters.content_presenter import present_contenido, present_course
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel, LessonModel, QuizModel
from src.infrastructure.fastapi.dependencies import get_contenido, get_cursos_service, templates
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(prefix="/cursos", tags=["cursos"])


@router.get("")
async def listado_cursos(
    request: Request,
    view: str | None = None,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    courses_data = content_data["courses"]

    mostrar_todos = view == "all"
    cursos_fuente = cursos_service.get_cursos() if mostrar_todos else cursos_service.get_cursos_publicos()
    cursos = [present_course(c) for c in cursos_fuente]

    seo: dict[str, Any] = {
        "title": f"{courses_data['title']} | {brand_data['brandName']}",
        "description": courses_data["subtitle"],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    if mostrar_todos:
        seo["meta_robots"] = "noindex, nofollow"

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "courses": courses_data,
        "cursos": cursos,
        "mostrando_todos": mostrar_todos,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="cursos/list.html", context=context)


@router.get("/instructor")
@router.get("/instructor/")
async def redireccionar_instructor_por_defecto(cursos_service: DataService = Depends(get_cursos_service)):
    instructores = list(cursos_service.get_instructores_dict().values())
    if not instructores:
        raise HTTPException(status_code=404, detail="No se encontraron instructores")
    default_id = instructores[0].id
    return RedirectResponse(url=f"/cursos/instructor/{default_id}", status_code=307)


@router.get("/instructor/{instructor_id}")
async def detalle_instructor(
    request: Request,
    instructor_id: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    instructor = cursos_service.get_instructor_por_id(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    cursos = [present_course(c) for c in cursos_service.get_cursos_publicos() if c.instructor.id == instructor_id]

    seo: dict[str, Any] = {
        "title": f"Instructor: {instructor.name} | DataMaq",
        "description": instructor.bio[:150],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": instructor.photo,
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "courses": content_data["courses"],
        "instructor": instructor.model_dump(),
        "cursos": cursos,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="cursos/instructor.html", context=context)


@router.get("/{curso_slug}")
async def detalle_curso(
    request: Request,
    curso_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    curso = cursos_service.get_curso_por_slug(curso_slug)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    presented_c = present_course(curso)

    seo: dict[str, Any] = {
        "title": f"Curso: {presented_c['title']} | DataMaq",
        "description": presented_c["description_short"],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented_c["og_image"] or presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    if curso.academic_only:
        seo["meta_robots"] = "noindex, nofollow"

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "courses": content_data["courses"],
        "curso": presented_c,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="cursos/detail.html", context=context)


@router.get("/{curso_slug}/{leccion_slug}")
async def vista_leccion(
    request: Request,
    curso_slug: str,
    leccion_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    resultado = cursos_service.get_leccion(curso_slug, leccion_slug)
    if not resultado:
        raise HTTPException(status_code=404, detail="Lección o curso no encontrado")

    curso, leccion = resultado
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    presented_c = present_course(curso)

    meta_robots = "noindex, nofollow" if curso.academic_only else "noindex, follow"
    seo: dict[str, Any] = {
        "title": f"{leccion.title} - Curso: {presented_c['title']} | DataMaq",
        "description": f"Lección sobre {leccion.title} en el curso {presented_c['title']}. Cursado gratuito en DataMaq.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented_c["og_image"] or presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
        "meta_robots": meta_robots,
    }

    # Determinamos lección anterior y siguiente para facilitar la navegación fluida
    prev_lesson = None
    next_lesson = None
    all_lessons: list[LessonModel | QuizModel] = []

    for section in curso.sections:
        for chapter in section.chapters:
            for item in chapter.items:
                all_lessons.append(item)

    for i, item in enumerate(all_lessons):
        if item.id == leccion.id:
            if i > 0:
                prev_lesson = all_lessons[i - 1]
            if i < len(all_lessons) - 1:
                next_lesson = all_lessons[i + 1]
            break

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "courses": content_data["courses"],
        "curso": presented_c,
        "leccion": leccion.model_dump(),
        "prev_lesson": prev_lesson.model_dump() if prev_lesson else None,
        "next_lesson": next_lesson.model_dump() if next_lesson else None,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="cursos/lesson.html", context=context)
