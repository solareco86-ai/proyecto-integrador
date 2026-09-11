"""Tests unitarios de los use cases de Comunicado (CRUD), sin base de datos real."""

import pytest

from src.application.dtos.content_management_dto import CrearComunicadoInput, EditarComunicadoInput
from src.application.use_cases.content.create_comunicado import CreateComunicadoUseCase
from src.application.use_cases.content.delete_comunicado import DeleteComunicadoUseCase
from src.application.use_cases.content.get_comunicado import GetComunicadoUseCase
from src.application.use_cases.content.list_comunicados import ListComunicadosUseCase
from src.application.use_cases.content.update_comunicado import UpdateComunicadoUseCase
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository


class InMemoryComunicadoRepo(ComunicadoRepository):
    def __init__(self) -> None:
        self.data: dict[str, Comunicado] = {}

    async def save(self, comunicado: Comunicado) -> None:
        self.data[comunicado.id] = comunicado

    async def get_by_id(self, comunicado_id: str) -> Comunicado | None:
        return self.data.get(comunicado_id)

    async def get_by_slug(self, slug: str) -> Comunicado | None:
        return next((x for x in self.data.values() if x.slug == slug), None)

    async def list_all(self) -> list[Comunicado]:
        return list(self.data.values())

    async def update(self, comunicado: Comunicado) -> None:
        self.data[comunicado.id] = comunicado

    async def delete(self, comunicado_id: str) -> None:
        self.data.pop(comunicado_id, None)


@pytest.mark.asyncio
async def test_create_comunicado_persiste_y_devuelve_entidad():
    repo = InMemoryComunicadoRepo()
    comunicado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Aviso", cuerpo="Contenido del aviso")
    )

    assert comunicado.titulo == "Aviso"
    assert comunicado.id in repo.data


@pytest.mark.asyncio
async def test_get_comunicado_devuelve_none_si_no_existe():
    repo = InMemoryComunicadoRepo()
    assert await GetComunicadoUseCase(repository=repo).execute("no-existe") is None


@pytest.mark.asyncio
async def test_list_comunicados_devuelve_todos():
    repo = InMemoryComunicadoRepo()
    create = CreateComunicadoUseCase(repository=repo)
    await create.execute(CrearComunicadoInput(titulo="A", cuerpo="1"))
    await create.execute(CrearComunicadoInput(titulo="B", cuerpo="2"))

    listado = await ListComunicadosUseCase(repository=repo).execute()

    assert len(listado) == 2


@pytest.mark.asyncio
async def test_update_comunicado_aplica_cambios():
    repo = InMemoryComunicadoRepo()
    creado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Original", cuerpo="X")
    )

    actualizado = await UpdateComunicadoUseCase(repository=repo).execute(
        EditarComunicadoInput(id=creado.id, titulo="Editado", cuerpo="Y")
    )

    assert actualizado.titulo == "Editado"
    assert actualizado.cuerpo == "Y"
    assert actualizado.updated_at is not None


@pytest.mark.asyncio
async def test_update_comunicado_inexistente_lanza_error():
    repo = InMemoryComunicadoRepo()
    with pytest.raises(EntityNotFoundError):
        await UpdateComunicadoUseCase(repository=repo).execute(
            EditarComunicadoInput(id="no-existe", titulo="X", cuerpo="Y")
        )


@pytest.mark.asyncio
async def test_delete_comunicado_es_idempotente():
    repo = InMemoryComunicadoRepo()
    # No debe lanzar excepción aunque el id no exista
    await DeleteComunicadoUseCase(repository=repo).execute("no-existe")


# --- Slug (5A) ---


@pytest.mark.asyncio
async def test_create_comunicado_genera_slug_a_partir_del_titulo():
    repo = InMemoryComunicadoRepo()
    comunicado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Aviso Importante", cuerpo="Cuerpo")
    )

    assert comunicado.slug == "aviso-importante"


@pytest.mark.asyncio
async def test_create_comunicado_resuelve_colision_de_slug_con_sufijo():
    repo = InMemoryComunicadoRepo()
    use_case = CreateComunicadoUseCase(repository=repo)
    primero = await use_case.execute(CrearComunicadoInput(titulo="Aviso General", cuerpo="1"))
    segundo = await use_case.execute(CrearComunicadoInput(titulo="Aviso General", cuerpo="2"))

    assert primero.slug == "aviso-general"
    assert segundo.slug == "aviso-general-2"


@pytest.mark.asyncio
async def test_update_comunicado_regenera_slug_si_cambia_el_titulo():
    repo = InMemoryComunicadoRepo()
    creado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Original", cuerpo="X")
    )

    actualizado = await UpdateComunicadoUseCase(repository=repo).execute(
        EditarComunicadoInput(id=creado.id, titulo="Título Nuevo", cuerpo="X")
    )

    assert actualizado.slug == "titulo-nuevo"


@pytest.mark.asyncio
async def test_update_comunicado_mantiene_slug_si_el_titulo_no_cambia():
    repo = InMemoryComunicadoRepo()
    creado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Original", cuerpo="X")
    )
    slug_original = creado.slug

    actualizado = await UpdateComunicadoUseCase(repository=repo).execute(
        EditarComunicadoInput(id=creado.id, titulo="Original", cuerpo="Cuerpo editado")
    )

    assert actualizado.slug == slug_original


@pytest.mark.asyncio
async def test_update_comunicado_resuelve_colision_de_slug_excluyendose_a_si_mismo():
    repo = InMemoryComunicadoRepo()
    use_case_create = CreateComunicadoUseCase(repository=repo)
    otro = await use_case_create.execute(CrearComunicadoInput(titulo="Comunicado Existente", cuerpo="A"))
    propio = await use_case_create.execute(CrearComunicadoInput(titulo="Otro Título", cuerpo="B"))

    actualizado = await UpdateComunicadoUseCase(repository=repo).execute(
        EditarComunicadoInput(id=propio.id, titulo="Comunicado Existente", cuerpo="B")
    )

    assert actualizado.slug == "comunicado-existente-2"
    assert repo.data[otro.id].slug == "comunicado-existente"


# --- Publicado/a (5B) ---


@pytest.mark.asyncio
async def test_create_comunicado_no_publicado_por_defecto():
    repo = InMemoryComunicadoRepo()
    comunicado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Aviso", cuerpo="Contenido")
    )

    assert comunicado.publicada is False


@pytest.mark.asyncio
async def test_create_comunicado_publicado_explicito():
    repo = InMemoryComunicadoRepo()
    comunicado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Aviso", cuerpo="Contenido", publicada=True)
    )

    assert comunicado.publicada is True


@pytest.mark.asyncio
async def test_update_comunicado_permite_cambiar_publicada_a_true():
    repo = InMemoryComunicadoRepo()
    creado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Original", cuerpo="X")
    )
    assert creado.publicada is False

    actualizado = await UpdateComunicadoUseCase(repository=repo).execute(
        EditarComunicadoInput(id=creado.id, titulo="Original", cuerpo="X", publicada=True)
    )

    assert actualizado.publicada is True
    assert repo.data[creado.id].publicada is True


@pytest.mark.asyncio
async def test_update_comunicado_permite_cambiar_publicada_a_false():
    repo = InMemoryComunicadoRepo()
    creado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Original", cuerpo="X", publicada=True)
    )

    actualizado = await UpdateComunicadoUseCase(repository=repo).execute(
        EditarComunicadoInput(id=creado.id, titulo="Original", cuerpo="X", publicada=False)
    )

    assert actualizado.publicada is False


@pytest.mark.asyncio
async def test_list_comunicados_conserva_estado_publicada():
    repo = InMemoryComunicadoRepo()
    create = CreateComunicadoUseCase(repository=repo)
    await create.execute(CrearComunicadoInput(titulo="Publicado", cuerpo="1", publicada=True))
    await create.execute(CrearComunicadoInput(titulo="Borrador", cuerpo="2"))

    listado = await ListComunicadosUseCase(repository=repo).execute()

    estados = {c.titulo: c.publicada for c in listado}
    assert estados["Publicado"] is True
    assert estados["Borrador"] is False


@pytest.mark.asyncio
async def test_persistencia_guarda_y_recupera_publicada_correctamente():
    repo = InMemoryComunicadoRepo()
    creado = await CreateComunicadoUseCase(repository=repo).execute(
        CrearComunicadoInput(titulo="Aviso", cuerpo="Contenido", publicada=True)
    )

    recuperado = await GetComunicadoUseCase(repository=repo).execute(creado.id)

    assert recuperado is not None
    assert recuperado.publicada is True
