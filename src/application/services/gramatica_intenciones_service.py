"""Gramática de consultas institucionales con atributos (estilo DCG).

La gramática se aplica sobre la secuencia de símbolos que produce el léxico
controlado. En notación DCG (ver docs/eje1-gramatica-intenciones.md):

    consulta(I, E)  --> cuerpo(E0), { resolver(E0, I, E) }.
    cuerpo(E)       --> [] | elemento(E1), cuerpo(E2), { unificar(E1, E2, E) }.
    elemento(t(T))  --> [tramite(T)].
    elemento(c(C))  --> [carrera(C)].
    elemento(a(N))  --> anio(N).
    elemento(n)     --> [nucleo].
    elemento(s)     --> [saludo].
    elemento(vacio) --> [pedido] | [ruido] | [ord(_)] | [marca_anio].
    anio(N)         --> [ord(N)], [marca_anio].
    anio(N)         --> [marca_anio], [ord(N)].

La unificación falla (consulta rechazada) si aparecen dos carreras, dos años
o dos trámites distintos en la misma consulta.
"""

from dataclasses import dataclass

from src.domain.conversacion.interpretacion import (
    CATEGORIA_CARRERA,
    CATEGORIA_MARCA_ANIO,
    CATEGORIA_NUCLEO,
    CATEGORIA_ORDINAL,
    CATEGORIA_RUIDO,
    CATEGORIA_SALUDO,
    CATEGORIA_TRAMITE,
    INTENCION_FUERA_DE_DOMINIO,
    Entidades,
    Interpretacion,
    Simbolo,
)

REGLA_TRAMITE = "consulta_tramite"
REGLA_CARRERA = "consulta_carrera"
REGLA_SALUDO = "saludo"
REGLA_CONFLICTO = "conflicto_entidades"
REGLA_SIN_NUCLEO = "sin_nucleo"

INTENCION_INFO_CARRERA = "info_carrera"
INTENCION_SALUDO = "saludo"

_CONFIANZA_BASE: dict[str, float] = {
    REGLA_TRAMITE: 0.9,
    REGLA_CARRERA: 0.85,
    REGLA_SALUDO: 0.95,
}


class ConflictoDeUnificacionError(Exception):
    """Dos atributos incompatibles para la misma entidad (p. ej. dos carreras)."""


@dataclass(frozen=True)
class _Rasgos:
    """Estructura de rasgos acumulada mientras se recorre la consulta."""

    tramite: str | None = None
    carrera: str | None = None
    anio: int | None = None
    nucleo: bool = False
    saludo: bool = False

    def unificar(self, otro: "_Rasgos") -> "_Rasgos":
        return _Rasgos(
            tramite=_unificar_valor(self.tramite, otro.tramite),
            carrera=_unificar_valor(self.carrera, otro.carrera),
            anio=_unificar_valor(self.anio, otro.anio),
            nucleo=self.nucleo or otro.nucleo,
            saludo=self.saludo or otro.saludo,
        )


def _unificar_valor[T](a: T | None, b: T | None) -> T | None:
    if a is not None and b is not None and a != b:
        raise ConflictoDeUnificacionError(f"{a!r} ≠ {b!r}")
    return a if a is not None else b


class GramaticaIntencionesService:
    """Analizador descendente recursivo que implementa la gramática del módulo."""

    def _anio(self, simbolos: list[Simbolo], i: int) -> tuple[int, int] | None:
        """anio(N) --> [ord(N)], [marca_anio] | [marca_anio], [ord(N)]."""
        if i + 1 >= len(simbolos):
            return None
        a, b = simbolos[i], simbolos[i + 1]
        if a.categoria == CATEGORIA_ORDINAL and b.categoria == CATEGORIA_MARCA_ANIO:
            return int(a.valor), i + 2
        if a.categoria == CATEGORIA_MARCA_ANIO and b.categoria == CATEGORIA_ORDINAL:
            return int(b.valor), i + 2
        return None

    def _elemento(self, simbolos: list[Simbolo], i: int) -> tuple[_Rasgos, int]:
        anio = self._anio(simbolos, i)
        if anio is not None:
            return _Rasgos(anio=anio[0]), anio[1]
        simbolo = simbolos[i]
        if simbolo.categoria == CATEGORIA_TRAMITE:
            return _Rasgos(tramite=simbolo.valor), i + 1
        if simbolo.categoria == CATEGORIA_CARRERA:
            return _Rasgos(carrera=simbolo.valor), i + 1
        if simbolo.categoria == CATEGORIA_NUCLEO:
            return _Rasgos(nucleo=True), i + 1
        if simbolo.categoria == CATEGORIA_SALUDO:
            return _Rasgos(saludo=True), i + 1
        return _Rasgos(), i + 1

    def _cuerpo(self, simbolos: list[Simbolo], i: int) -> _Rasgos:
        """cuerpo(E) --> [] | elemento(E1), cuerpo(E2), {unificar(E1, E2, E)}."""
        if i >= len(simbolos):
            return _Rasgos()
        rasgos, siguiente = self._elemento(simbolos, i)
        return rasgos.unificar(self._cuerpo(simbolos, siguiente))

    def interpretar(self, simbolos: list[Simbolo]) -> Interpretacion:
        try:
            rasgos = self._cuerpo(simbolos, 0)
        except ConflictoDeUnificacionError:
            return self._rechazo(REGLA_CONFLICTO)

        entidades = Entidades(carrera=rasgos.carrera, anio=rasgos.anio, tramite=rasgos.tramite)
        if rasgos.tramite is not None:
            intencion, regla = rasgos.tramite, REGLA_TRAMITE
        elif rasgos.carrera is not None or rasgos.nucleo:
            intencion, regla = INTENCION_INFO_CARRERA, REGLA_CARRERA
        elif rasgos.saludo and rasgos.anio is None:
            intencion, regla = INTENCION_SALUDO, REGLA_SALUDO
        else:
            return self._rechazo(REGLA_SIN_NUCLEO)

        return Interpretacion(
            intencion=intencion,
            entidades=entidades,
            confianza=round(_CONFIANZA_BASE[regla] * self._factor_cobertura(simbolos), 2),
            aceptada=True,
            regla=regla,
        )

    @staticmethod
    def _factor_cobertura(simbolos: list[Simbolo]) -> float:
        """Penaliza la confianza según la proporción de palabras no reconocidas."""
        ruido = sum(1 for s in simbolos if s.categoria == CATEGORIA_RUIDO)
        cobertura = (len(simbolos) - ruido) / len(simbolos) if simbolos else 0.0
        return 0.5 + 0.5 * cobertura

    @staticmethod
    def _rechazo(regla: str) -> Interpretacion:
        return Interpretacion(
            intencion=INTENCION_FUERA_DE_DOMINIO,
            entidades=Entidades(),
            confianza=0.0,
            aceptada=False,
            regla=regla,
        )
