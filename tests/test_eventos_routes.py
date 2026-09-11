"""Tests de integración HTTP de las rutas públicas /eventos (5D), sin base de datos real."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.content.entities import Evento
from src.domain.content.repositories import EventoRepository
from src.infrastructure.fastapi.app import app
from src.infrastructure.fastapi.dependencies import get_evento_repository


class InMemoryEventoRepo(EventoRepository):
    def __init__(self, eventos: list[Evento] | None = None) -> None:
        self.data: dict[str, Evento] = {e.id: e for e in (eventos or [])}

    async def save(self, evento: Evento) -> None:
        self.data[evento.id] = evento

    async def get_by_id(self, evento_id: str) -> Evento | None:
        return self.data.get(evento_id)

    async def get_by_slug(self, slug: str) -> Evento | None:
        return next((x for x in self.data.values() if x.slug == slug), None)

    async def list_all(self) -> list[Evento]:
        # Mismo criterio que EventoRepositorySQL: ordenado por fecha_evento ASC.
        return sorted(self.data.values(), key=lambda e: e.fecha_evento)

    async def update(self, evento: Evento) -> None:
        self.data[evento.id] = evento

    async def delete(self, evento_id: str) -> None:
        self.data.pop(evento_id, None)


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    yield
    app.dependency_overrides.clear()


def _configurar(repo: InMemoryEventoRepo) -> None:
    app.dependency_overrides[get_evento_repository] = lambda: repo


# --- Listado ---


@pytest.mark.asyncio
async def test_listado_responde_200():
    _configurar(InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_listado_muestra_solo_eventos_publicados():
    publicado = Evento.create(
        titulo="Evento publicado", descripcion="Descripción pública", fecha_evento="2026-12-15T18:00:00", publicada=True
    )
    borrador = Evento.create(
        titulo="Evento en borrador", descripcion="Descripción interna", fecha_evento="2026-12-20T18:00:00", publicada=False
    )
    _configurar(InMemoryEventoRepo([publicado, borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos")

    assert response.status_code == 200
    assert "Evento publicado" in response.text
    assert "Evento en borrador" not in response.text


@pytest.mark.asyncio
async def test_evento_publicado_aparece_en_el_listado():
    publicado = Evento.create(
        titulo="Jornada de Ciencias 2026", descripcion="Descripción", fecha_evento="2026-11-01T10:00:00", publicada=True
    )
    _configurar(InMemoryEventoRepo([publicado]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos")

    assert "Jornada de Ciencias 2026" in response.text


@pytest.mark.asyncio
async def test_evento_no_publicado_no_aparece_en_el_listado():
    borrador = Evento.create(
        titulo="Todavia sin publicar", descripcion="Descripción", fecha_evento="2026-11-01T10:00:00", publicada=False
    )
    _configurar(InMemoryEventoRepo([borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos")

    assert "Todavia sin publicar" not in response.text


@pytest.mark.asyncio
async def test_listado_vacio_muestra_mensaje_sin_romper():
    _configurar(InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos")

    assert response.status_code == 200
    assert "Todavía no hay eventos publicados" in response.text


@pytest.mark.asyncio
async def test_listado_ordena_por_fecha_ascendente():
    mas_tarde = Evento.create(
        titulo="Evento de diciembre", descripcion="Descripción", fecha_evento="2026-12-01T10:00:00", publicada=True
    )
    mas_temprano = Evento.create(
        titulo="Evento de enero", descripcion="Descripción", fecha_evento="2026-01-01T10:00:00", publicada=True
    )
    # Se guardan en orden inverso al esperado para verificar que el orden lo define el repositorio.
    _configurar(InMemoryEventoRepo([mas_tarde, mas_temprano]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos")

    body = response.text
    assert body.index("Evento de enero") < body.index("Evento de diciembre")


# --- Detalle por slug ---


@pytest.mark.asyncio
async def test_detalle_por_slug_responde_200_y_muestra_contenido():
    evento = Evento.create(
        titulo="Jornada de Ciencias 2026",
        descripcion="Descripción completa del evento",
        fecha_evento="2026-11-01T10:00:00",
        lugar="Auditorio principal",
        publicada=True,
    )
    _configurar(InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/eventos/{evento.slug}")

    assert response.status_code == 200
    assert evento.slug == "jornada-de-ciencias-2026"
    assert "Jornada de Ciencias 2026" in response.text
    assert "Descripción completa del evento" in response.text
    assert "Auditorio principal" in response.text


@pytest.mark.asyncio
async def test_detalle_slug_inexistente_devuelve_404():
    _configurar(InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos/no-existe")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_detalle_evento_no_publicado_devuelve_404():
    borrador = Evento.create(
        titulo="Aviso interno", descripcion="Descripción", fecha_evento="2026-11-01T10:00:00", publicada=False
    )
    _configurar(InMemoryEventoRepo([borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/eventos/{borrador.slug}")

    assert response.status_code == 404
    assert "Aviso interno" not in response.text


@pytest.mark.asyncio
async def test_detalle_no_expone_autor_id():
    evento = Evento.create(
        titulo="Evento con autor",
        descripcion="Descripción",
        fecha_evento="2026-11-01T10:00:00",
        autor_id="autor-secreto-456",
        publicada=True,
    )
    _configurar(InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/eventos/{evento.slug}")

    assert "autor-secreto-456" not in response.text


# --- SEO / JSON-LD ---


@pytest.mark.asyncio
async def test_detalle_incluye_json_ld_event():
    evento = Evento.create(
        titulo="Evento con SEO", descripcion="Descripción", fecha_evento="2026-11-01T10:00:00", publicada=True
    )
    _configurar(InMemoryEventoRepo([evento]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get(f"/eventos/{evento.slug}")

    assert response.status_code == 200
    assert '"@type": "Event"' in response.text
    assert "<title>Evento con SEO" in response.text


@pytest.mark.asyncio
async def test_listado_incluye_canonical_y_title():
    _configurar(InMemoryEventoRepo([]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/eventos")

    assert response.status_code == 200
    assert "<title>Eventos" in response.text
    assert "rel='canonical'" in response.text


# --- Sitemap ---


@pytest.mark.asyncio
async def test_sitemap_incluye_solo_eventos_publicados():
    publicado = Evento.create(
        titulo="Evento publicado en sitemap",
        descripcion="Descripción",
        fecha_evento="2026-11-01T10:00:00",
        publicada=True,
    )
    borrador = Evento.create(
        titulo="Evento borrador en sitemap",
        descripcion="Descripción",
        fecha_evento="2026-11-05T10:00:00",
        publicada=False,
    )
    _configurar(InMemoryEventoRepo([publicado, borrador]))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/sitemap.xml")

    assert response.status_code == 200
    body = response.text
    assert f"/eventos/{publicado.slug}" in body
    assert f"/eventos/{borrador.slug}" not in body
    assert "<loc>" in body and "/eventos</loc>" in body
