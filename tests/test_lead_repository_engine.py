"""Tests de regresión para la configuración del engine SQLAlchemy de leads.

Cubre el bug de `pool_pre_ping` + `aiomysql`: el `do_ping` síncrono de SQLAlchemy
llama `ping()` sin `reconnect`, argumento posicional que exige el adaptador async
de aiomysql, rompiendo el segundo checkout del pool de conexiones.
"""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from src.infrastructure.persistence.mysql import lead_repository_mysql

_MYSQL_URL = "mysql+aiomysql://datamaq_leads:secret@127.0.0.1:3306/datamaq_leads"


@pytest.fixture(autouse=True)
def _reset_engine() -> Generator[None, None, None]:
    """Aísla el singleton `_engine` entre tests."""
    lead_repository_mysql._engine = None
    yield
    lead_repository_mysql._engine = None


def test_engine_mysql_no_usa_pool_pre_ping() -> None:
    """MySQL no debe configurar `pool_pre_ping` (incompatible con aiomysql)."""
    mock_create = MagicMock()
    with (
        patch.object(lead_repository_mysql, "create_async_engine", mock_create),
        patch.object(lead_repository_mysql.config, "DATABASE_URL", _MYSQL_URL),
    ):
        lead_repository_mysql._get_engine()

    assert mock_create.call_args is not None
    kwargs = mock_create.call_args.kwargs
    assert "pool_pre_ping" not in kwargs
    assert kwargs["pool_size"] == 3
    assert kwargs["max_overflow"] == 2


def test_engine_sqlite_sin_kwargs_mysql() -> None:
    """El fallback SQLite no recibe kwargs de pool propios de MySQL."""
    mock_create = MagicMock()
    with (
        patch.object(lead_repository_mysql, "create_async_engine", mock_create),
        patch.object(lead_repository_mysql.config, "DATABASE_URL", ""),
    ):
        lead_repository_mysql._get_engine()

    assert mock_create.call_args is not None
    kwargs = mock_create.call_args.kwargs
    assert "pool_size" not in kwargs
    assert "max_overflow" not in kwargs
    assert "pool_pre_ping" not in kwargs
