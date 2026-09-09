"""Caso de uso para obtener un comunicado por id."""

from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class GetComunicadoUseCase:
    """Busca un comunicado por su id."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self, comunicado_id: str) -> Comunicado | None:
        """Devuelve el comunicado si existe, o None."""
        return await self._repository.get_by_id(comunicado_id)
