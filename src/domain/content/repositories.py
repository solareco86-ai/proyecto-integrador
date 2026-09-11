"""Contratos de repositorio para la persistencia de contenido institucional."""

from abc import ABC, abstractmethod

from src.domain.content.entities import Comunicado, Evento, Noticia


class NoticiaRepository(ABC):
    """Interfaz que deben implementar los repositorios de noticias."""

    @abstractmethod
    async def save(self, noticia: Noticia) -> None:
        """Persiste una noticia nueva en el almacén de datos."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, noticia_id: str) -> Noticia | None:
        """Busca una noticia por su id. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Noticia]:
        """Devuelve todas las noticias almacenadas."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, noticia: Noticia) -> None:
        """Actualiza una noticia existente."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, noticia_id: str) -> None:
        """Elimina una noticia por su id. No falla si el id no existe."""
        raise NotImplementedError

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos (True por defecto en repositorios base/memoria)."""
        return True


class EventoRepository(ABC):
    """Interfaz que deben implementar los repositorios de eventos."""

    @abstractmethod
    async def save(self, evento: Evento) -> None:
        """Persiste un evento nuevo en el almacén de datos."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, evento_id: str) -> Evento | None:
        """Busca un evento por su id. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Evento]:
        """Devuelve todos los eventos almacenados."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, evento: Evento) -> None:
        """Actualiza un evento existente."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, evento_id: str) -> None:
        """Elimina un evento por su id. No falla si el id no existe."""
        raise NotImplementedError

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos (True por defecto en repositorios base/memoria)."""
        return True


class ComunicadoRepository(ABC):
    """Interfaz que deben implementar los repositorios de comunicados."""

    @abstractmethod
    async def save(self, comunicado: Comunicado) -> None:
        """Persiste un comunicado nuevo en el almacén de datos."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, comunicado_id: str) -> Comunicado | None:
        """Busca un comunicado por su id. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Comunicado]:
        """Devuelve todos los comunicados almacenados."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, comunicado: Comunicado) -> None:
        """Actualiza un comunicado existente."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, comunicado_id: str) -> None:
        """Elimina un comunicado por su id. No falla si el id no existe."""
        raise NotImplementedError

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos (True por defecto en repositorios base/memoria)."""
        return True
