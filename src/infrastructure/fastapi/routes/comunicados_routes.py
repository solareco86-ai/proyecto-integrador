from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_comunicado, present_contenido
from src.application.dtos import ContenidoModel
from src.application.use_cases.content.get_comunicado_by_slug import GetComunicadoBySlugUseCase
from src.application.use_cases.content.list_comunicados import ListComunicadosUseCase
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.fastapi.dependencies import get_comunicado_repository, get_contenido, templates
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(prefix="/comunicados", tags=["comunicados"])


@router.get("")
async def listado_comunicados(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    todos = await ListComunicadosUseCase(repository=comunicado_repository).execute()
    comunicados = [present_comunicado(c) for c in todos if c.publicada]

    seo: dict[str, Any] = {
        "title": f"Comunicados | {brand_data['brandName']}",
        "description": "Comunicados oficiales del ISFT N° 199: información institucional y avisos oficiales.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "comunicados": comunicados,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="comunicados/list.html", context=context)


@router.get("/{slug}")
async def detalle_comunicado(
    request: Request,
    slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
):
    comunicado = await GetComunicadoBySlugUseCase(repository=comunicado_repository).execute(slug)
    if comunicado is None or not comunicado.publicada:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    presented_comunicado = present_comunicado(comunicado)

    seo: dict[str, Any] = {
        "title": f"{presented_comunicado['titulo']} | {brand_data['brandName']}",
        "description": presented_comunicado["cuerpo"][:160],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "comunicado": presented_comunicado,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="comunicados/detail.html", context=context)
