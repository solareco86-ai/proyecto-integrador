import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response
from sqlalchemy.exc import OperationalError

from src.adapters.presenters.content_presenter import present_contenido
from src.application.data_service import DataService
from src.application.dtos import ContenidoModel, IndustriaModel
from src.application.use_cases.content.list_comunicados import ListComunicadosUseCase
from src.application.use_cases.content.list_eventos import ListEventosUseCase
from src.application.use_cases.content.list_noticias import ListNoticiasUseCase
from src.domain.content.repositories import ComunicadoRepository, EventoRepository, NoticiaRepository
from src.infrastructure.fastapi.dependencies import (
    get_comunicado_repository,
    get_contenido,
    get_cursos_service,
    get_evento_repository,
    get_geografia,
    get_industrias,
    get_noticia_repository,
    templates,
)
from src.infrastructure.fastapi.metrics import registry
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.infrastructure.settings import config

logger = logging.getLogger(config.LOGGER_NAME)

router = APIRouter()

# --- Health Endpoints ---


@router.get("/healthz")
async def healthz():
    """Liveness probe: la app responde."""
    return {"status": "ok"}


@router.get("/metrics")
async def metrics() -> Response:
    """Expone métricas operativas en formato Prometheus text exposition."""
    return Response(content=registry.render(), media_type="text/plain; version=0.0.4; charset=utf-8")


@router.get("/ready")
async def ready() -> JSONResponse:
    """Readiness probe: verifica que la DB de leads sea accesible."""
    from src.infrastructure.fastapi.dependencies import get_lead_repository

    try:
        repo = get_lead_repository()
        db_healthy = await repo.is_healthy()
        if db_healthy:
            return JSONResponse(
                status_code=200,
                content={"status": "ok", "checks": {"db_accessible": True}},
            )
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "checks": {"db_accessible": False}},
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "checks": {"db_accessible": False, "error": str(e)}},
        )


def _content_lastmod() -> str:
    """
    Devuelve la fecha de modificación más reciente de los archivos de datos
    de contenido (YAML/Markdown) para usar como lastmod del sitemap.
    Si no se encuentran archivos, retorna la fecha actual.
    """
    data_dir = Path("data")
    latest_mtime: float = 0.0
    if data_dir.exists():
        for path in data_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in (".yaml", ".yml", ".md"):
                mtime = path.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime
    if latest_mtime:
        return datetime.fromtimestamp(latest_mtime).strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d")


@router.get("/robots.txt")
async def robots():
    return FileResponse(config.ROBOTS_TXT_PATH)


@router.get("/humans.txt")
async def humans():
    return FileResponse(config.HUMANS_TXT_PATH, media_type="text/plain")


@router.get("/llms.txt")
async def llms_txt():
    return FileResponse(config.LLMS_TXT_PATH, media_type="text/plain; charset=utf-8")


@router.get("/llms-full.txt")
async def llms_full_txt():
    return FileResponse(config.LLMS_FULL_TXT_PATH, media_type="text/plain; charset=utf-8")


@router.get("/google1be4ebe73ffd0291.html")
async def google_verification():
    return FileResponse("static/google1be4ebe73ffd0291.html")


@router.post("/csp-report", status_code=204)
async def csp_report_endpoint(request: Request) -> Response:
    """Endpoint receptor de reportes de violación de Content-Security-Policy."""
    body = await request.body()
    report = body.decode("utf-8", errors="replace")
    logger.warning("Violación CSP reportada: %s", report[:4096])
    return Response(status_code=204)


@router.get("/sitemap.xml")
async def sitemap(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    geografia: dict[str, Any] = Depends(get_geografia),
    industrias_data: IndustriaModel = Depends(get_industrias),
    cursos_service: DataService = Depends(get_cursos_service),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
    evento_repository: EventoRepository = Depends(get_evento_repository),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
):
    base_url = config.BASE_URL.rstrip("/")
    lastmod = _content_lastmod()

    urls = [
        {"loc": f"{base_url}/", "lastmod": lastmod, "changefreq": "monthly", "priority": "1.0"},
        {"loc": f"{base_url}/landing/calidad-energia", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.9"},
        {
            "loc": f"{base_url}/landing/telemetria-industrial",
            "lastmod": lastmod,
            "changefreq": "monthly",
            "priority": "0.9",
        },
        {"loc": f"{base_url}/contact", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.6"},
        {"loc": f"{base_url}/terminos-y-condiciones", "lastmod": lastmod, "changefreq": "yearly", "priority": "0.3"},
        {"loc": f"{base_url}/carreras", "lastmod": lastmod, "changefreq": "weekly", "priority": "0.9"},
        {"loc": f"{base_url}/cursos", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{base_url}/casos", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.7"},
        {"loc": f"{base_url}/guias", "lastmod": lastmod, "changefreq": "monthly", "priority": "0.7"},
    ]

    localidades = geografia.get("localidades", {})
    for provincia_key, provincia in localidades.items():
        # Página hub de provincia
        urls.append(
            {
                "loc": f"{base_url}/{provincia_key}",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.6",
            }
        )
        for municipio_key, municipio in provincia.items():
            # Página hub de municipio
            urls.append(
                {
                    "loc": f"{base_url}/{provincia_key}/{municipio_key}",
                    "lastmod": lastmod,
                    "changefreq": "monthly",
                    "priority": "0.6",
                }
            )
            for localidad_key in municipio.keys():
                urls.append(
                    {
                        "loc": f"{base_url}/{provincia_key}/{municipio_key}/{localidad_key}.html",
                        "lastmod": lastmod,
                        "changefreq": "monthly",
                        "priority": "0.7",
                    }
                )

    for industria_key in industrias_data.industrias.keys():
        urls.append(
            {
                "loc": f"{base_url}/industria/{industria_key}.html",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.7",
            }
        )

    # Los cursos sostienen la actividad docente, no el embudo comercial: se mantienen
    # indexables pero por debajo de casos, guías y landings de servicio.
    for curso in cursos_service.get_cursos_publicos():
        urls.append(
            {
                "loc": f"{base_url}/cursos/{curso.slug}",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.4",
            }
        )

    for instructor_id in cursos_service.get_instructores_dict().keys():
        urls.append(
            {
                "loc": f"{base_url}/cursos/instructor/{instructor_id}",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.3",
            }
        )

    for caso in cursos_service.get_casos():
        urls.append(
            {
                "loc": f"{base_url}/casos/{caso.slug}",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.9",
            }
        )

    for guia in cursos_service.get_guias():
        urls.append(
            {
                "loc": f"{base_url}/guias/{guia.slug}",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.9",
            }
        )

    for carrera in cursos_service.get_carreras():
        urls.append(
            {
                "loc": f"{base_url}/carreras/{carrera.slug}",
                "lastmod": lastmod,
                "changefreq": "monthly",
                "priority": "0.9",
            }
        )

    urls.append({"loc": f"{base_url}/noticias", "lastmod": lastmod, "changefreq": "weekly", "priority": "0.6"})
    try:
        noticias = await ListNoticiasUseCase(repository=noticia_repository).execute()
    except OperationalError:
        # Entornos sin la migración de contenido institucional aplicada (p. ej. tests
        # o desarrollo local sin DB): el sitemap no debe romperse por esto.
        noticias = []
    for noticia in noticias:
        if noticia.publicada and noticia.slug:
            urls.append(
                {
                    "loc": f"{base_url}/noticias/{noticia.slug}",
                    "lastmod": (noticia.updated_at or noticia.created_at or lastmod),
                    "changefreq": "monthly",
                    "priority": "0.5",
                }
            )

    urls.append({"loc": f"{base_url}/eventos", "lastmod": lastmod, "changefreq": "weekly", "priority": "0.6"})
    try:
        eventos = await ListEventosUseCase(repository=evento_repository).execute()
    except OperationalError:
        eventos = []
    for evento in eventos:
        if evento.publicada and evento.slug:
            urls.append(
                {
                    "loc": f"{base_url}/eventos/{evento.slug}",
                    "lastmod": (evento.updated_at or evento.created_at or lastmod),
                    "changefreq": "monthly",
                    "priority": "0.5",
                }
            )

    urls.append({"loc": f"{base_url}/comunicados", "lastmod": lastmod, "changefreq": "weekly", "priority": "0.6"})
    try:
        comunicados = await ListComunicadosUseCase(repository=comunicado_repository).execute()
    except OperationalError:
        comunicados = []
    for comunicado in comunicados:
        if comunicado.publicada and comunicado.slug:
            urls.append(
                {
                    "loc": f"{base_url}/comunicados/{comunicado.slug}",
                    "lastmod": (comunicado.updated_at or comunicado.created_at or lastmod),
                    "changefreq": "monthly",
                    "priority": "0.5",
                }
            )

    return templates.TemplateResponse(
        request=request, name="sitemap.xml", context={"urls": urls}, media_type="application/xml"
    )


@router.get("/dev/preview/{partial_name:path}")
async def preview(
    request: Request,
    partial_name: str,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    presented = present_contenido(contenido)
    context: dict[str, Any] = {
        "brand": presented["brand"],
        "content": presented["content"],
        "seo": presented["seo"],
        "footer": presented.get("footer"),
        "partial_name": partial_name,
        "config": config,
        "planes": cursos_service.get_planes(),
    }
    response = templates.TemplateResponse(request=request, name="preview.html", context=context)
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


@router.get("/")
async def root(
    request: Request,
    contenido: ContenidoModel = Depends(get_contenido),
    cursos_service: DataService = Depends(get_cursos_service),
):
    presented = present_contenido(contenido)
    base_seo: dict[str, Any] = presented["seo"]
    seo: dict[str, Any] = {
        **base_seo,
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: dict[str, Any] = {
        "brand": presented["brand"],
        "content": presented["content"],
        "seo": seo,
        "footer": presented.get("footer"),
        "casos": cursos_service.get_casos(),
        "guias": cursos_service.get_guias(),
        "cursos": cursos_service.get_cursos(),
        "carreras": cursos_service.get_carreras(),
        "planes": cursos_service.get_planes(),
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@router.get("/monitoreo")
async def monitoreo() -> RedirectResponse:
    return RedirectResponse(url="/cursos", status_code=301)


@router.get("/planes")
async def planes_alias() -> RedirectResponse:
    return RedirectResponse(url="/carreras", status_code=301)


@router.get("/pricing")
async def pricing_alias() -> RedirectResponse:
    return RedirectResponse(url="/carreras", status_code=301)


@router.get("/terminos-y-condiciones")
async def terms(request: Request, contenido: ContenidoModel = Depends(get_contenido)):
    presented = present_contenido(contenido)
    base_seo: dict[str, Any] = presented["seo"]
    seo: dict[str, Any] = {
        **base_seo,
        "title": f"{presented['legal_pages']['terms']['title']} | {presented['brand']['brandName']}",
        "description": f"Términos y condiciones de uso del sitio web de {presented['brand']['brandName']}.",
        "canonical_url": canonical_url(request.url),
        "og_image_width": 1200,
        "og_image_height": 630,
    }
    context: dict[str, Any] = {
        "brand": presented["brand"],
        "content": presented["content"],
        "terms": presented["legal_pages"]["terms"],
        "cookie_banner": presented["content"]["cookie_banner"],
        "seo": seo,
        "footer": presented.get("footer"),
    }
    return templates.TemplateResponse(request=request, name="terms.html", context=context)
