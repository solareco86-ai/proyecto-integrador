"""Caso de uso para obtener una noticia por id."""

from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository


class GetNoticiaUseCase:
    """Busca una noticia por su id."""

    def __init__(self, repository: NoticiaRepository) -> None:
        self._repository = repository

    async def execute(self, noticia_id: str) -> Noticia | None:
        """Devuelve la noticia si existe, o None."""
        return await self._repository.get_by_id(noticia_id)
