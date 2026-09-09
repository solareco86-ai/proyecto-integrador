"""Caso de uso para listar todos los comunicados."""

from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class ListComunicadosUseCase:
    """Devuelve todos los comunicados almacenados."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Comunicado]:
        """Devuelve la lista completa de comunicados."""
        return await self._repository.list_all()
