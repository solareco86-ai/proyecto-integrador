from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import RowMapping

from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.persistence.mysql.engine import get_engine
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)

_INSERT_SQL = text("""
    INSERT INTO noticias (id, titulo, cuerpo, autor_id, publicada, slug, created_at, updated_at)
    VALUES (:id, :titulo, :cuerpo, :autor_id, :publicada, :slug, :created_at, :updated_at)
""")

_SELECT_BY_ID_SQL = text("SELECT * FROM noticias WHERE id = :id")
_SELECT_BY_SLUG_SQL = text("SELECT * FROM noticias WHERE slug = :slug")
_SELECT_ALL_SQL = text("SELECT * FROM noticias ORDER BY created_at DESC")

_UPDATE_SQL = text("""
    UPDATE noticias
    SET titulo = :titulo, cuerpo = :cuerpo, publicada = :publicada, slug = :slug, updated_at = :updated_at
    WHERE id = :id
""")

_DELETE_SQL = text("DELETE FROM noticias WHERE id = :id")


class NoticiaRepositorySQL(NoticiaRepository):
    """Implementación de NoticiaRepository con SQLAlchemy async.

    Soporta SQLite (desarrollo local) y MySQL (producción VPS).
    El dialecto se determina por DATABASE_URL.
    """

    def __init__(self) -> None:
        self._engine = get_engine()

    async def save(self, noticia: Noticia) -> None:
        data = self._to_row(noticia)
        logger.debug("[NoticiaRepositorySQL] Guardando noticia %s", data["id"])
        async with self._engine.begin() as conn:
            from src.infrastructure.persistence.mysql.models import Base

            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(_INSERT_SQL, data)
        logger.info("[NoticiaRepositorySQL] Noticia %s guardada", data["id"])

    async def get_by_id(self, noticia_id: str) -> Noticia | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_ID_SQL, {"id": noticia_id})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def get_by_slug(self, slug: str) -> Noticia | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_SLUG_SQL, {"slug": slug})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def list_all(self) -> list[Noticia]:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_ALL_SQL)
            return [self._to_entity(row) for row in result.mappings().all()]

    async def update(self, noticia: Noticia) -> None:
        data = self._to_row(noticia)
        async with self._engine.begin() as conn:
            await conn.execute(_UPDATE_SQL, data)
        logger.info("[NoticiaRepositorySQL] Noticia %s actualizada", noticia.id)

    async def delete(self, noticia_id: str) -> None:
        async with self._engine.begin() as conn:
            await conn.execute(_DELETE_SQL, {"id": noticia_id})
        logger.info("[NoticiaRepositorySQL] Noticia %s eliminada (si existía)", noticia_id)

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos."""
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.warning("[NoticiaRepositorySQL] Health check falló: %s", e)
            return False

    @staticmethod
    def _to_row(noticia: Noticia) -> dict[str, Any]:
        created_at = _parse_datetime(noticia.created_at) or datetime.utcnow()
        return {
            "id": noticia.id,
            "titulo": noticia.titulo,
            "cuerpo": noticia.cuerpo,
            "autor_id": noticia.autor_id,
            "publicada": noticia.publicada,
            "slug": noticia.slug,
            "created_at": created_at,
            "updated_at": _parse_datetime(noticia.updated_at),
        }

    @staticmethod
    def _to_entity(row: RowMapping) -> Noticia:
        return Noticia(
            id=row["id"],
            titulo=row["titulo"],
            cuerpo=row["cuerpo"],
            autor_id=row["autor_id"],
            publicada=bool(row["publicada"]),
            slug=row["slug"],
            created_at=_format_datetime(row["created_at"]),
            updated_at=_format_datetime(row["updated_at"]),
        )


def _parse_datetime(value: str | None) -> datetime | None:
    """Convierte un timestamp ISO del dominio a datetime para SQLAlchemy."""
    if value is None:
        return None
    return datetime.fromisoformat(value)


def _format_datetime(value: Any) -> str | None:
    """Normaliza un valor de columna DATETIME a str ISO para el dominio."""
    if value is None:
        return None
    return value.isoformat() if isinstance(value, datetime) else value
