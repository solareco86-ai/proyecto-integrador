"""Contrato de repositorio para la persistencia de usuarios."""

from abc import ABC, abstractmethod

from src.domain.auth.entities import Usuario


class UsuarioRepository(ABC):
    """Interfaz que deben implementar los repositorios de usuarios."""

    @abstractmethod
    async def save(self, usuario: Usuario) -> None:
        """Persiste un usuario en el almacén de datos."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Usuario | None:
        """Busca un usuario por su email. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, usuario_id: str) -> Usuario | None:
        """Busca un usuario por su id. Devuelve None si no existe."""
        raise NotImplementedError

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos (True por defecto en repositorios base/memoria)."""
        return True
