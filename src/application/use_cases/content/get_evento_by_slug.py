"""Caso de uso para obtener un evento por su slug."""

from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class GetEventoBySlugUseCase:
    """Busca un evento por su slug."""

    def __init__(self, repository: EventoRepository) -> None:
        self._repository = repository

    async def execute(self, slug: str) -> Evento | None:
        """Devuelve el evento si existe, o None."""
        return await self._repository.get_by_slug(slug)
