"""Caso de uso para eliminar un evento."""

from src.domain.content.repositories import EventoRepository


class DeleteEventoUseCase:
    """Elimina un evento por su id. Operación idempotente."""

    def __init__(self, repository: EventoRepository) -> None:
        self._repository = repository

    async def execute(self, evento_id: str) -> None:
        """Elimina el evento; no falla si el id no existe."""
        await self._repository.delete(evento_id)
