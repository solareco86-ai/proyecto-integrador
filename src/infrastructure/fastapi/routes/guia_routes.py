from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_contenido, present_guia
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel, GuiasHeroModel
from src.infrastructure.fastapi.dependencies import get_contenido, get_cursos_service, templates
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(prefix="/guias", tags=["guias"])


@router.get("")
async def listado_guias(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    guias_service: DataService = Depends(get_cursos_service),
):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    guias_data = content_data.get("guias") or GuiasHeroModel().model_dump()

    guias = [present_guia(g) for g in guias_service.get_guias()]

    seo: dict[str, Any] = {
        "title": f"{guias_data['title']} | {brand_data['brandName']}",
        "description": guias_data["subtitle"],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "guias_hero": guias_data,
        "guias": guias,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="guias/list.html", context=context)


@router.get("/{guia_slug}")
@router.get("/{guia_slug}.html")
async def detalle_guia(
    request: Request,
    guia_slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    guias_service: DataService = Depends(get_cursos_service),
):
    # Soportar slugs con o sin sufijo .html
    clean_slug = guia_slug.removesuffix(".html")
    guia = guias_service.get_guia_por_slug(clean_slug)
    if not guia:
        raise HTTPException(status_code=404, detail="Guía no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    guias_data = content_data.get("guias") or GuiasHeroModel().model_dump()

    presented_guia = present_guia(guia)

    seo: dict[str, Any] = {
        "title": f"{presented_guia['title']} | {brand_data['brandName']}",
        "description": presented_guia["summary"],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented_guia["og_image"] or presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "guias_hero": guias_data,
        "guia": presented_guia,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="guias/detail.html", context=context)
