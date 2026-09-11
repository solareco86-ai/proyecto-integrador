"""Caso de uso para crear una noticia."""

from src.application.dtos.content_management_dto import CrearNoticiaInput
from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository


class CreateNoticiaUseCase:
    """Crea una noticia nueva y la persiste."""

    def __init__(self, repository: NoticiaRepository) -> None:
        self._repository = repository

    async def execute(self, input: CrearNoticiaInput) -> Noticia:
        """Crea la entidad Noticia y la guarda en el repositorio."""
        noticia = Noticia.create(
            titulo=input.titulo,
            cuerpo=input.cuerpo,
            autor_id=input.autor_id,
            publicada=input.publicada,
        )
        await self._repository.save(noticia)
        return noticia
