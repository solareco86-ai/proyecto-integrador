"""Caso de uso para eliminar una noticia."""

from src.application.gateways.image_storage_gateway import ImageStorageGateway
from src.domain.content.repositories import NoticiaRepository


class DeleteNoticiaUseCase:
    """Elimina una noticia por su id. Operación idempotente."""

    def __init__(self, repository: NoticiaRepository, image_gateway: ImageStorageGateway) -> None:
        self._repository = repository
        self._image_gateway = image_gateway

    async def execute(self, noticia_id: str) -> None:
        """Elimina la noticia y, si tenía imagen asociada, su archivo. No falla si el id no existe."""
        existente = await self._repository.get_by_id(noticia_id)
        await self._repository.delete(noticia_id)
        if existente is not None:
            await self._image_gateway.delete(existente.imagen)
