from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_contenido, present_evento
from src.application.dtos import ContenidoModel
from src.application.use_cases.content.get_evento_by_slug import GetEventoBySlugUseCase
from src.application.use_cases.content.list_eventos import ListEventosUseCase
from src.domain.content.repositories import EventoRepository
from src.infrastructure.fastapi.dependencies import get_contenido, get_evento_repository, templates
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.get("")
async def listado_eventos(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    evento_repository: EventoRepository = Depends(get_evento_repository),
):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    # ListEventosUseCase ya delega en el repositorio, que ordena por
    # fecha_evento ASC (criterio ya establecido en el proyecto).
    todos = await ListEventosUseCase(repository=evento_repository).execute()
    eventos = [present_evento(e) for e in todos if e.publicada]

    seo: dict[str, Any] = {
        "title": f"Eventos | {brand_data['brandName']}",
        "description": "Eventos institucionales del ISFT N° 199: actividades académicas, jornadas y actos oficiales.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "eventos": eventos,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="eventos/list.html", context=context)


@router.get("/{slug}")
async def detalle_evento(
    request: Request,
    slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    evento_repository: EventoRepository = Depends(get_evento_repository),
):
    evento = await GetEventoBySlugUseCase(repository=evento_repository).execute(slug)
    if evento is None or not evento.publicada:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    presented_evento = present_evento(evento)

    seo: dict[str, Any] = {
        "title": f"{presented_evento['titulo']} | {brand_data['brandName']}",
        "description": presented_evento["descripcion"][:160],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "evento": presented_evento,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="eventos/detail.html", context=context)
