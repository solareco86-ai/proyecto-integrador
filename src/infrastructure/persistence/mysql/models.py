from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
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


class UsuarioModel(Base):
    """Modelo ORM SQLAlchemy para la tabla usuarios (autoridades del panel)."""

    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), default="autoridad", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)


class NoticiaModel(Base):
    """Modelo ORM SQLAlchemy para la tabla noticias."""

    __tablename__ = "noticias"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    cuerpo: Mapped[str] = mapped_column(Text, nullable=False)
    autor_id: Mapped[str | None] = mapped_column(String(40), ForeignKey("usuarios.id"), nullable=True)
    publicada: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    slug: Mapped[str | None] = mapped_column(String(220), nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class EventoModel(Base):
    """Modelo ORM SQLAlchemy para la tabla eventos."""

    __tablename__ = "eventos"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_evento: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    lugar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    autor_id: Mapped[str | None] = mapped_column(String(40), ForeignKey("usuarios.id"), nullable=True)
    publicada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    slug: Mapped[str | None] = mapped_column(String(220), nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ComunicadoModel(Base):
    """Modelo ORM SQLAlchemy para la tabla comunicados."""

    __tablename__ = "comunicados"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    cuerpo: Mapped[str] = mapped_column(Text, nullable=False)
    autor_id: Mapped[str | None] = mapped_column(String(40), ForeignKey("usuarios.id"), nullable=True)
    publicada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    slug: Mapped[str | None] = mapped_column(String(220), nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
