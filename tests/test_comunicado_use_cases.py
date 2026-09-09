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
