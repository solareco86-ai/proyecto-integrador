"""Caso de uso para obtener un evento por id."""

from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class GetEventoUseCase:
    """Busca un evento por su id."""

    def __init__(self, repository: EventoRepository) -> None:
        self._repository = repository

    async def execute(self, evento_id: str) -> Evento | None:
        """Devuelve el evento si existe, o None."""
        return await self._repository.get_by_id(evento_id)
