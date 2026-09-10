import hashlib
import os
import time
from datetime import datetime
from typing import Any, cast

from fastapi import Depends, HTTPException, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.types import Scope

from src.application.data_service import DataService
from src.application.dtos import ContenidoModel, LandingContentModel
from src.application.gateways.notification_gateway import NotificationGateway
from src.application.gateways.password_hasher_gateway import PasswordHasherGateway
from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.content.repositories import EventoRepository, NoticiaRepository
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.gateways.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.gateways.email_notification_gateway import EmailNotificationGateway
from src.infrastructure.persistence.mysql.evento_repository_mysql import EventoRepositorySQL
from src.infrastructure.persistence.mysql.lead_repository_mysql import LeadRepositorySQL
from src.infrastructure.persistence.mysql.noticia_repository_mysql import NoticiaRepositorySQL
from src.infrastructure.persistence.mysql.usuario_repository_mysql import UsuarioRepositorySQL
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)

# --- Instancias compartidas ---


class CachedStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        # En desarrollo desactivamos caché inmutable
        if config.DEBUG:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        elif scope.get("query_string"):
            # Recursos versionados (?v=<hash>): la URL cambia con el contenido,
            # por lo que es seguro servirlos como inmutables.
            response.headers["Cache-Control"] = (
                f"public, max-age={config.STATIC_CACHE_SECONDS}, immutable"
            )
        else:
            # Módulos y assets sin versión (imports relativos): revalidación corta
            # con 304 vía ETag/Last-Modified para no servir archivos viejos.
            response.headers["Cache-Control"] = f"public, max-age={config.STATIC_MODULE_MAX_AGE}"
        return response


templates = Jinja2Templates(directory=config.TEMPLATES_DIR)
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True
templates.env.globals = cast(dict[str, Any], templates.env.globals)  # type: ignore[assignment]

# --- Configuración del Servicio de Datos ---
data_service = DataService(data_dir=config.DATA_DIR)


# --- Dependencias de Datos ---
def get_contenido() -> ContenidoModel:
    return data_service.get_contenido()


def get_geografia():
    return data_service.get_geografia()


def get_industrias():
    return data_service.get_industrias()


def get_cursos_service() -> DataService:
    return data_service


def get_landing_content() -> LandingContentModel:
    return data_service.get_landing_content()


def get_landing_campaigns():
    return data_service.get_landing_campaigns()


# --- Dependencias de Infraestructura (Repository + Gateway) ---
def get_lead_repository() -> LeadRepository:
    return LeadRepositorySQL()


# --- Dependencias de Autenticación (panel de autoridades) ---
def get_usuario_repository() -> UsuarioRepository:
    return UsuarioRepositorySQL()


def get_password_hasher() -> PasswordHasherGateway:
    return BcryptPasswordHasher()


def get_noticia_repository() -> NoticiaRepository:
    return NoticiaRepositorySQL()


def get_evento_repository() -> EventoRepository:
    return EventoRepositorySQL()


async def get_current_user(
    request: Request,
    usuario_repository: UsuarioRepository = Depends(get_usuario_repository),
) -> Usuario | None:
    """Devuelve el usuario autenticado según la sesión, o None si no hay sesión válida.

    Re-consulta siempre la DB (nunca confía solo en la cookie) para que una
    desactivación (is_active=False) tenga efecto inmediato.
    """
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    usuario = await usuario_repository.get_by_id(user_id)
    if usuario is None or not usuario.is_active:
        return None
    return usuario


async def require_authority(
    usuario: Usuario | None = Depends(get_current_user),
) -> Usuario:
    """Exige una sesión autenticada con rol 'autoridad'.

    Sin sesión válida (o usuario inactivo, ya descartado por get_current_user)
    redirige a /panel/login. Con sesión válida pero rol distinto de
    'autoridad', deniega el acceso con 403.
    """
    if usuario is None:
        raise HTTPException(status_code=303, headers={"Location": "/panel/login"})
    if usuario.rol != "autoridad":
        raise HTTPException(status_code=403, detail="No autorizado")
    return usuario


from src.infrastructure.gateways.datamaq_hub_gateway import DatamaqHubGateway
from src.infrastructure.gateways.email_notification_gateway import (
    ConsoleNotificationGateway,
)
from src.infrastructure.gateways.ga4_measurement_gateway import GA4MeasurementGateway
from src.infrastructure.gateways.telegram_notification_gateway import (
    CompositeNotificationGateway,
    TelegramNotificationGateway,
)


def get_notification_gateway() -> NotificationGateway:
    active_gateways: list[NotificationGateway] = []

    if config.SMTP_USERNAME and config.SMTP_PASSWORD and config.NOTIFICATION_EMAIL:
        active_gateways.append(
            EmailNotificationGateway(
                host=config.SMTP_HOST,
                port=config.SMTP_PORT,
                username=config.SMTP_USERNAME,
                password=config.SMTP_PASSWORD,
                to_email=config.NOTIFICATION_EMAIL,
            )
        )

    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
        active_gateways.append(
            TelegramNotificationGateway(
                bot_token=config.TELEGRAM_BOT_TOKEN,
                chat_id=config.TELEGRAM_CHAT_ID,
            )
        )

    if config.GA4_MEASUREMENT_ID and config.GA4_API_SECRET:
        active_gateways.append(
            GA4MeasurementGateway(
                measurement_id=config.GA4_MEASUREMENT_ID,
                api_secret=config.GA4_API_SECRET,
            )
        )

    if config.DATAMAQ_HUB_URL:
        active_gateways.append(
            DatamaqHubGateway(
                hub_url=config.DATAMAQ_HUB_URL,
                api_key=config.DATAMAQ_HUB_API_KEY,
            )
        )

    if not active_gateways:
        logger.info(
            "[dependencies] Ningún canal de notificación configurado (SMTP/Telegram/GA4/Hub) — "
            "usando ConsoleNotificationGateway para desarrollo local."
        )
        return ConsoleNotificationGateway()

    if len(active_gateways) == 1:
        return active_gateways[0]

    return CompositeNotificationGateway(active_gateways)


# --- Configuración Jinja2 ---

# TTL (segundos) del hash de contenido cacheado de la carpeta static/.
_STATIC_VERSION_TTL_SECONDS = 60

# Caché del hash de contenido: (momento_monotónico, hash). Se recalcula al expirar
# el TTL, de modo que un deploy o cambio de archivo se refleja sin reiniciar el
# proceso (a diferencia del SHA de git cacheado al boot).
_static_version_cache: tuple[float, str] | None = None


def _hash_static_tree() -> str:
    """Calcula un hash SHA-256 del contenido y rutas de la carpeta static/."""
    digest = hashlib.sha256()
    for root, dirs, files in os.walk(config.STATIC_DIR):
        dirs.sort()
        for name in sorted(files):
            rel_path = os.path.join(root, name)
            digest.update(rel_path.encode("utf-8"))
            try:
                with open(rel_path, "rb") as handle:
                    digest.update(handle.read())
            except OSError:
                # Archivo ilegible (permisos o borrado concurrente): se omite.
                continue
    return digest.hexdigest()[:12]


def get_static_version() -> str:
    """Versión de cache-busting: timestamp en DEBUG, hash de contenido en prod."""
    global _static_version_cache
    if config.DEBUG:
        return str(int(time.time()))
    now = time.monotonic()
    if _static_version_cache is None or (now - _static_version_cache[0]) > _STATIC_VERSION_TTL_SECONDS:
        try:
            digest = _hash_static_tree()
        except Exception as e:
            logger.warning("No se pudo hashear static/. Error: %s. Usando timestamp.", e)
            digest = str(int(time.time()))
        _static_version_cache = (now, digest)
    return _static_version_cache[1]


templates.env.globals["static_version"] = get_static_version  # type: ignore[index]
templates.env.globals["config"] = config  # type: ignore[index]
templates.env.globals["year"] = datetime.now().year
templates.env.globals["commit_sha"] = config.GIT_COMMIT_SHA
