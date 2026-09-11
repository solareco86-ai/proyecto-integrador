"""Tests unitarios de los use cases de Evento (CRUD), sin base de datos real."""

import pytest

from src.application.dtos.content_management_dto import CrearEventoInput, EditarEventoInput
from src.application.use_cases.content.create_evento import CreateEventoUseCase
from src.application.use_cases.content.delete_evento import DeleteEventoUseCase
from src.application.use_cases.content.get_evento import GetEventoUseCase
from src.application.use_cases.content.get_evento_by_slug import GetEventoBySlugUseCase
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

    async def get_by_slug(self, slug: str) -> Evento | None:
        return next((x for x in self.data.values() if x.slug == slug), None)

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


# --- Slug (5A) ---


@pytest.mark.asyncio
async def test_create_evento_genera_slug_a_partir_del_titulo():
    repo = InMemoryEventoRepo()
    evento = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(titulo="Acto de Fin de Año", descripcion="Descripción", fecha_evento="2026-12-15T18:00:00")
    )

    assert evento.slug == "acto-de-fin-de-ano"


@pytest.mark.asyncio
async def test_create_evento_resuelve_colision_de_slug_con_sufijo():
    repo = InMemoryEventoRepo()
    use_case = CreateEventoUseCase(repository=repo)
    primero = await use_case.execute(
        CrearEventoInput(titulo="Jornada Abierta", descripcion="D1", fecha_evento="2026-01-01T10:00:00")
    )
    segundo = await use_case.execute(
        CrearEventoInput(titulo="Jornada Abierta", descripcion="D2", fecha_evento="2026-02-01T10:00:00")
    )

    assert primero.slug == "jornada-abierta"
    assert segundo.slug == "jornada-abierta-2"


@pytest.mark.asyncio
async def test_update_evento_regenera_slug_si_cambia_el_titulo():
    repo = InMemoryEventoRepo()
    creado = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(titulo="Original", descripcion="X", fecha_evento="2026-01-01T10:00:00")
    )

    actualizado = await UpdateEventoUseCase(repository=repo).execute(
        EditarEventoInput(id=creado.id, titulo="Título Nuevo", descripcion="X", fecha_evento="2026-01-01T10:00:00")
    )

    assert actualizado.slug == "titulo-nuevo"


@pytest.mark.asyncio
async def test_update_evento_mantiene_slug_si_el_titulo_no_cambia():
    repo = InMemoryEventoRepo()
    creado = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(titulo="Original", descripcion="X", fecha_evento="2026-01-01T10:00:00")
    )
    slug_original = creado.slug

    actualizado = await UpdateEventoUseCase(repository=repo).execute(
        EditarEventoInput(id=creado.id, titulo="Original", descripcion="Y", fecha_evento="2026-01-01T10:00:00")
    )

    assert actualizado.slug == slug_original


@pytest.mark.asyncio
async def test_update_evento_resuelve_colision_de_slug_excluyendose_a_si_mismo():
    repo = InMemoryEventoRepo()
    use_case_create = CreateEventoUseCase(repository=repo)
    otro = await use_case_create.execute(
        CrearEventoInput(titulo="Evento Existente", descripcion="A", fecha_evento="2026-01-01T10:00:00")
    )
    propio = await use_case_create.execute(
        CrearEventoInput(titulo="Otro Título", descripcion="B", fecha_evento="2026-02-01T10:00:00")
    )

    actualizado = await UpdateEventoUseCase(repository=repo).execute(
        EditarEventoInput(
            id=propio.id, titulo="Evento Existente", descripcion="B", fecha_evento="2026-02-01T10:00:00"
        )
    )

    assert actualizado.slug == "evento-existente-2"
    assert repo.data[otro.id].slug == "evento-existente"


# --- Publicado/a (5B) ---


@pytest.mark.asyncio
async def test_create_evento_no_publicado_por_defecto():
    repo = InMemoryEventoRepo()
    evento = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(titulo="Acto", descripcion="Descripción", fecha_evento="2026-12-15T18:00:00")
    )

    assert evento.publicada is False


@pytest.mark.asyncio
async def test_create_evento_publicado_explicito():
    repo = InMemoryEventoRepo()
    evento = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(
            titulo="Acto", descripcion="Descripción", fecha_evento="2026-12-15T18:00:00", publicada=True
        )
    )

    assert evento.publicada is True


@pytest.mark.asyncio
async def test_update_evento_permite_cambiar_publicada_a_true():
    repo = InMemoryEventoRepo()
    creado = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(titulo="Original", descripcion="X", fecha_evento="2026-01-01T10:00:00")
    )
    assert creado.publicada is False

    actualizado = await UpdateEventoUseCase(repository=repo).execute(
        EditarEventoInput(
            id=creado.id,
            titulo="Original",
            descripcion="X",
            fecha_evento="2026-01-01T10:00:00",
            publicada=True,
        )
    )

    assert actualizado.publicada is True
    assert repo.data[creado.id].publicada is True


@pytest.mark.asyncio
async def test_update_evento_permite_cambiar_publicada_a_false():
    repo = InMemoryEventoRepo()
    creado = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(
            titulo="Original", descripcion="X", fecha_evento="2026-01-01T10:00:00", publicada=True
        )
    )

    actualizado = await UpdateEventoUseCase(repository=repo).execute(
        EditarEventoInput(
            id=creado.id,
            titulo="Original",
            descripcion="X",
            fecha_evento="2026-01-01T10:00:00",
            publicada=False,
        )
    )

    assert actualizado.publicada is False


@pytest.mark.asyncio
async def test_list_eventos_conserva_estado_publicada():
    repo = InMemoryEventoRepo()
    create = CreateEventoUseCase(repository=repo)
    await create.execute(
        CrearEventoInput(titulo="Publicado", descripcion="D1", fecha_evento="2026-01-01T10:00:00", publicada=True)
    )
    await create.execute(CrearEventoInput(titulo="Borrador", descripcion="D2", fecha_evento="2026-02-01T10:00:00"))

    listado = await ListEventosUseCase(repository=repo).execute()

    estados = {e.titulo: e.publicada for e in listado}
    assert estados["Publicado"] is True
    assert estados["Borrador"] is False


@pytest.mark.asyncio
async def test_persistencia_guarda_y_recupera_publicada_correctamente():
    repo = InMemoryEventoRepo()
    creado = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(
            titulo="Acto", descripcion="Descripción", fecha_evento="2026-12-15T18:00:00", publicada=True
        )
    )

    recuperado = await GetEventoUseCase(repository=repo).execute(creado.id)

    assert recuperado is not None
    assert recuperado.publicada is True


# --- Página pública de Eventos (5D) ---


@pytest.mark.asyncio
async def test_get_evento_by_slug_devuelve_la_entidad():
    repo = InMemoryEventoRepo()
    creado = await CreateEventoUseCase(repository=repo).execute(
        CrearEventoInput(titulo="Acto", descripcion="Descripción", fecha_evento="2026-12-15T18:00:00")
    )

    encontrado = await GetEventoBySlugUseCase(repository=repo).execute(creado.slug)

    assert encontrado == creado


@pytest.mark.asyncio
async def test_get_evento_by_slug_devuelve_none_si_no_existe():
    repo = InMemoryEventoRepo()

    assert await GetEventoBySlugUseCase(repository=repo).execute("no-existe") is None
