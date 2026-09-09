import re


class Price(float):
    """Value Object puro (stdlib) que representa un Precio no negativo en el dominio."""

    def __new__(cls, value: float | int) -> "Price":
        val = float(value)
        if val < 0.0:
            raise ValueError(f"Precio inválido: {val}. No puede ser negativo.")
        return super().__new__(cls, val)

    @classmethod
    def validate(cls, v: float | int) -> "Price":
        """Valida y crea una instancia inmutable de Price."""
        return cls(v)


class Slug(str):
    """Value Object puro (stdlib) que representa un Slug url-safe e inmutable en el dominio."""

    def __new__(cls, value: str) -> "Slug":
        val = str(value).strip()
        if not re.fullmatch(r"[a-z0-9-]+", val):
            raise ValueError(f"Slug inválido: '{val}'. Debe ser alfanumérico en minúsculas con guiones.")
        return super().__new__(cls, val)

    @classmethod
    def validate(cls, v: str) -> "Slug":
        """Valida y crea una instancia inmutable de Slug."""
        return cls(v)
