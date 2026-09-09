"""Tests unitarios de los use cases de Noticia (CRUD), sin base de datos real."""

import pytest

from src.application.dtos.content_management_dto import CrearNoticiaInput, EditarNoticiaInput
from src.application.use_cases.content.create_noticia import CreateNoticiaUseCase
from src.application.use_cases.content.delete_noticia import DeleteNoticiaUseCase
from src.application.use_cases.content.get_noticia import GetNoticiaUseCase
from src.application.use_cases.content.list_noticias import ListNoticiasUseCase
from src.application.use_cases.content.update_noticia import UpdateNoticiaUseCase
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository


class InMemoryNoticiaRepo(NoticiaRepository):
    def __init__(self) -> None:
        self.data: dict[str, Noticia] = {}

    async def save(self, noticia: Noticia) -> None:
        self.data[noticia.id] = noticia

    async def get_by_id(self, noticia_id: str) -> Noticia | None:
        return self.data.get(noticia_id)

    async def list_all(self) -> list[Noticia]:
        return list(self.data.values())

    async def update(self, noticia: Noticia) -> None:
        self.data[noticia.id] = noticia

    async def delete(self, noticia_id: str) -> None:
        self.data.pop(noticia_id, None)


@pytest.mark.asyncio
async def test_create_noticia_persiste_y_devuelve_entidad():
    repo = InMemoryNoticiaRepo()
    use_case = CreateNoticiaUseCase(repository=repo)

    noticia = await use_case.execute(CrearNoticiaInput(titulo="Título", cuerpo="Cuerpo"))

    assert noticia.titulo == "Título"
    assert noticia.publicada is True
    assert noticia.id in repo.data


@pytest.mark.asyncio
async def test_create_noticia_admite_borrador():
    repo = InMemoryNoticiaRepo()
    use_case = CreateNoticiaUseCase(repository=repo)

    noticia = await use_case.execute(CrearNoticiaInput(titulo="Título", cuerpo="Cuerpo", publicada=False))

    assert noticia.publicada is False


@pytest.mark.asyncio
async def test_get_noticia_devuelve_none_si_no_existe():
    repo = InMemoryNoticiaRepo()
    use_case = GetNoticiaUseCase(repository=repo)

    assert await use_case.execute("no-existe") is None


@pytest.mark.asyncio
async def test_get_noticia_devuelve_entidad_existente():
    repo = InMemoryNoticiaRepo()
    creada = await CreateNoticiaUseCase(repository=repo).execute(CrearNoticiaInput(titulo="A", cuerpo="B"))

    encontrada = await GetNoticiaUseCase(repository=repo).execute(creada.id)

    assert encontrada == creada


@pytest.mark.asyncio
async def test_list_noticias_devuelve_todas():
    repo = InMemoryNoticiaRepo()
    use_case_create = CreateNoticiaUseCase(repository=repo)
    await use_case_create.execute(CrearNoticiaInput(titulo="Uno", cuerpo="Cuerpo 1"))
    await use_case_create.execute(CrearNoticiaInput(titulo="Dos", cuerpo="Cuerpo 2"))

    listado = await ListNoticiasUseCase(repository=repo).execute()

    assert len(listado) == 2


@pytest.mark.asyncio
async def test_update_noticia_aplica_cambios():
    repo = InMemoryNoticiaRepo()
    creada = await CreateNoticiaUseCase(repository=repo).execute(CrearNoticiaInput(titulo="Original", cuerpo="X"))

    actualizada = await UpdateNoticiaUseCase(repository=repo).execute(
        EditarNoticiaInput(id=creada.id, titulo="Editado", cuerpo="Y", publicada=False)
    )

    assert actualizada.titulo == "Editado"
    assert actualizada.cuerpo == "Y"
    assert actualizada.publicada is False
    assert actualizada.updated_at is not None
    assert repo.data[creada.id].titulo == "Editado"


@pytest.mark.asyncio
async def test_update_noticia_inexistente_lanza_error():
    repo = InMemoryNoticiaRepo()
    use_case = UpdateNoticiaUseCase(repository=repo)

    with pytest.raises(EntityNotFoundError):
        await use_case.execute(EditarNoticiaInput(id="no-existe", titulo="X", cuerpo="Y"))


@pytest.mark.asyncio
async def test_delete_noticia_elimina_existente():
    repo = InMemoryNoticiaRepo()
    creada = await CreateNoticiaUseCase(repository=repo).execute(CrearNoticiaInput(titulo="A", cuerpo="B"))

    await DeleteNoticiaUseCase(repository=repo).execute(creada.id)

    assert creada.id not in repo.data


@pytest.mark.asyncio
async def test_delete_noticia_es_idempotente():
    repo = InMemoryNoticiaRepo()
    use_case = DeleteNoticiaUseCase(repository=repo)

    # No debe lanzar excepción aunque el id no exista
    await use_case.execute("no-existe")
