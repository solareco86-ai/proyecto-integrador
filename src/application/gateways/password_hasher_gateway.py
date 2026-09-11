"""Puerto de aplicación para el hashing y verificación de contraseñas."""

from abc import ABC, abstractmethod


class PasswordHasherGateway(ABC):
    """Interfaz que deben implementar los hashers de contraseñas.

    El dominio y los use cases dependen únicamente de esta interfaz,
    nunca de la librería de hashing concreta (p. ej. bcrypt).
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """Genera el hash seguro de una contraseña en texto plano."""
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Verifica si una contraseña en texto plano coincide con un hash."""
        raise NotImplementedError
