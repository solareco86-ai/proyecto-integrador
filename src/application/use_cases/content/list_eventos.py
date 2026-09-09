"""Caso de uso para listar todos los eventos."""

from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class ListEventosUseCase:
    """Devuelve todos los eventos almacenados."""

    def __init__(self, repository: EventoRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Evento]:
        """Devuelve la lista completa de eventos."""
        return await self._repository.list_all()
