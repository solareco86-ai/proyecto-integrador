"""Caso de uso para eliminar un comunicado."""

from src.domain.content.repositories import ComunicadoRepository


class DeleteComunicadoUseCase:
    """Elimina un comunicado por su id. Operación idempotente."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self, comunicado_id: str) -> None:
        """Elimina el comunicado; no falla si el id no existe."""
        await self._repository.delete(comunicado_id)
