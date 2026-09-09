from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa para ORM de SQLAlchemy."""

    pass


class LeadModel(Base):
    """Modelo ORM SQLAlchemy para la tabla leads."""

    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=True)
    last_name: Mapped[str] = mapped_column(String(60), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    company: Mapped[str] = mapped_column(String(120), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    preferred_contact_channel: Mapped[str] = mapped_column(String(20), default="whatsapp", nullable=True)
    page_location: Mapped[str] = mapped_column(String(500), nullable=True)
    traffic_source: Mapped[str] = mapped_column(String(500), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=True)
    geographic_location: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, index=True)
    captcha_token: Mapped[str] = mapped_column(String(255), nullable=True)
    gclid: Mapped[str] = mapped_column(String(255), nullable=True)
    fbclid: Mapped[str] = mapped_column(String(255), nullable=True)
    utm_source: Mapped[str] = mapped_column(String(255), nullable=True)
    utm_medium: Mapped[str] = mapped_column(String(255), nullable=True)
    utm_campaign: Mapped[str] = mapped_column(String(255), nullable=True)
    lead_source: Mapped[str | None] = mapped_column(String(80), nullable=True)
