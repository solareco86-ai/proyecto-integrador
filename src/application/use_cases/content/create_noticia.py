"""Caso de uso para crear una noticia."""

from dataclasses import replace

from src.application.dtos.content_management_dto import CrearNoticiaInput
from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository


class CreateNoticiaUseCase:
    """Crea una noticia nueva y la persiste."""

    def __init__(self, repository: NoticiaRepository) -> None:
        self._repository = repository

    async def execute(self, input: CrearNoticiaInput) -> Noticia:
        """Crea la entidad Noticia (con su slug base) y la guarda, resolviendo colisiones de slug."""
        noticia = Noticia.create(
            titulo=input.titulo,
            cuerpo=input.cuerpo,
            autor_id=input.autor_id,
            publicada=input.publicada,
        )
        slug_unico = await self._resolver_slug_unico(noticia.slug)
        if slug_unico != noticia.slug:
            noticia = replace(noticia, slug=slug_unico)
        await self._repository.save(noticia)
        return noticia

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
