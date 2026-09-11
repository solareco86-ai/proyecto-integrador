"""Tests de integración HTTP de las rutas públicas /comunicados (5E), sin base de datos real."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.content.entities import Comunicado
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_comunicado_repository


class InMemoryComunicadoRepo(ComunicadoRepository):
    def __init__(self, comunicados: list[Comunicado] | None = None) -> None:
        self.data: dict[str, Comunicado] = {c.id: c for c in (comunicados or [])}

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


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


def _configurar(repo: InMemoryComunicadoRepo) -> None:
    app.dependency_overrides[get_comunicado_repository] = lambda: repo


# --- Listado ---


@pytest.mark.asyncio
async def test_listado_responde_200():
    _configurar(InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/comunicados")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_listado_muestra_solo_comunicados_publicados():
    publicado = Comunicado.create(titulo="Comunicado publicado", cuerpo="Cuerpo público", publicada=True)
    borrador = Comunicado.create(titulo="Comunicado en borrador", cuerpo="Cuerpo sin publicar", publicada=False)
    _configurar(InMemoryComunicadoRepo([publicado, borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/comunicados")

    assert response.status_code == 200
    assert "Comunicado publicado" in response.text
    assert "Comunicado en borrador" not in response.text


@pytest.mark.asyncio
async def test_comunicado_publicado_aparece_en_el_listado():
    publicado = Comunicado.create(titulo="Aviso institucional", cuerpo="Cuerpo", publicada=True)
    _configurar(InMemoryComunicadoRepo([publicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/comunicados")

    assert "Aviso institucional" in response.text


@pytest.mark.asyncio
async def test_comunicado_no_publicado_no_aparece_en_el_listado():
    borrador = Comunicado.create(titulo="Todavia sin publicar", cuerpo="Cuerpo", publicada=False)
    _configurar(InMemoryComunicadoRepo([borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/comunicados")

    assert "Todavia sin publicar" not in response.text


@pytest.mark.asyncio
async def test_listado_vacio_muestra_mensaje_sin_romper():
    _configurar(InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/comunicados")

    assert response.status_code == 200
    assert "Todavía no hay comunicados publicados" in response.text


# --- Detalle por slug ---


@pytest.mark.asyncio
async def test_detalle_por_slug_responde_200_y_muestra_contenido():
    comunicado = Comunicado.create(
        titulo="Aviso de Inscripción", cuerpo="Cuerpo completo del comunicado", publicada=True
    )
    _configurar(InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/comunicados/{comunicado.slug}")

    assert response.status_code == 200
    assert comunicado.slug == "aviso-de-inscripcion"
    assert "Aviso de Inscripción" in response.text
    assert "Cuerpo completo del comunicado" in response.text


@pytest.mark.asyncio
async def test_detalle_slug_inexistente_devuelve_404():
    _configurar(InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/comunicados/no-existe")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_detalle_comunicado_no_publicado_devuelve_404():
    borrador = Comunicado.create(titulo="Aviso interno", cuerpo="Cuerpo", publicada=False)
    _configurar(InMemoryComunicadoRepo([borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/comunicados/{borrador.slug}")

    assert response.status_code == 404
    assert "Aviso interno" not in response.text


@pytest.mark.asyncio
async def test_detalle_no_expone_autor_id():
    comunicado = Comunicado.create(
        titulo="Comunicado con autor", cuerpo="Cuerpo", autor_id="autor-secreto-789", publicada=True
    )
    _configurar(InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/comunicados/{comunicado.slug}")

    assert "autor-secreto-789" not in response.text


# --- SEO / JSON-LD ---


@pytest.mark.asyncio
async def test_detalle_incluye_json_ld_article():
    comunicado = Comunicado.create(titulo="Comunicado con SEO", cuerpo="Cuerpo", publicada=True)
    _configurar(InMemoryComunicadoRepo([comunicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/comunicados/{comunicado.slug}")

    assert response.status_code == 200
    assert '"@type": "Article"' in response.text
    assert "<title>Comunicado con SEO" in response.text


@pytest.mark.asyncio
async def test_listado_incluye_canonical_y_title():
    _configurar(InMemoryComunicadoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/comunicados")

    assert response.status_code == 200
    assert "<title>Comunicados" in response.text
    assert "rel='canonical'" in response.text


# --- Sitemap ---


@pytest.mark.asyncio
async def test_sitemap_incluye_solo_comunicados_publicados():
    publicado = Comunicado.create(titulo="Comunicado publicado en sitemap", cuerpo="Cuerpo", publicada=True)
    borrador = Comunicado.create(titulo="Comunicado borrador en sitemap", cuerpo="Cuerpo", publicada=False)
    _configurar(InMemoryComunicadoRepo([publicado, borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    body = response.text
    assert f"/comunicados/{publicado.slug}" in body
    assert f"/comunicados/{borrador.slug}" not in body
    assert "<loc>" in body and "/comunicados</loc>" in body
