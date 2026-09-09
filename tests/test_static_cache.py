"""Tests del cache-busting robusto de frontend (spec cache-busting-frontend)."""

import time
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from src.infrastructure.fastapi import dependencies
from src.infrastructure.fastapi.app import app
from src.infrastructure.settings import config


def _reset_static_version_cache() -> None:
    """Reinicia la caché interna de static_version para aislar cada test."""
    dependencies._static_version_cache = None


@pytest.mark.asyncio  # type: ignore
async def test_static_con_query_lleva_immutable() -> None:
    original_debug = config.DEBUG
    config.DEBUG = False
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/static/robots.txt?v=abc123")

        cache_control = response.headers.get("cache-control", "")
        assert "immutable" in cache_control
        assert f"max-age={config.STATIC_CACHE_SECONDS}" in cache_control
    finally:
        config.DEBUG = original_debug


@pytest.mark.asyncio  # type: ignore
async def test_static_sin_query_sin_immutable() -> None:
    original_debug = config.DEBUG
    config.DEBUG = False
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/static/robots.txt")

        cache_control = response.headers.get("cache-control", "")
        assert "immutable" not in cache_control
        assert f"max-age={config.STATIC_MODULE_MAX_AGE}" in cache_control
    finally:
        config.DEBUG = original_debug


def test_static_version_estable_dentro_del_ttl() -> None:
    original_debug = config.DEBUG
    config.DEBUG = False
    _reset_static_version_cache()
    try:
        v1 = dependencies.get_static_version()
        v2 = dependencies.get_static_version()
        assert v1 == v2
        assert v1 != ""  # digest no vacío
    finally:
        config.DEBUG = original_debug
        _reset_static_version_cache()


def test_static_version_cambia_con_contenido() -> None:
    original_debug = config.DEBUG
    config.DEBUG = False
    _reset_static_version_cache()
    try:
        v1 = dependencies.get_static_version()
        # Fuerza el vencimiento del TTL y un hash de contenido distinto.
        dependencies._static_version_cache = (time.monotonic() - 9999, v1)
        with patch.object(dependencies, "_hash_static_tree", return_value="nuevohash1234"):
            v2 = dependencies.get_static_version()
        assert v1 != v2
        assert v2 == "nuevohash1234"
    finally:
        config.DEBUG = original_debug
        _reset_static_version_cache()


def test_static_version_debug_usa_timestamp() -> None:
    original_debug = config.DEBUG
    config.DEBUG = True
    _reset_static_version_cache()
    try:
        version = dependencies.get_static_version()
        assert version.isdigit()
    finally:
        config.DEBUG = original_debug
        _reset_static_version_cache()


def test_static_version_fallback_ante_error() -> None:
    original_debug = config.DEBUG
    config.DEBUG = False
    _reset_static_version_cache()
    try:
        with patch.object(
            dependencies, "_hash_static_tree", side_effect=Exception("boom")
        ):
            version = dependencies.get_static_version()
        assert version.isdigit()  # fallback a timestamp
    finally:
        config.DEBUG = original_debug
        _reset_static_version_cache()


def test_hash_static_tree_ignora_archivo_ilegible() -> None:
    with patch.object(
        dependencies.os, "walk", return_value=[("static/js", [], ["x.js"])]
    ):
        with patch("builtins.open", side_effect=OSError("permiso denegado")):
            result = dependencies._hash_static_tree()
    assert isinstance(result, str)
    assert len(result) == 12
