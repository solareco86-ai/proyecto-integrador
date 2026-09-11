"""Caso de uso para eliminar una noticia."""

from src.domain.content.repositories import NoticiaRepository


class DeleteNoticiaUseCase:
    """Elimina una noticia por su id. Operación idempotente."""

    def __init__(self, repository: NoticiaRepository) -> None:
        self._repository = repository

    async def execute(self, noticia_id: str) -> None:
        """Elimina la noticia; no falla si el id no existe."""
        await self._repository.delete(noticia_id)
