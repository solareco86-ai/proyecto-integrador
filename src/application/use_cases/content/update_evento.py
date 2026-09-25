"""Caso de uso para editar un evento existente."""

from dataclasses import replace
from datetime import UTC, datetime

from src.application.dtos.content_management_dto import EditarEventoInput
from src.application.gateways.image_storage_gateway import ImageStorageGateway
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.common.slugify import slugify
from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class UpdateEventoUseCase:
    """Edita un evento existente. Lanza EntityNotFoundError si no existe."""

    def __init__(self, repository: EventoRepository, image_gateway: ImageStorageGateway) -> None:
        self._repository = repository
        self._image_gateway = image_gateway

    async def execute(self, input: EditarEventoInput) -> Evento:
        """Busca el evento, aplica los cambios y persiste la actualización.

        El slug no es editable directamente: se regenera a partir del nuevo
        título solo cuando el título cambia, resolviendo colisiones contra
        otros registros (excluyéndose a sí mismo).

        Manejo de imagen: `input.imagen` (una ruta ya guardada por
        `ImageStorageGateway`, responsabilidad de la ruta HTTP) reemplaza la
        imagen actual; `input.quitar_imagen` la quita explícitamente; si
        ninguna de las dos se indica, la imagen existente se conserva. El
        archivo anterior solo se elimina físicamente *después* de persistir
        con éxito la actualización, para no perder ambas imágenes si algo
        falla a mitad de camino.
        """
        existente = await self._repository.get_by_id(input.id)
        if existente is None:
            raise EntityNotFoundError(f"Evento {input.id} no encontrado")

        slug = existente.slug
        if input.titulo != existente.titulo:
            slug = await self._resolver_slug_unico(slugify(input.titulo), excluir_id=existente.id)

        imagen_anterior = existente.imagen
        if input.quitar_imagen:
            nueva_imagen = None
        elif input.imagen is not None:
            nueva_imagen = input.imagen
        else:
            nueva_imagen = imagen_anterior

        actualizado = replace(
            existente,
            titulo=input.titulo,
            descripcion=input.descripcion,
            fecha_evento=input.fecha_evento,
            lugar=input.lugar,
            publicada=input.publicada,
            slug=slug,
            updated_at=datetime.now(UTC).isoformat(),
            imagen=nueva_imagen,
        )
        await self._repository.update(actualizado)

        if imagen_anterior is not None and imagen_anterior != nueva_imagen:
            await self._image_gateway.delete(imagen_anterior)

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
