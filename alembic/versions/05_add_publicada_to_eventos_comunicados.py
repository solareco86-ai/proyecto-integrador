"""add_publicada_to_eventos_comunicados

Revision ID: f3a9c1d7b6e4
Revises: e7f1b5c8a3d2
Create Date: 2026-09-12 00:00:00.000000

Agrega la columna `publicada` a eventos y comunicados (noticias ya la
tenía desde la migración 03). No modifica ninguna migración existente.

A diferencia de Noticia, cuyo valor por defecto es `True`, el contenido
nuevo de Eventos y Comunicados NO debe hacerse público automáticamente:
debe poder prepararse desde el panel y publicarse explícitamente. Por eso
la columna se agrega con `server_default=false` — los registros existentes
(si los hubiera) quedan en estado no publicado, un valor seguro que evita
exponer contenido preexistente sin revisión, y ningún registro queda con
`publicada` en NULL.
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f3a9c1d7b6e4"
down_revision: str | Sequence[str] | None = "e7f1b5c8a3d2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "eventos",
        sa.Column("publicada", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "comunicados",
        sa.Column("publicada", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("comunicados", "publicada")
    op.drop_column("eventos", "publicada")
