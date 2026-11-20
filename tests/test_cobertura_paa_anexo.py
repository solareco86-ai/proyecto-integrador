from pathlib import Path
from typing import Any, cast

import pytest
import yaml

CURSO_DIR = Path("data/core/cursos/procesamiento-aprendizaje-automatico")
MAPA_PATH = CURSO_DIR / "mapa-cobertura-anexo.yaml"
ESPECIFICACION_PATH = CURSO_DIR / "especificacion-oficial.yaml"


@pytest.fixture(scope="module")
def mapa_cobertura() -> dict[str, Any]:
    assert MAPA_PATH.exists(), f"El archivo {MAPA_PATH} debe existir"
    with open(MAPA_PATH, encoding="utf-8") as f:
        data: Any = yaml.safe_load(f)
    assert isinstance(data, dict), "El mapa de cobertura debe ser un diccionario YAML válido"
    return cast(dict[str, Any], data)


@pytest.fixture(scope="module")
def especificacion_oficial() -> dict[str, Any]:
    assert ESPECIFICACION_PATH.exists(), f"El archivo {ESPECIFICACION_PATH} debe existir"
    with open(ESPECIFICACION_PATH, encoding="utf-8") as f:
        data: Any = yaml.safe_load(f)
    assert isinstance(data, dict), "La especificación oficial debe ser un diccionario YAML válido"
    return cast(dict[str, Any], data)


def test_mapa_cobertura_estructura_metadata(mapa_cobertura: dict[str, Any]) -> None:
    """Verifica que los metadatos del mapa estén completos y referencien la resolución oficial."""
    metadata = mapa_cobertura.get("metadata", {})
    assert "2730/22" in metadata.get("resolucion", "")
    assert "12" in metadata.get("espacio", "")
    assert "modo_estricto" in metadata


def test_mapa_cobertura_capacidades_profesionales(
    mapa_cobertura: dict[str, Any], especificacion_oficial: dict[str, Any]
) -> None:
    """Verifica que las 3 capacidades del anexo figuren en el mapa y tengan estado válido."""
    capacidades_oficiales = especificacion_oficial.get("capacidades_profesionales", [])
    assert len(capacidades_oficiales) == 3

    capacidades_mapa = mapa_cobertura.get("capacidades_profesionales", [])
    assert len(capacidades_mapa) == 3

    textos_mapa = {c.get("texto_literal") for c in capacidades_mapa}
    for cap_oficial in capacidades_oficiales:
        assert cap_oficial in textos_mapa, f"La capacidad oficial '{cap_oficial}' debe figurar en el mapa de cobertura"


def test_mapa_cobertura_bloques_contenidos_completos(mapa_cobertura: dict[str, Any]) -> None:
    """Verifica que todos los ítems de contenidos de los 3 bloques tengan cobertura o estado explícito."""
    bloques = mapa_cobertura.get("contenidos_bloques", [])
    assert len(bloques) >= 28, f"Se esperaban al menos 28 contenidos temáticos, se encontraron {len(bloques)}"

    for item in bloques:
        cid = item.get("id")
        literal = item.get("contenido_literal")
        estado = item.get("estado")
        lecciones = item.get("lecciones", [])

        assert estado in {"cubierto", "pendiente"}, (
            f"El ítem '{cid}' ({literal}) tiene un estado no permitido: '{estado}'. Debe ser 'cubierto' o 'pendiente'."
        )

        if estado == "cubierto":
            assert len(lecciones) > 0, (
                f"El contenido '{literal}' está marcado como 'cubierto' pero no lista ninguna lección."
            )
            for leccion_rel in lecciones:
                archivo = CURSO_DIR / leccion_rel
                assert archivo.exists(), (
                    f"La lección '{leccion_rel}' asignada al contenido '{literal}' no existe en {archivo}."
                )
        elif estado == "pendiente":
            assert item.get("entregable_asociado"), (
                f"El contenido '{literal}' está en estado 'pendiente' sin declarar 'entregable_asociado'."
            )


def test_mapa_cobertura_modo_estricto_o_progreso(mapa_cobertura: dict[str, Any]) -> None:
    """Si modo_estricto está activo, falla si algún contenido o capacidad queda pendiente."""
    metadata = mapa_cobertura.get("metadata", {})
    modo_estricto = metadata.get("modo_estricto", False)

    pendientes: list[str] = []
    for item in mapa_cobertura.get("contenidos_bloques", []):
        if item.get("estado") == "pendiente":
            pendientes.append(f"Bloque: {item.get('contenido_literal')} ({item.get('entregable_asociado')})")

    for cap in mapa_cobertura.get("capacidades_profesionales", []):
        if cap.get("estado") == "pendiente":
            pendientes.append(f"Capacidad {cap.get('numero')}: {cap.get('texto_literal')}")

    if modo_estricto:
        assert not pendientes, (
            f"El modo estricto está ACTIVO pero existen {len(pendientes)} contenidos pendientes:\n"
            + "\n".join(pendientes)
        )
