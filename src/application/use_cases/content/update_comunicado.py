"""Caso de uso para editar un comunicado existente."""

from dataclasses import replace
from datetime import UTC, datetime

from src.application.dtos.content_management_dto import EditarComunicadoInput
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class UpdateComunicadoUseCase:
    """Edita un comunicado existente. Lanza EntityNotFoundError si no existe."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self, input: EditarComunicadoInput) -> Comunicado:
        """Busca el comunicado, aplica los cambios y persiste la actualización."""
        existente = await self._repository.get_by_id(input.id)
        if existente is None:
            raise EntityNotFoundError(f"Comunicado {input.id} no encontrado")

        actualizado = replace(
            existente,
            titulo=input.titulo,
            cuerpo=input.cuerpo,
            updated_at=datetime.now(UTC).isoformat(),
        )
        await self._repository.update(actualizado)
        return actualizado
