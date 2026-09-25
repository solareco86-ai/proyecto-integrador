"""Caso de uso para eliminar un comunicado."""

from src.application.gateways.image_storage_gateway import ImageStorageGateway
from src.domain.content.repositories import ComunicadoRepository


class DeleteComunicadoUseCase:
    """Elimina un comunicado por su id. Operación idempotente."""

    def __init__(self, repository: ComunicadoRepository, image_gateway: ImageStorageGateway) -> None:
        self._repository = repository
        self._image_gateway = image_gateway

    async def execute(self, comunicado_id: str) -> None:
        """Elimina el comunicado y, si tenía imagen asociada, su archivo. No falla si el id no existe."""
        existente = await self._repository.get_by_id(comunicado_id)
        await self._repository.delete(comunicado_id)
        if existente is not None:
            await self._image_gateway.delete(existente.imagen)
