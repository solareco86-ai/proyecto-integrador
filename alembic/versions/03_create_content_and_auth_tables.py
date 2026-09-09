"""create_content_and_auth_tables

Revision ID: d4e6c3a9f210
Revises: b2c4a1f9d7e3
Create Date: 2026-09-09 00:00:00.000000

Crea las tablas usuarios, noticias, eventos y comunicados para el panel
de autoridades, alineadas con los modelos ORM (UsuarioModel, NoticiaModel,
EventoModel, ComunicadoModel).
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d4e6c3a9f210"
down_revision: str | Sequence[str] | None = "b2c4a1f9d7e3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "usuarios",
        sa.Column("id", sa.String(length=40), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("rol", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "noticias",
        sa.Column("id", sa.String(length=40), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("cuerpo", sa.Text(), nullable=False),
        sa.Column("autor_id", sa.String(length=40), nullable=True),
        sa.Column("publicada", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["autor_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_noticias_created_at"), "noticias", ["created_at"], unique=False)

    op.create_table(
        "eventos",
        sa.Column("id", sa.String(length=40), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("fecha_evento", sa.DateTime(), nullable=False),
        sa.Column("lugar", sa.String(length=255), nullable=True),
        sa.Column("autor_id", sa.String(length=40), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["autor_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_eventos_created_at"), "eventos", ["created_at"], unique=False)

    op.create_table(
        "comunicados",
        sa.Column("id", sa.String(length=40), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("cuerpo", sa.Text(), nullable=False),
        sa.Column("autor_id", sa.String(length=40), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["autor_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_comunicados_created_at"), "comunicados", ["created_at"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_comunicados_created_at"), table_name="comunicados")
    op.drop_table("comunicados")

    op.drop_index(op.f("ix_eventos_created_at"), table_name="eventos")
    op.drop_table("eventos")

    op.drop_index(op.f("ix_noticias_created_at"), table_name="noticias")
    op.drop_table("noticias")

    op.drop_table("usuarios")
