"""Re-export para compatibilidad hacia atrás del contrato LeadRepository."""

from src.domain.leads.repositories import LeadRepository

__all__ = ["LeadRepository"]
