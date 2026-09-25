"""add_imagen_columns

Revision ID: 375cc69b4ea8
Revises: f3a9c1d7b6e4
Create Date: 2026-09-24 00:00:00.000000

Agrega la columna `imagen` (ruta relativa del archivo, no bytes) a noticias,
eventos y comunicados, para soportar imágenes opcionales desde el Panel de
Autoridades. La columna es nullable en las tres tablas: el contenido
existente sin imagen sigue siendo válido sin necesidad de backfill.
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "375cc69b4ea8"
down_revision: str | Sequence[str] | None = "f3a9c1d7b6e4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("noticias", sa.Column("imagen", sa.String(255), nullable=True))
    op.add_column("eventos", sa.Column("imagen", sa.String(255), nullable=True))
    op.add_column("comunicados", sa.Column("imagen", sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("comunicados", "imagen")
    op.drop_column("eventos", "imagen")
    op.drop_column("noticias", "imagen")
