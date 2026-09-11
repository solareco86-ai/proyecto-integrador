"""add_slug_columns

Revision ID: e7f1b5c8a3d2
Revises: d4e6c3a9f210
Create Date: 2026-09-12 00:00:00.000000

Agrega la columna `slug` (con índice único) a noticias, eventos y
comunicados, para soportar URLs públicas amigables. No modifica ninguna
migración existente.

Los registros ya existentes (si los hubiera) se completan (backfill) con un
slug generado a partir de su título, resolviendo colisiones con un sufijo
numérico, antes de crear el índice único — así ningún registro queda con un
slug NULL o duplicado y la aplicación no se rompe al leer datos previos.

La función de generación de slugs se reimplementa acá, self-contained,
en vez de importar `src.domain.common.slugify`: las migraciones no deben
depender del código de la aplicación, que puede cambiar en el futuro.
"""
import re
import unicodedata
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e7f1b5c8a3d2"
down_revision: str | Sequence[str] | None = "d4e6c3a9f210"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _slugify(texto: str) -> str:
    """Copia self-contained de la normalización de slugs usada por el dominio."""
    normalizado = unicodedata.normalize("NFKD", texto)
    sin_tildes = normalizado.encode("ascii", "ignore").decode("ascii")
    minusculas = sin_tildes.lower()
    con_guiones = re.sub(r"[^a-z0-9]+", "-", minusculas)
    return con_guiones.strip("-") or "item"


def _backfill_slugs(table_name: str) -> None:
    """Completa el slug de los registros existentes que todavía no lo tienen."""
    conn = op.get_bind()
    metadata = sa.MetaData()
    tabla = sa.Table(table_name, metadata, autoload_with=conn)

    filas = conn.execute(sa.select(tabla.c.id, tabla.c.titulo).order_by(tabla.c.created_at)).fetchall()

    slugs_usados: set[str] = set()
    for fila in filas:
        base = _slugify(fila.titulo)
        candidato = base
        contador = 2
        while candidato in slugs_usados:
            candidato = f"{base}-{contador}"
            contador += 1
        slugs_usados.add(candidato)
        conn.execute(tabla.update().where(tabla.c.id == fila.id).values(slug=candidato))


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("noticias", sa.Column("slug", sa.String(length=220), nullable=True))
    _backfill_slugs("noticias")
    op.create_index(op.f("ix_noticias_slug"), "noticias", ["slug"], unique=True)

    op.add_column("eventos", sa.Column("slug", sa.String(length=220), nullable=True))
    _backfill_slugs("eventos")
    op.create_index(op.f("ix_eventos_slug"), "eventos", ["slug"], unique=True)

    op.add_column("comunicados", sa.Column("slug", sa.String(length=220), nullable=True))
    _backfill_slugs("comunicados")
    op.create_index(op.f("ix_comunicados_slug"), "comunicados", ["slug"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_comunicados_slug"), table_name="comunicados")
    op.drop_column("comunicados", "slug")

    op.drop_index(op.f("ix_eventos_slug"), table_name="eventos")
    op.drop_column("eventos", "slug")

    op.drop_index(op.f("ix_noticias_slug"), table_name="noticias")
    op.drop_column("noticias", "slug")
