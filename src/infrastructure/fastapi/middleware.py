import logging
import time
import uuid
from collections import defaultdict
from urllib.parse import urlunsplit

from fastapi import Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import RequestResponseEndpoint

from src.infrastructure.fastapi.csp import build_csp
from src.infrastructure.settings import config

logger = logging.getLogger(config.LOGGER_NAME)

# --- Request ID ---


async def request_id_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Genera o propaga X-Request-ID para correlacionar logs."""
    request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:12]}"
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# --- Rate Limiting (in-memory, single-process) ---

_rate_store: dict[str, list[float]] = defaultdict(list)


async def rate_limit_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Rate-limiting mínimo para el endpoint de contacto."""
    if request.url.path == "/api/v1/contact" and request.method == "POST":
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        cutoff = now - config.RATE_LIMIT_WINDOW_SECONDS

        # Limpiar timestamps viejos de esta IP
        _rate_store[client_ip] = [t for t in _rate_store[client_ip] if t > cutoff]

        if len(_rate_store[client_ip]) >= config.RATE_LIMIT_MAX_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"detail": "Demasiadas solicitudes. Intente nuevamente en un minuto."},
            )

        _rate_store[client_ip].append(now)

    return await call_next(request)


# --- Canonical Redirect ---


def _canonical_parts(request: Request) -> tuple[str, str, str]:
    """
    Devuelve la versión canónica (scheme, host, path) para la request.

    Reglas:
      - HTTPS cuando el reverse proxy indica HTTP (vía X-Forwarded-Proto).
      - Sin prefijo www.
      - Sin trailing slash, salvo que el path sea '/'.
    """
    scheme = request.url.scheme
    host = request.url.hostname or ""
    path = request.url.path

    # Detectar HTTPS a través del reverse proxy. Si el proxy ya redirige HTTP→HTTPS
    # y no envía este header, no forzamos redirección para evitar loops.
    forwarded_proto = request.headers.get("x-forwarded-proto")
    if forwarded_proto and forwarded_proto.lower() == "http":
        scheme = "https"

    # Normalizar www → dominio raíz
    if host.startswith("www."):
        host = host[4:]

    # Normalizar trailing slash
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    return scheme, host, path


async def security_headers_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """
    Middleware que agrega cabeceras de seguridad basicas a todas las respuestas.
    """
    response = await call_next(request)
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Strict-Transport-Security", config.HSTS_HEADER)
    response.headers["X-Commit-SHA"] = config.GIT_COMMIT_SHA
    if "text/html" in response.headers.get("content-type", ""):
        telemetry_hosts = tuple(h for h in (config.TELEMETRY_API_URL, config.TELEMETRY_WS_URL) if h)
        try:
            response.headers.setdefault("Content-Security-Policy", build_csp(telemetry_hosts))
            logger.debug(
                "Content-Security-Policy header set",
                {
                    "csp": response.headers.get("Content-Security-Policy"),
                    "telemetry_connect": " ".join(telemetry_hosts),
                },
            )
        except Exception as e:
            logger.error("Failed to set Content-Security-Policy header", exc_info=e)
    return response


async def canonical_redirect_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """
    Middleware que redirige con HTTP 308 a la URL canónica cuando sea necesario.

    No redirige peticiones a archivos estáticos ni a la API por motivos de trailing
    slash; sí normaliza scheme/host para todo el tráfico.
    """
    scheme, host, path = _canonical_parts(request)

    current_scheme = request.url.scheme
    current_host = request.url.hostname or ""
    current_path = request.url.path

    needs_redirect = scheme != current_scheme or host != current_host or path != current_path

    if needs_redirect:
        canonical = urlunsplit((scheme, host, path, request.url.query, ""))
        return RedirectResponse(url=canonical, status_code=308)

    return await call_next(request)


async def cache_control_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """
    Middleware que añade cabeceras Cache-Control a las páginas HTML y sitemaps XML.
    En desarrollo (config.DEBUG=True) o rutas de previsualización no añade caché.
    """
    response = await call_next(request)

    if config.DEBUG:
        return response

    path = request.url.path
    if path.startswith("/dev/preview"):
        return response

    content_type = response.headers.get("content-type", "")
    if response.status_code == 200:
        if "text/html" in content_type or "application/xml" in content_type:
            response.headers["Cache-Control"] = config.HTML_CACHE_CONTROL

    return response
