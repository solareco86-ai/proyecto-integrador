"""Caso de uso para obtener una noticia por su slug."""

from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository


class GetNoticiaBySlugUseCase:
    """Busca una noticia por su slug."""

    def __init__(self, repository: NoticiaRepository) -> None:
        self._repository = repository

    async def execute(self, slug: str) -> Noticia | None:
        """Devuelve la noticia si existe, o None."""
        return await self._repository.get_by_slug(slug)
