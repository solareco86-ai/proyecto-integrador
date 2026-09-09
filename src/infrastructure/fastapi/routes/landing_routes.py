from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from src.adapters.presenters.content_presenter import present_contenido
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel, LandingCampaignModel
from src.infrastructure.fastapi.dependencies import (
    get_contenido,
    get_cursos_service,
    templates,
)
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(prefix="/landing", tags=["Landings"])


@router.get("/calidad-energia")
async def landing_calidad_energia(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    campaign: LandingCampaignModel | None = cursos_service.get_landing_campaign("calidad-energia")
    if not campaign:
        raise HTTPException(status_code=404, detail="Landing de Calidad de Energía no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]

    seo: dict[str, Any] = {
        "title": f"{campaign.hero_title} | {brand_data['brandName']}",
        "description": campaign.hero_subtitle,
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
        "campaign": campaign.model_dump(),
        "casos": cursos_service.get_casos(),
        "cursos": cursos_service.get_cursos(),
    }
    return templates.TemplateResponse(request=request, name="landings/calidad_energia.html", context=context)


@router.get("/calidad-energia.html")
async def landing_calidad_energia_alias() -> RedirectResponse:
    return RedirectResponse(url="/landing/calidad-energia", status_code=301)


@router.get("/telemetria-industrial")
async def landing_telemetria_industrial(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    campaign: LandingCampaignModel | None = cursos_service.get_landing_campaign("telemetria-industrial")
    if not campaign:
        raise HTTPException(status_code=404, detail="Landing de Telemetría Industrial no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]

    seo: dict[str, Any] = {
        "title": f"{campaign.hero_title} | {brand_data['brandName']}",
        "description": campaign.hero_subtitle,
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
        "campaign": campaign.model_dump(),
        "casos": cursos_service.get_casos(),
        "cursos": cursos_service.get_cursos(),
    }
    return templates.TemplateResponse(request=request, name="landings/telemetria_industrial.html", context=context)


@router.get("/telemetria-industrial.html")
async def landing_telemetria_industrial_alias() -> RedirectResponse:
    return RedirectResponse(url="/landing/telemetria-industrial", status_code=301)
