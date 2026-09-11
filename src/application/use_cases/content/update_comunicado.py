"""Caso de uso para editar un comunicado existente."""

from dataclasses import replace
from datetime import UTC, datetime

from src.application.dtos.content_management_dto import EditarComunicadoInput
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.common.slugify import slugify
from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class UpdateComunicadoUseCase:
    """Edita un comunicado existente. Lanza EntityNotFoundError si no existe."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self, input: EditarComunicadoInput) -> Comunicado:
        """Busca el comunicado, aplica los cambios y persiste la actualización.

        El slug no es editable directamente: se regenera a partir del nuevo
        título solo cuando el título cambia, resolviendo colisiones contra
        otros registros (excluyéndose a sí mismo).
        """
        existente = await self._repository.get_by_id(input.id)
        if existente is None:
            raise EntityNotFoundError(f"Comunicado {input.id} no encontrado")

        slug = existente.slug
        if input.titulo != existente.titulo:
            slug = await self._resolver_slug_unico(slugify(input.titulo), excluir_id=existente.id)

        actualizado = replace(
            existente,
            titulo=input.titulo,
            cuerpo=input.cuerpo,
            publicada=input.publicada,
            slug=slug,
            updated_at=datetime.now(UTC).isoformat(),
        )
        await self._repository.update(actualizado)
        return actualizado

    async def _resolver_slug_unico(self, slug_base: str, excluir_id: str) -> str:
        """Agrega un sufijo numérico si el slug base ya está en uso por otro registro."""
        candidato = slug_base
        contador = 2
        while True:
            existente = await self._repository.get_by_slug(candidato)
            if existente is None or existente.id == excluir_id:
                return candidato
            candidato = f"{slug_base}-{contador}"
            contador += 1
