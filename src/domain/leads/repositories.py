"""Contrato de repositorio para la persistencia de leads."""

from abc import ABC, abstractmethod

from src.domain.leads.entities import Lead


class LeadRepository(ABC):
    """Interfaz que deben implementar los repositorios de leads."""

    @abstractmethod
    async def save(self, lead: Lead) -> None:
        """Persiste un lead en el almacén de datos."""
        raise NotImplementedError

    async def is_healthy(self) -> bool:
        """Verifica la conectividad con el almacén de datos (True por defecto en repositorios base/memoria)."""
        return True
