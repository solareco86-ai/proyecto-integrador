from abc import ABC, abstractmethod

from src.application.dtos import TelemetryPlanModel


class TelemetryPlanesGateway(ABC):
    """Puerto de salida para obtener el catálogo de planes de telemetría."""

    @abstractmethod
    def obtener_catalogo(self) -> list[TelemetryPlanModel]:
        """Devuelve el catálogo de planes (fuente de verdad: API datamaq-telemetry)."""
        raise NotImplementedError
