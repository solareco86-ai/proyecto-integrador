from dataclasses import asdict
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.domain.entities.lead import Lead
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.settings import config
from src.infrastructure.settings.logger import setup_logger

logger = setup_logger(config.LOGGER_NAME, debug=config.DEBUG)

_INSERT_SQL = text("""
    INSERT INTO leads (id, name, first_name, last_name, email, phone, company, comment,
                       preferred_contact_channel, page_location, traffic_source, user_agent,
                       geographic_location, created_at, captcha_token,
                       gclid, fbclid, utm_source, utm_medium, utm_campaign, lead_source)
    VALUES (:id, :name, :first_name, :last_name, :email, :phone, :company, :comment,
            :preferred_contact_channel, :page_location, :traffic_source, :user_agent,
            :geographic_location, :created_at, :captcha_token,
            :gclid, :fbclid, :utm_source, :utm_medium, :utm_campaign, :lead_source)
""")

# Engine singleton: se crea una sola vez al importar, no por request
_engine: AsyncEngine | None = None


def _get_engine() -> AsyncEngine:
    """Devuelve el engine singleton, creándolo la primera vez."""
    global _engine
    if _engine is None:
        db_url = config.DATABASE_URL or "sqlite+aiosqlite:///data/leads.db"
        engine_kwargs: dict[str, Any] = {"echo": config.DEBUG}
        if "mysql" in db_url:
            # pool_pre_ping es incompatible con aiomysql: el do_ping síncrono de
            # SQLAlchemy llama ping() sin `reconnect`, que el adaptador async de
            # aiomysql exige como argumento posicional (rompe el 2º checkout).
            # pool_recycle descarta conexiones inactivas antes de que MySQL cierre el socket por wait_timeout.
            engine_kwargs.update({"pool_size": 3, "max_overflow": 2, "pool_recycle": 1800})
        _engine = create_async_engine(db_url, **engine_kwargs)
    return _engine


class LeadRepositorySQL(LeadRepository):
    """Implementación de LeadRepository con SQLAlchemy async.

    Soporta SQLite (desarrollo local) y MySQL (producción VPS).
    El dialecto se determina por DATABASE_URL.
    """

    def __init__(self) -> None:
        self._engine = _get_engine()

    async def save(self, lead: Lead) -> None:
        data = asdict(lead)
        data["id"] = str(lead.id)
        data["first_name"] = lead.contact.first_name
        data["last_name"] = lead.contact.last_name
        data["name"] = lead.contact.name
        data["email"] = lead.contact.email
        data["phone"] = lead.contact.phone
        data["company"] = lead.contact.company
        data["preferred_contact_channel"] = lead.preferred_contact_channel
        data["page_location"] = lead.page_location
        data["traffic_source"] = lead.traffic_source
        data["user_agent"] = lead.user_agent
        data["geographic_location"] = lead.geographic_location
        data["created_at"] = lead.created_at
        data["captcha_token"] = lead.captcha_token
        data["gclid"] = lead.gclid
        data["fbclid"] = lead.fbclid
        data["utm_source"] = lead.utm_source
        data["utm_medium"] = lead.utm_medium
        data["utm_campaign"] = lead.utm_campaign
        data["lead_source"] = lead.lead_source

        logger.debug("[LeadRepositorySQL] Guardando lead %s", data["id"])
        async with self._engine.begin() as conn:
            # Asegurar que la tabla existe con todas las columnas
            from src.infrastructure.persistence.mysql.models import Base

            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(_INSERT_SQL, data)
        logger.info("[LeadRepositorySQL] Lead %s guardado", data["id"])

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos."""
        try:
            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.warning("[LeadRepositorySQL] Health check falló: %s", e)
            return False
