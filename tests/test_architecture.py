"""Pruebas automáticas de conformidad arquitectónica (Clean Architecture & DDD).

Verifica estáticamente mediante el script `scripts/verify_architecture.py` que ningún módulo
en `src/` viole la regla de dependencia de capas.
"""

from scripts.verify_architecture import verify_architecture


def test_clean_architecture_compliance():
    """Verifica que el 100% de los módulos en src/ respetan las restricciones de capas."""
    errors = verify_architecture()
    assert not errors, f"Se detectaron {len(errors)} violaciones de Clean Architecture:\n" + "\n".join(errors)
