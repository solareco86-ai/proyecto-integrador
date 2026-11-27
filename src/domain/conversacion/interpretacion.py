from dataclasses import dataclass

# Categorías léxicas (preterminales) que reconoce la gramática de consultas.
CATEGORIA_SALUDO = "SALUDO"
CATEGORIA_PEDIDO = "PEDIDO"
CATEGORIA_NUCLEO = "NUCLEO"
CATEGORIA_TRAMITE = "TRAMITE"
CATEGORIA_CARRERA = "CARRERA"
CATEGORIA_ORDINAL = "ORD"
CATEGORIA_MARCA_ANIO = "MARCA_ANIO"
CATEGORIA_RUIDO = "RUIDO"

INTENCION_FUERA_DE_DOMINIO = "fuera_de_dominio"


@dataclass(frozen=True)
class Simbolo:
    """Palabra o expresión de la consulta etiquetada con su categoría léxica."""

    categoria: str
    valor: str
    texto: str


@dataclass(frozen=True)
class Entidades:
    """Entidades clave extraídas de la consulta."""

    carrera: str | None = None
    anio: int | None = None
    tramite: str | None = None


@dataclass(frozen=True)
class Interpretacion:
    """Resultado del análisis semántico: intención principal, entidades y confianza."""

    intencion: str
    entidades: Entidades
    confianza: float
    aceptada: bool
    regla: str | None = None
