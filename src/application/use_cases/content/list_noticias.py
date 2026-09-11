"""Caso de uso para listar todas las noticias."""

from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository


class ListNoticiasUseCase:
    """Devuelve todas las noticias almacenadas."""

    def __init__(self, repository: NoticiaRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Noticia]:
        """Devuelve la lista completa de noticias."""
        return await self._repository.list_all()
