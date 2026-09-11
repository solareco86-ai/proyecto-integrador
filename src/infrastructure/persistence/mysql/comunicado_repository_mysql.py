from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import RowMapping

from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.persistence.mysql.engine import get_engine
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)

_INSERT_SQL = text("""
    INSERT INTO comunicados (id, titulo, cuerpo, autor_id, publicada, slug, created_at, updated_at)
    VALUES (:id, :titulo, :cuerpo, :autor_id, :publicada, :slug, :created_at, :updated_at)
""")

_SELECT_BY_ID_SQL = text("SELECT * FROM comunicados WHERE id = :id")
_SELECT_BY_SLUG_SQL = text("SELECT * FROM comunicados WHERE slug = :slug")
_SELECT_ALL_SQL = text("SELECT * FROM comunicados ORDER BY created_at DESC")

_UPDATE_SQL = text("""
    UPDATE comunicados
    SET titulo = :titulo, cuerpo = :cuerpo, publicada = :publicada, slug = :slug, updated_at = :updated_at
    WHERE id = :id
""")

_DELETE_SQL = text("DELETE FROM comunicados WHERE id = :id")


class ComunicadoRepositorySQL(ComunicadoRepository):
    """Implementación de ComunicadoRepository con SQLAlchemy async.

    Soporta SQLite (desarrollo local) y MySQL (producción VPS).
    El dialecto se determina por DATABASE_URL.
    """

    def __init__(self) -> None:
        self._engine = get_engine()

    async def save(self, comunicado: Comunicado) -> None:
        data = self._to_row(comunicado)
        logger.debug("[ComunicadoRepositorySQL] Guardando comunicado %s", data["id"])
        async with self._engine.begin() as conn:
            from src.infrastructure.persistence.mysql.models import Base

            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(_INSERT_SQL, data)
        logger.info("[ComunicadoRepositorySQL] Comunicado %s guardado", data["id"])

    async def get_by_id(self, comunicado_id: str) -> Comunicado | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_ID_SQL, {"id": comunicado_id})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def get_by_slug(self, slug: str) -> Comunicado | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_SLUG_SQL, {"slug": slug})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def list_all(self) -> list[Comunicado]:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_ALL_SQL)
            return [self._to_entity(row) for row in result.mappings().all()]

    async def update(self, comunicado: Comunicado) -> None:
        data = self._to_row(comunicado)
        async with self._engine.begin() as conn:
            await conn.execute(_UPDATE_SQL, data)
        logger.info("[ComunicadoRepositorySQL] Comunicado %s actualizado", comunicado.id)

    async def delete(self, comunicado_id: str) -> None:
        async with self._engine.begin() as conn:
            await conn.execute(_DELETE_SQL, {"id": comunicado_id})
        logger.info("[ComunicadoRepositorySQL] Comunicado %s eliminado (si existía)", comunicado_id)

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos."""
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.warning("[ComunicadoRepositorySQL] Health check falló: %s", e)
            return False

    @staticmethod
    def _to_row(comunicado: Comunicado) -> dict[str, Any]:
        created_at = _parse_datetime(comunicado.created_at) or datetime.utcnow()
        return {
            "id": comunicado.id,
            "titulo": comunicado.titulo,
            "cuerpo": comunicado.cuerpo,
            "autor_id": comunicado.autor_id,
            "publicada": comunicado.publicada,
            "slug": comunicado.slug,
            "created_at": created_at,
            "updated_at": _parse_datetime(comunicado.updated_at),
        }

    @staticmethod
    def _to_entity(row: RowMapping) -> Comunicado:
        return Comunicado(
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
