from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.exceptions import HTTPException

from src.application.dtos import ContenidoModel
from src.infrastructure.fastapi.dependencies import CachedStaticFiles, data_service, get_contenido, templates
from src.infrastructure.fastapi.metrics import metrics_middleware
from src.infrastructure.fastapi.middleware import (
    cache_control_middleware,
    canonical_redirect_middleware,
    rate_limit_middleware,
    request_id_middleware,
    security_headers_middleware,
)
from src.infrastructure.fastapi.utils.seo import canonical_url
from src.infrastructure.settings import config

# --- Inicialización de FastAPI ---

app = FastAPI(title=config.APP_TITLE)
app.state.config = config
app.middleware("http")(request_id_middleware)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(canonical_redirect_middleware)
app.middleware("http")(security_headers_middleware)
app.middleware("http")(cache_control_middleware)
app.middleware("http")(metrics_middleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/static", CachedStaticFiles(directory=config.STATIC_DIR), name="static")

# --- Manejadores de error ---


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        path = request.url.path

        # No aplicar lógica de redirección a archivos estáticos ni API
        if not path.startswith("/static") and not path.startswith("/api"):
            # Redirecciones 301 puntuales para URLs legacy (si están configuradas)
            redirects = data_service.get_redirects()
            target = redirects.get(path)
            if target:
                return RedirectResponse(url=target, status_code=301)

        contenido: ContenidoModel = get_contenido()
        seo: dict[str, Any] = {
            "title": f"Página no encontrada | {contenido.brand.brandName}",
            "description": "La página solicitada no existe.",
            "canonical_url": canonical_url(request.url),
            "site_name": contenido.brand.brandName,
            "og_image": contenido.seo.og_image,
            "og_image_width": 1200,
            "og_image_height": 630,
        }
        context: dict[str, Any] = {
            "request": request,
            "brand": contenido.brand.model_dump(),
            "content": contenido.content.model_dump(),
            "seo": seo,
            "footer": contenido.footer.model_dump() if contenido.footer else None,
            "page_robots": "noindex,follow",
        }
        return templates.TemplateResponse(request=request, name="404.html", context=context, status_code=404)

    if exc.status_code >= 500:
        contenido = get_contenido()
        seo_500: dict[str, Any] = {
            "title": f"Inconveniente en el Servidor | {contenido.brand.brandName}",
            "description": "Estamos trabajando para resolver un inconveniente técnico. Podés contactarnos directamente por WhatsApp.",
            "canonical_url": canonical_url(request.url),
            "site_name": contenido.brand.brandName,
            "og_image": contenido.seo.og_image,
            "og_image_width": 1200,
            "og_image_height": 630,
        }
        context_500: dict[str, Any] = {
            "request": request,
            "brand": contenido.brand.model_dump(),
            "content": contenido.content.model_dump(),
            "seo": seo_500,
            "footer": contenido.footer.model_dump() if contenido.footer else None,
            "page_robots": "noindex,nofollow",
        }
        return templates.TemplateResponse(
            request=request, name="500.html", context=context_500, status_code=exc.status_code
        )

    response = HTMLResponse(
        content=f"<h1>Error {exc.status_code}</h1><p>Error interno del servidor</p>", status_code=exc.status_code
    )
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


# --- Registro de Routers ---
from src.infrastructure.fastapi.routes.carreras_routes import router as carreras_router
from src.infrastructure.fastapi.routes.caso_routes import router as caso_router
from src.infrastructure.fastapi.routes.contact_routes import router as contact_router
from src.infrastructure.fastapi.routes.course_routes import router as course_router
from src.infrastructure.fastapi.routes.guia_routes import router as guia_router
from src.infrastructure.fastapi.routes.industry_routes import router as industry_router
from src.infrastructure.fastapi.routes.landing_routes import router as landing_router
from src.infrastructure.fastapi.routes.main_routes import router as main_router
from src.infrastructure.fastapi.routes.seo_routes import router as seo_router

# Eliminamos el prefijo para respetar la estructura de URLs solicitada
app.include_router(main_router)
app.include_router(carreras_router)
app.include_router(industry_router)
app.include_router(contact_router)
app.include_router(landing_router)
app.include_router(course_router)
app.include_router(caso_router)
app.include_router(guia_router)
app.include_router(seo_router)  # Debe ir último: sus rutas /{provincia} y /{provincia}/{municipio} son catch-all
