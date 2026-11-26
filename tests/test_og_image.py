from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from PIL import Image

from src.infrastructure.fastapi.app import app


def test_og_default_image_properties() -> None:
    """Verifica que la imagen Open Graph por defecto exista y tenga formato estándar."""
    og_path = Path("static/og-default.webp")
    assert og_path.exists(), "static/og-default.webp debe existir"

    with Image.open(og_path) as im:
        assert im.format == "WEBP"
        assert im.size == (1200, 630)


@pytest.mark.asyncio
async def test_home_renders_institutional_og_image() -> None:
    """Verifica que la home inyecte la imagen Open Graph institucional en el meta tag."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert "og:image" in response.text
    assert "og-default.webp" in response.text
