import pytest
from httpx import ASGITransport, AsyncClient  # type: ignore

from src.infrastructure.fastapi.app import app


@pytest.mark.asyncio  # type: ignore
async def test_no_redirect_for_canonical_request():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/", follow_redirects=False)
    assert response.status_code == 200


@pytest.mark.asyncio  # type: ignore
async def test_redirect_www_to_non_www():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://www.test") as ac:
        response = await ac.get("/", follow_redirects=False)
    assert response.status_code == 308
    assert response.headers["location"] == "http://test/"


@pytest.mark.asyncio  # type: ignore
async def test_redirect_trailing_slash():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/contact/", follow_redirects=False)
    assert response.status_code == 308
    assert response.headers["location"] == "http://test/contact"


@pytest.mark.asyncio  # type: ignore
async def test_redirect_http_to_https_via_forwarded_proto():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/", headers={"X-Forwarded-Proto": "http"}, follow_redirects=False)
    assert response.status_code == 308
    assert response.headers["location"] == "https://test/"


@pytest.mark.asyncio  # type: ignore
async def test_no_redirect_when_forwarded_proto_is_https():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/", headers={"X-Forwarded-Proto": "https"}, follow_redirects=False)
    assert response.status_code == 200


@pytest.mark.asyncio  # type: ignore
async def test_no_redirect_for_root_path():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/", follow_redirects=False)
    assert response.status_code == 200
