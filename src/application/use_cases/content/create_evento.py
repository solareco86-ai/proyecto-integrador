"""Caso de uso para crear un evento."""

from src.application.dtos.content_management_dto import CrearEventoInput
from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class CreateEventoUseCase:
    """Crea un evento nuevo y lo persiste."""

    def __init__(self, repository: EventoRepository) -> None:
        self._repository = repository

    async def execute(self, input: CrearEventoInput) -> Evento:
        """Crea la entidad Evento y la guarda en el repositorio."""
        evento = Evento.create(
            titulo=input.titulo,
            descripcion=input.descripcion,
            fecha_evento=input.fecha_evento,
            lugar=input.lugar,
            autor_id=input.autor_id,
        )
        await self._repository.save(evento)
        return evento
