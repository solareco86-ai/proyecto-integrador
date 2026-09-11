"""Caso de uso para obtener un comunicado por su slug."""

from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class GetComunicadoBySlugUseCase:
    """Busca un comunicado por su slug."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self, slug: str) -> Comunicado | None:
        """Devuelve el comunicado si existe, o None."""
        return await self._repository.get_by_slug(slug)
