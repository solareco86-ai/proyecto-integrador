"""Caso de uso para editar un evento existente."""

from dataclasses import replace
from datetime import UTC, datetime

from src.application.dtos.content_management_dto import EditarEventoInput
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class UpdateEventoUseCase:
    """Edita un evento existente. Lanza EntityNotFoundError si no existe."""

    def __init__(self, repository: EventoRepository) -> None:
        self._repository = repository

    async def execute(self, input: EditarEventoInput) -> Evento:
        """Busca el evento, aplica los cambios y persiste la actualización."""
        existente = await self._repository.get_by_id(input.id)
        if existente is None:
            raise EntityNotFoundError(f"Evento {input.id} no encontrado")

        actualizado = replace(
            existente,
            titulo=input.titulo,
            descripcion=input.descripcion,
            fecha_evento=input.fecha_evento,
            lugar=input.lugar,
            updated_at=datetime.now(UTC).isoformat(),
        )
        await self._repository.update(actualizado)
        return actualizado
