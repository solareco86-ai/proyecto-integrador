"""Excepciones de dominio transversales."""


class DomainError(Exception):
    """Excepción base para errores de dominio."""

    pass


class EntityNotFoundError(DomainError):
    """Lanzada cuando una entidad solicitada no existe."""

    pass


class ValidationError(DomainError):
    """Lanzada cuando fallan las invariantes de dominio."""

    pass
