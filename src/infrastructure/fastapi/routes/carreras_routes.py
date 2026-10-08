from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from src.adapters.presenters.content_presenter import present_contenido
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel
from src.infrastructure.fastapi.dependencies import get_contenido, get_cursos_service, templates
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(tags=["carreras"])


@router.get("/carreras")
async def listado_carreras(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    data_svc: DataService = Depends(get_cursos_service),
):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    carreras = data_svc.get_carreras()

    seo: dict[str, Any] = {
        "title": f"Oferta Académica y Tecnicaturas Superiores | {brand_data['brandName']}",
        "description": "Tecnicaturas superiores oficiales, públicas y gratuitas en Tigre. Ciencia de Datos e IA, Mecatrónica, Logística y más. Turno vespertino.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "carreras": carreras,
        "sedes_por_id": data_svc.get_sedes_por_id(),
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="carreras.html", context=context)


@router.get("/carreras/{carrera_slug}")
async def detalle_carrera(
    request: Request,
    carrera_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    data_svc: DataService = Depends(get_cursos_service),
):
    carrera = data_svc.get_carrera_by_slug(carrera_slug)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    seo: dict[str, Any] = {
        "title": f"{carrera.title} | {brand_data['brandName']}",
        "description": carrera.description_short,
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "carrera": carrera,
        "otras_carreras": data_svc.get_otras_carreras(carrera_slug),
        "sedes_por_id": data_svc.get_sedes_por_id(),
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="carrera_detail.html", context=context)


@router.get("/campus")
async def campus(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    data_svc: DataService = Depends(get_cursos_service),
):
    """Pantalla de estructura del campus virtual.

    El módulo todavía no está construido: la vista se alimenta de datos de
    muestra declarados en `data/campus/muestra.yaml` y lleva un aviso
    permanente, además de `noindex`, para que no se confunda con información
    real de ninguna persona.
    """
    presented = present_contenido(contenido)
    brand_data = presented["brand"]

    seo: dict[str, Any] = {
        "title": f"Campus virtual | {brand_data['brandName']}",
        "description": "Estructura del campus virtual del ISFT N° 199.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": presented["content"],
        "campus": data_svc.get_campus_muestra(),
        "seo": seo,
    }
    return templates.TemplateResponse(request=request, name="campus.html", context=context)


@router.get("/inscripciones")
async def inscripciones_alias() -> RedirectResponse:
    return RedirectResponse(url="/carreras#requisitos", status_code=301)
