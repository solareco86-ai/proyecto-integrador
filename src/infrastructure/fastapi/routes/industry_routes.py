from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_contenido
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel, IndustriaModel, LandingContentModel
from src.infrastructure.fastapi.dependencies import (
    get_contenido,
    get_cursos_service,
    get_industrias,
    get_landing_content,
    templates,
)
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter()


@router.get("/industria/{industria}.html")
async def pagina_industria(
    request: Request,
    industria: str,
    contenido: ContenidoModel = Depends(get_contenido),
    industrias_data: IndustriaModel = Depends(get_industrias),
    landing_content: LandingContentModel = Depends(get_landing_content),
    cursos_service: DataService = Depends(get_cursos_service),
):

    nombre_industria = industrias_data.industrias.get(industria)

    if not nombre_industria:
        raise HTTPException(status_code=404, detail="Industria no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]
    servicios_data = content_data["services"]["cards"]

    industria_content = landing_content.industrias.get(industria)

    seo: dict[str, Any] = {
        "title": f"Telemetría y calidad de energía para {nombre_industria} | {brand_data['brandName']}",
        "description": f"Monitoreo IoT en tiempo real, corrección de factor de potencia (ENRE 544/2024) y optimización de potencia contratada T2/T3 aplicados a la {nombre_industria}. Visitas técnicas en campo.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    hero_title = f"Telemetría y calidad de energía para {nombre_industria}"
    hero_subtitle = f"Monitoreo IoT en tiempo real, corrección de factor de potencia bajo la Res. ENRE 544/2024 y optimización de potencia contratada T2/T3 aplicados a la {nombre_industria}."

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "servicios": servicios_data,
        "faq": content_data["faq"]["questions"],
        "industria_nombre": nombre_industria,
        "seo": seo,
        "footer": presented.get("footer"),
        "hero_title": hero_title,
        "hero_subtitle": hero_subtitle,
        "landing_industria": industria_content.model_dump() if industria_content else None,
        "casos": cursos_service.get_casos(),
        "guias": cursos_service.get_guias(),
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)
