"""Tests de integración HTTP de las rutas públicas /noticias (5C), sin base de datos real."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.content.entities import Noticia
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_noticia_repository


class InMemoryNoticiaRepo(NoticiaRepository):
    def __init__(self, noticias: list[Noticia] | None = None) -> None:
        self.data: dict[str, Noticia] = {n.id: n for n in (noticias or [])}

    async def save(self, noticia: Noticia) -> None:
        self.data[noticia.id] = noticia

    async def get_by_id(self, noticia_id: str) -> Noticia | None:
        return self.data.get(noticia_id)

    async def get_by_slug(self, slug: str) -> Noticia | None:
        return next((x for x in self.data.values() if x.slug == slug), None)

    async def list_all(self) -> list[Noticia]:
        return list(self.data.values())

    async def update(self, noticia: Noticia) -> None:
        self.data[noticia.id] = noticia

    async def delete(self, noticia_id: str) -> None:
        self.data.pop(noticia_id, None)


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


def _configurar(repo: InMemoryNoticiaRepo) -> None:
    app.dependency_overrides[get_noticia_repository] = lambda: repo


# --- Listado ---


@pytest.mark.asyncio
async def test_listado_responde_200():
    _configurar(InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/noticias")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_listado_muestra_solo_noticias_publicadas():
    publicada = Noticia.create(titulo="Noticia publicada", cuerpo="Cuerpo público", publicada=True)
    borrador = Noticia.create(titulo="Noticia en borrador", cuerpo="Cuerpo sin publicar", publicada=False)
    _configurar(InMemoryNoticiaRepo([publicada, borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/noticias")

    assert response.status_code == 200
    assert "Noticia publicada" in response.text
    assert "Noticia en borrador" not in response.text


@pytest.mark.asyncio
async def test_noticia_publicada_aparece_en_el_listado():
    publicada = Noticia.create(titulo="Acto institucional", cuerpo="Cuerpo", publicada=True)
    _configurar(InMemoryNoticiaRepo([publicada]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/noticias")

    assert "Acto institucional" in response.text


@pytest.mark.asyncio
async def test_noticia_no_publicada_no_aparece_en_el_listado():
    borrador = Noticia.create(titulo="Todavia sin publicar", cuerpo="Cuerpo", publicada=False)
    _configurar(InMemoryNoticiaRepo([borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/noticias")

    assert "Todavia sin publicar" not in response.text


@pytest.mark.asyncio
async def test_listado_vacio_muestra_mensaje_sin_romper():
    _configurar(InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/noticias")

    assert response.status_code == 200
    assert "Todavía no hay noticias publicadas" in response.text


# --- Detalle por slug ---


@pytest.mark.asyncio
async def test_detalle_por_slug_responde_200_y_muestra_contenido():
    noticia = Noticia.create(titulo="Inscripción 2027", cuerpo="Cuerpo completo de la noticia", publicada=True)
    _configurar(InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/noticias/{noticia.slug}")

    assert response.status_code == 200
    assert "Inscripción 2027" in response.text
    assert "Cuerpo completo de la noticia" in response.text


@pytest.mark.asyncio
async def test_detalle_slug_inexistente_devuelve_404():
    _configurar(InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/noticias/no-existe")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_detalle_noticia_no_publicada_devuelve_404():
    borrador = Noticia.create(titulo="Aviso interno", cuerpo="Cuerpo", publicada=False)
    _configurar(InMemoryNoticiaRepo([borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/noticias/{borrador.slug}")

    assert response.status_code == 404
    assert "Aviso interno" not in response.text


@pytest.mark.asyncio
async def test_detalle_no_expone_autor_id():
    noticia = Noticia.create(
        titulo="Noticia con autor", cuerpo="Cuerpo", autor_id="autor-secreto-123", publicada=True
    )
    _configurar(InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/noticias/{noticia.slug}")

    assert "autor-secreto-123" not in response.text


# --- SEO / JSON-LD ---


@pytest.mark.asyncio
async def test_detalle_incluye_json_ld_newsarticle():
    noticia = Noticia.create(titulo="Noticia con SEO", cuerpo="Cuerpo", publicada=True)
    _configurar(InMemoryNoticiaRepo([noticia]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/noticias/{noticia.slug}")

    assert response.status_code == 200
    assert '"@type": "NewsArticle"' in response.text
    assert "<title>Noticia con SEO" in response.text


@pytest.mark.asyncio
async def test_listado_incluye_canonical_y_title():
    _configurar(InMemoryNoticiaRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/noticias")

    assert response.status_code == 200
    assert "<title>Noticias" in response.text
    assert "rel='canonical'" in response.text
