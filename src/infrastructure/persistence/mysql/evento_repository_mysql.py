from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import RowMapping

from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository
from src.infrastructure.persistence.mysql.engine import get_engine
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)

_INSERT_SQL = text("""
    INSERT INTO eventos (id, titulo, descripcion, fecha_evento, lugar, autor_id, slug, created_at, updated_at)
    VALUES (:id, :titulo, :descripcion, :fecha_evento, :lugar, :autor_id, :slug, :created_at, :updated_at)
""")

_SELECT_BY_ID_SQL = text("SELECT * FROM eventos WHERE id = :id")
_SELECT_BY_SLUG_SQL = text("SELECT * FROM eventos WHERE slug = :slug")
_SELECT_ALL_SQL = text("SELECT * FROM eventos ORDER BY fecha_evento ASC")

_UPDATE_SQL = text("""
    UPDATE eventos
    SET titulo = :titulo, descripcion = :descripcion, fecha_evento = :fecha_evento,
        lugar = :lugar, slug = :slug, updated_at = :updated_at
    WHERE id = :id
""")

_DELETE_SQL = text("DELETE FROM eventos WHERE id = :id")


class EventoRepositorySQL(EventoRepository):
    """Implementación de EventoRepository con SQLAlchemy async.

    Soporta SQLite (desarrollo local) y MySQL (producción VPS).
    El dialecto se determina por DATABASE_URL.
    """

    def __init__(self) -> None:
        self._engine = get_engine()

    async def save(self, evento: Evento) -> None:
        data = self._to_row(evento)
        logger.debug("[EventoRepositorySQL] Guardando evento %s", data["id"])
        async with self._engine.begin() as conn:
            from src.infrastructure.persistence.mysql.models import Base

            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(_INSERT_SQL, data)
        logger.info("[EventoRepositorySQL] Evento %s guardado", data["id"])

    async def get_by_id(self, evento_id: str) -> Evento | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_ID_SQL, {"id": evento_id})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def get_by_slug(self, slug: str) -> Evento | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_SLUG_SQL, {"slug": slug})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def list_all(self) -> list[Evento]:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_ALL_SQL)
            return [self._to_entity(row) for row in result.mappings().all()]

    async def update(self, evento: Evento) -> None:
        data = self._to_row(evento)
        async with self._engine.begin() as conn:
            await conn.execute(_UPDATE_SQL, data)
        logger.info("[EventoRepositorySQL] Evento %s actualizado", evento.id)

    async def delete(self, evento_id: str) -> None:
        async with self._engine.begin() as conn:
            await conn.execute(_DELETE_SQL, {"id": evento_id})
        logger.info("[EventoRepositorySQL] Evento %s eliminado (si existía)", evento_id)

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos."""
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.warning("[EventoRepositorySQL] Health check falló: %s", e)
            return False

    @staticmethod
    def _to_row(evento: Evento) -> dict[str, Any]:
        created_at = _parse_datetime(evento.created_at) or datetime.utcnow()
        fecha_evento = _parse_datetime(evento.fecha_evento)
        return {
            "id": evento.id,
            "titulo": evento.titulo,
            "descripcion": evento.descripcion,
            "fecha_evento": fecha_evento,
            "lugar": evento.lugar,
            "autor_id": evento.autor_id,
            "slug": evento.slug,
            "created_at": created_at,
            "updated_at": _parse_datetime(evento.updated_at),
        }

    @staticmethod
    def _to_entity(row: RowMapping) -> Evento:
        return Evento(
            id=row["id"],
            titulo=row["titulo"],
            descripcion=row["descripcion"],
            fecha_evento=_format_datetime(row["fecha_evento"]) or "",
            lugar=row["lugar"],
            autor_id=row["autor_id"],
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
