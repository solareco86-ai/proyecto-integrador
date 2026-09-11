from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from src.adapters.presenters.content_presenter import present_contenido, present_noticia
from src.application.dtos import ContenidoModel
from src.application.use_cases.content.get_noticia_by_slug import GetNoticiaBySlugUseCase
from src.application.use_cases.content.list_noticias import ListNoticiasUseCase
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.fastapi.dependencies import get_contenido, get_noticia_repository, templates
from src.infrastructure.fastapi.utils.seo import canonical_url

router = APIRouter(prefix="/noticias", tags=["noticias"])


@router.get("")
async def listado_noticias(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
):
    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    todas = await ListNoticiasUseCase(repository=noticia_repository).execute()
    noticias = [present_noticia(n) for n in todas if n.publicada]

    seo: dict[str, Any] = {
        "title": f"Noticias | {brand_data['brandName']}",
        "description": "Noticias institucionales del ISFT N° 199: novedades académicas, actividades e información oficial.",
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "noticias": noticias,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="noticias/list.html", context=context)


@router.get("/{slug}")
async def detalle_noticia(
    request: Request,
    slug: str,
    contenido: ContenidoModel = Depends(get_contenido),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
):
    noticia = await GetNoticiaBySlugUseCase(repository=noticia_repository).execute(slug)
    if noticia is None or not noticia.publicada:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    presented = present_contenido(contenido)
    brand_data = presented["brand"]
    content_data = presented["content"]

    presented_noticia = present_noticia(noticia)

    seo: dict[str, Any] = {
        "title": f"{presented_noticia['titulo']} | {brand_data['brandName']}",
        "description": presented_noticia["cuerpo"][:160],
        "canonical_url": canonical_url(request.url),
        "site_name": brand_data["brandName"],
        "og_image": presented["seo"]["og_image"],
        "og_image_width": 1200,
        "og_image_height": 630,
    }

    context: dict[str, Any] = {
        "brand": brand_data,
        "content": content_data,
        "noticia": presented_noticia,
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="noticias/detail.html", context=context)
