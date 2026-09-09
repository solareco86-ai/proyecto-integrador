from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import RowMapping

from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.infrastructure.persistence.mysql.engine import get_engine
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)

_INSERT_SQL = text("""
    INSERT INTO usuarios (id, email, password_hash, nombre, rol, is_active, created_at)
    VALUES (:id, :email, :password_hash, :nombre, :rol, :is_active, :created_at)
""")

_SELECT_BY_ID_SQL = text("SELECT * FROM usuarios WHERE id = :id")
_SELECT_BY_EMAIL_SQL = text("SELECT * FROM usuarios WHERE email = :email")


class UsuarioRepositorySQL(UsuarioRepository):
    """Implementación de UsuarioRepository con SQLAlchemy async.

    Soporta SQLite (desarrollo local) y MySQL (producción VPS).
    El dialecto se determina por DATABASE_URL.
    """

    def __init__(self) -> None:
        self._engine = get_engine()

    async def save(self, usuario: Usuario) -> None:
        data = self._to_row(usuario)
        logger.debug("[UsuarioRepositorySQL] Guardando usuario %s", data["id"])
        async with self._engine.begin() as conn:
            from src.infrastructure.persistence.mysql.models import Base

            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(_INSERT_SQL, data)
        logger.info("[UsuarioRepositorySQL] Usuario %s guardado", data["id"])

    async def get_by_id(self, usuario_id: str) -> Usuario | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_ID_SQL, {"id": usuario_id})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def get_by_email(self, email: str) -> Usuario | None:
        async with self._engine.connect() as conn:
            result = await conn.execute(_SELECT_BY_EMAIL_SQL, {"email": email})
            row = result.mappings().first()
            return self._to_entity(row) if row is not None else None

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos."""
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.warning("[UsuarioRepositorySQL] Health check falló: %s", e)
            return False

    @staticmethod
    def _to_row(usuario: Usuario) -> dict[str, Any]:
        created_at = _parse_datetime(usuario.created_at) or datetime.utcnow()
        return {
            "id": usuario.id,
            "email": usuario.email,
            "password_hash": usuario.password_hash,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "is_active": usuario.is_active,
            "created_at": created_at,
        }

    @staticmethod
    def _to_entity(row: RowMapping) -> Usuario:
        return Usuario(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            nombre=row["nombre"],
            rol=row["rol"],
            is_active=bool(row["is_active"]),
            created_at=_format_datetime(row["created_at"]),
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
