"""Caso de uso para crear un comunicado."""

from dataclasses import replace

from src.application.dtos.content_management_dto import CrearComunicadoInput
from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class CreateComunicadoUseCase:
    """Crea un comunicado nuevo y lo persiste."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self, input: CrearComunicadoInput) -> Comunicado:
        """Crea la entidad Comunicado (con su slug base) y la guarda, resolviendo colisiones de slug."""
        comunicado = Comunicado.create(
            titulo=input.titulo,
            cuerpo=input.cuerpo,
            autor_id=input.autor_id,
        )
        slug_unico = await self._resolver_slug_unico(comunicado.slug)
        if slug_unico != comunicado.slug:
            comunicado = replace(comunicado, slug=slug_unico)
        await self._repository.save(comunicado)
        return comunicado

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
