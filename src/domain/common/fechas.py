"""Cálculos de fechas del dominio. Solo librería estándar."""

from datetime import date, datetime, timedelta, timezone

# Hora oficial argentina. No tiene horario de verano desde 2009, así que un
# huso fijo alcanza y no depende de que el servidor tenga la base de zonas.
HORA_ARGENTINA = timezone(timedelta(hours=-3), "ART")


def hoy_en_argentina() -> date:
    """La fecha de hoy en Argentina: de 21:00 a 24:00 en UTC ya es mañana."""
    return datetime.now(HORA_ARGENTINA).date()


def dias_restantes(fecha_iso: str, hoy: date | None = None) -> int | None:
    """Días que faltan hasta `fecha_iso` (formato AAAA-MM-DD).

    Devuelve 0 el mismo día del vencimiento y `None` si la fecha ya pasó o no
    es interpretable: quien renderiza decide qué hacer en cada caso, pero nunca
    recibe un número negativo que pueda publicarse como si fuera un plazo.
    """
    try:
        limite = date.fromisoformat(fecha_iso)
    except (TypeError, ValueError):
        return None

    referencia = hoy if hoy is not None else hoy_en_argentina()
    diferencia = (limite - referencia).days
    return diferencia if diferencia >= 0 else None
