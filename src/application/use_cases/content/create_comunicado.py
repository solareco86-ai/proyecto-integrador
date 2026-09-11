"""Caso de uso para crear un comunicado."""

from src.application.dtos.content_management_dto import CrearComunicadoInput
from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class CreateComunicadoUseCase:
    """Crea un comunicado nuevo y lo persiste."""

    def __init__(self, repository: ComunicadoRepository) -> None:
        self._repository = repository

    async def execute(self, input: CrearComunicadoInput) -> Comunicado:
        """Crea la entidad Comunicado y la guarda en el repositorio."""
        comunicado = Comunicado.create(
            titulo=input.titulo,
            cuerpo=input.cuerpo,
            autor_id=input.autor_id,
        )
        await self._repository.save(comunicado)
        return comunicado
