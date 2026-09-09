"""Tests unitarios de los use cases de Evento (CRUD), sin base de datos real."""

import pytest

from src.application.dtos.content_management_dto import CrearEventoInput, EditarEventoInput
from src.application.use_cases.content.create_evento import CreateEventoUseCase
from src.application.use_cases.content.delete_evento import DeleteEventoUseCase
from src.application.use_cases.content.get_evento import GetEventoUseCase
from src.application.use_cases.content.list_eventos import ListEventosUseCase
from src.application.use_cases.content.update_evento import UpdateEventoUseCase
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository


class InMemoryEventoRepo(EventoRepository):
    def __init__(self) -> None:
        self.data: dict[str, Evento] = {}

    async def save(self, evento: Evento) -> None:
        self.data[evento.id] = evento

    async def get_by_id(self, evento_id: str) -> Evento | None:
        return self.data.get(evento_id)

    async def list_all(self) -> list[Evento]:
        return list(self.data.values())

    async def update(self, evento: Evento) -> None:
        self.data[evento.id] = evento

    async def delete(self, evento_id: str) -> None:
        self.data.pop(evento_id, None)


@pytest.mark.asyncio
async def test_create_evento_persiste_y_devuelve_entidad():
    repo = InMemoryEventoRepo()
    use_case = CreateEventoUseCase(repository=repo)

    evento = await use_case.execute(
        CrearEventoInput(titulo="Acto", descripcion="Acto de fin de año", fecha_evento="2026-12-15T18:00:00")
    )

    assert evento.titulo == "Acto"
    assert evento.id in repo.data


@pytest.mark.asyncio
async def test_get_evento_devuelve_none_si_no_existe():
    repo = InMemoryEventoRepo()
    assert await GetEventoUseCase(repository=repo).execute("no-existe") is None


@pytest.mark.asyncio
async def test_list_eventos_devuelve_todos():
    repo = InMemoryEventoRepo()
    create = CreateEventoUseCase(repository=repo)
    await create.execute(CrearEventoInput(titulo="A", descripcion="D1", fecha_evento="2026-01-01T10:00:00"))
    await create.execute(CrearEventoInput(titulo="B", descripcion="D2", fecha_evento="2026-02-01T10:00:00"))

    listado = await ListEventosUseCase(repository=repo).execute()

    assert len(listado) == 2


@pytest.mark.asyncio
async def test_update_evento_aplica_cambios():
    repo = InMemoryEventoRepo()
    creado = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(titulo="Original", descripcion="X", fecha_evento="2026-01-01T10:00:00")
    )

    actualizado = await UpdateEventoUseCase(repository=repo).execute(
        EditarEventoInput(
            id=creado.id,
            titulo="Editado",
            descripcion="Y",
            fecha_evento="2026-03-01T10:00:00",
            lugar="Auditorio",
        )
    )

    assert actualizado.titulo == "Editado"
    assert actualizado.lugar == "Auditorio"
    assert actualizado.updated_at is not None


@pytest.mark.asyncio
async def test_update_evento_inexistente_lanza_error():
    repo = InMemoryEventoRepo()
    with pytest.raises(EntityNotFoundError):
        await UpdateEventoUseCase(repository=repo).execute(
            EditarEventoInput(id="no-existe", titulo="X", descripcion="Y", fecha_evento="2026-01-01T10:00:00")
        )


@pytest.mark.asyncio
async def test_delete_evento_es_idempotente():
    repo = InMemoryEventoRepo()
    # No debe lanzar excepción aunque el id no exista
    await DeleteEventoUseCase(repository=repo).execute("no-existe")
