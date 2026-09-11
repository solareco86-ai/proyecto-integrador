"""Entidades de dominio del subdominio de Autenticación."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass
class Usuario:
    id: str
    email: str
    password_hash: str
    nombre: str
    rol: str = "autoridad"
    is_active: bool = True
    created_at: str | None = None

    @classmethod
    def create(
        cls,
        email: str,
        password_hash: str,
        nombre: str,
        rol: str = "autoridad",
        is_active: bool = True,
    ) -> "Usuario":
        """Crea una instancia de Usuario con un id y created_at nuevos."""
        return cls(
            id=str(uuid4()),
            email=email,
            password_hash=password_hash,
            nombre=nombre,
            rol=rol,
            is_active=is_active,
            created_at=datetime.now(UTC).isoformat(),
        )
