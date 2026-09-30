"""Caso de uso para eliminar un evento."""

from src.application.gateways.image_storage_gateway import ImageStorageGateway
from src.domain.content.repositories import EventoRepository


class DeleteEventoUseCase:
    """Elimina un evento por su id. Operación idempotente."""

    def __init__(self, repository: EventoRepository, image_gateway: ImageStorageGateway) -> None:
        self._repository = repository
        self._image_gateway = image_gateway

    async def execute(self, evento_id: str) -> None:
        """Elimina el evento y, si tenía imagen asociada, su archivo. No falla si el id no existe."""
        existente = await self._repository.get_by_id(evento_id)
        await self._repository.delete(evento_id)
        if existente is not None:
            await self._image_gateway.delete(existente.imagen)
