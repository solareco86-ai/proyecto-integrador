"""Cálculos de fechas del dominio. Solo librería estándar."""

from datetime import UTC, date, datetime


def dias_restantes(fecha_iso: str, hoy: date | None = None) -> int | None:
    """Días que faltan hasta `fecha_iso` (formato AAAA-MM-DD).

    Devuelve 0 el mismo día del vencimiento y `None` si la fecha ya pasó o no
    es interpretable: quien renderiza decide qué hacer en cada caso, pero nunca
    recibe un número negativo que pueda publicarse como si fuera un plazo.
    """
    try:
        limite = date.fromisoformat(fecha_iso)
    except ValueError:
        return None

    referencia = hoy if hoy is not None else datetime.now(UTC).date()
    diferencia = (limite - referencia).days
    return diferencia if diferencia >= 0 else None
