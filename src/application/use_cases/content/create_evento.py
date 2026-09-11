"""Caso de uso para crear un evento."""

from dataclasses import replace

from src.application.dtos.content_management_dto import CrearEventoInput
from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class CreateEventoUseCase:
    """Crea un evento nuevo y lo persiste."""

    def __init__(self, repository: EventoRepository) -> None:
        self._repository = repository

    async def execute(self, input: CrearEventoInput) -> Evento:
        """Crea la entidad Evento (con su slug base) y la guarda, resolviendo colisiones de slug."""
        evento = Evento.create(
            titulo=input.titulo,
            descripcion=input.descripcion,
            fecha_evento=input.fecha_evento,
            lugar=input.lugar,
            autor_id=input.autor_id,
        )
        slug_unico = await self._resolver_slug_unico(evento.slug)
        if slug_unico != evento.slug:
            evento = replace(evento, slug=slug_unico)
        await self._repository.save(evento)
        return evento

    async def _resolver_slug_unico(self, slug_base: str | None) -> str | None:
        """Agrega un sufijo numérico si el slug base ya está en uso."""
        if slug_base is None:
            return None
        candidato = slug_base
        contador = 2
        while await self._repository.get_by_slug(candidato) is not None:
            candidato = f"{slug_base}-{contador}"
            contador += 1
        return candidato
