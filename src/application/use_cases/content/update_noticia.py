"""Caso de uso para editar una noticia existente."""

from dataclasses import replace
from datetime import UTC, datetime

from src.application.dtos.content_management_dto import EditarNoticiaInput
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository


class UpdateNoticiaUseCase:
    """Edita una noticia existente. Lanza EntityNotFoundError si no existe."""

    def __init__(self, repository: NoticiaRepository) -> None:
        self._repository = repository

    async def execute(self, input: EditarNoticiaInput) -> Noticia:
        """Busca la noticia, aplica los cambios y persiste la actualización."""
        existente = await self._repository.get_by_id(input.id)
        if existente is None:
            raise EntityNotFoundError(f"Noticia {input.id} no encontrada")

        actualizada = replace(
            existente,
            titulo=input.titulo,
            cuerpo=input.cuerpo,
            publicada=input.publicada,
            updated_at=datetime.now(UTC).isoformat(),
        )
        await self._repository.update(actualizada)
        return actualizada
