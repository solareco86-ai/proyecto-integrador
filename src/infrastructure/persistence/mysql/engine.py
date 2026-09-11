"""Engine SQLAlchemy async compartido para los repositorios de contenido institucional.

Nota: `lead_repository_mysql.py` mantiene su propio singleton de engine
independiente (no se modificó) para no alterar su comportamiento actual,
dado que `test_lead_repository_engine.py` parchea sus símbolos internos
directamente. Este módulo evita duplicar la lógica de construcción del
engine entre los repositorios nuevos (noticias, eventos, comunicados).
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.infrastructure.settings import config

# Engine singleton: se crea una sola vez al importar, no por request
_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """Devuelve el engine singleton compartido, creándolo la primera vez."""
    global _engine
    if _engine is None:
        db_url = config.DATABASE_URL or "sqlite+aiosqlite:///data/leads.db"
        engine_kwargs: dict[str, Any] = {"echo": config.DEBUG}
        if "mysql" in db_url:
            # Mismo criterio que lead_repository_mysql.py: pool_pre_ping es
            # incompatible con aiomysql, y pool_recycle evita conexiones muertas.
            engine_kwargs.update({"pool_size": 3, "max_overflow": 2, "pool_recycle": 1800})
        _engine = create_async_engine(db_url, **engine_kwargs)
    return _engine
