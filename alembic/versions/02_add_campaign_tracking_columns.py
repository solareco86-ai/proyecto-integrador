"""add_campaign_tracking_columns

Revision ID: b2c4a1f9d7e3
Revises: 577a94057b53
Create Date: 2026-08-14 23:50:00.000000

Añade las columnas de tracking de campañas (gclid, fbclid, utm_*) a la tabla leads,
alineando el esquema con LeadModel (SQLAlchemy) y el INSERT de LeadRepositorySQL.
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2c4a1f9d7e3"
down_revision: str | Sequence[str] | None = "577a94057b53"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("leads", sa.Column("gclid", sa.String(length=255), nullable=True))
    op.add_column("leads", sa.Column("fbclid", sa.String(length=255), nullable=True))
    op.add_column("leads", sa.Column("utm_source", sa.String(length=255), nullable=True))
    op.add_column("leads", sa.Column("utm_medium", sa.String(length=255), nullable=True))
    op.add_column("leads", sa.Column("utm_campaign", sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("leads", "utm_campaign")
    op.drop_column("leads", "utm_medium")
    op.drop_column("leads", "utm_source")
    op.drop_column("leads", "fbclid")
    op.drop_column("leads", "gclid")
