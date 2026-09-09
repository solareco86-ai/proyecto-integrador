from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_caso, present_contenido
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel
from src.infrastructure.fastapi.dependencies import get_contenido, get_cursos_service, templates
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(prefix="/casos", tags=["casos"])


@router.get("")
async def listado_casos(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    casos_service: DataService = Depends(get_cursos_service),
):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    cases_data = content_data["cases"]

    casos = [present_caso(c) for c in casos_service.get_casos()]

    seo: dict[str, Any] = {
        "title": f"{cases_data['title']} | {brand_data['brandName']}",
        "description": cases_data["subtitle"],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "cases": cases_data,
        "casos": casos,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="casos/list.html", context=context)


@router.get("/{caso_slug}")
async def detalle_caso(
    request: Request,
    caso_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    casos_service: DataService = Depends(get_cursos_service),
):
    caso = casos_service.get_caso_por_slug(caso_slug)
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    presented_caso = present_caso(caso)

    seo: dict[str, Any] = {
        "title": f"Caso: {presented_caso['title']} | {brand_data['brandName']}",
        "description": presented_caso["summary"],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented_caso["og_image"] or presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "cases": content_data["cases"],
        "caso": presented_caso,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="casos/detail.html", context=context)
