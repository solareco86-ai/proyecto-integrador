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


class CredencialesInvalidasError(DomainError):
    """Lanzada cuando el login falla: email inexistente, password incorrecta o usuario inactivo.

    Se usa el mismo mensaje/excepción para los tres casos para no filtrar,
    a través de una diferencia de error, si un email está o no registrado.
    """

    pass
