import os
from typing import Any, cast

import yaml

from src.domain.conversacion.interpretacion import INTENCION_FUERA_DE_DOMINIO, Interpretacion
from src.domain.conversacion.respuesta import Respuesta

_UMBRAL_POR_DEFECTO = 0.6


def _leer_yaml(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        loaded: Any = yaml.safe_load(f)
    if isinstance(loaded, dict):
        return cast(dict[str, Any], loaded)
    return {}


def _como_dict(valor: object) -> dict[str, object]:
    if isinstance(valor, dict):
        return {str(k): v for k, v in cast(dict[object, object], valor).items()}
    return {}


def _como_lista(valor: object) -> list[str]:
    if isinstance(valor, list):
        return [str(item) for item in cast(list[object], valor)]
    return []


def _enumerar(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " y " + items[-1]


def _minuscula_inicial(texto: str) -> str:
    return texto[:1].lower() + texto[1:]


class _Variables(dict[str, str]):
    """Deja intacto un marcador desconocido en lugar de fallar."""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


class RespuestasChatService:
    """Construye la respuesta al usuario solo con datos oficiales de data/."""

    def __init__(self, data_dir: str | None = None) -> None:
        self.data_dir: str = data_dir or os.getenv("DATA_DIR", "data")
        config = _leer_yaml(os.path.join(self.data_dir, "chat", "intenciones.yaml"))
        brand = _leer_yaml(os.path.join(self.data_dir, "config", "brand.yaml"))
        carreras_data = _leer_yaml(os.path.join(self.data_dir, "content", "carreras.yaml"))

        self.umbral: float = float(config.get("umbral_confianza", _UMBRAL_POR_DEFECTO))
        self.intenciones: dict[str, object] = _como_dict(config.get("intenciones"))
        self.derivacion: dict[str, object] = _como_dict(config.get("derivacion"))
        self.fuera_de_dominio: dict[str, object] = _como_dict(config.get("fuera_de_dominio"))
        self.email: str = str(brand.get("contactEmail", ""))
        self.carreras: dict[str, dict[str, object]] = {}
        for carrera_obj in cast(list[object], carreras_data.get("carreras", [])):
            carrera = _como_dict(carrera_obj)
            if carrera.get("slug"):
                self.carreras[str(carrera["slug"])] = carrera

    def _variables(self, carrera: dict[str, object] | None) -> _Variables:
        variables = _Variables(
            email=self.email,
            lista_carreras=_enumerar([str(c.get("title", "")) for c in self.carreras.values()]),
        )
        if carrera is not None:
            for campo in ("title", "slug", "duracion", "titulo_otorgado", "resolucion"):
                variables[campo] = str(carrera.get(campo, ""))
            variables["modalidad"] = _minuscula_inicial(str(carrera.get("modalidad", "")))
            variables["turno"] = _minuscula_inicial(str(carrera.get("turno", "")))
            variables["materias_destacadas"] = _enumerar(_como_lista(carrera.get("materias_destacadas")))
        return variables

    def _armar(
        self, plantilla: dict[str, object], sufijo: str, intencion: str, confianza: float, variables: _Variables
    ) -> Respuesta | None:
        texto = plantilla.get(f"reply{sufijo}")
        if texto is None:
            return None
        fuentes = _como_lista(plantilla.get(f"sources{sufijo}", plantilla.get("sources")))
        return Respuesta(
            texto=str(texto).format_map(variables),
            intencion=intencion,
            fuentes=[fuente.format_map(variables) for fuente in fuentes],
            confianza=confianza,
        )

    def _derivar(self, intencion: str, confianza: float) -> Respuesta:
        respuesta = self._armar(self.derivacion, "", intencion, confianza, self._variables(None))
        return respuesta or Respuesta(texto=self.email, intencion=intencion, fuentes=[], confianza=confianza)

    @staticmethod
    def _sufijo(interpretacion: Interpretacion, carrera: dict[str, object] | None) -> str:
        """Elige la plantilla según la entidad más específica detectada."""
        if interpretacion.entidades.anio is not None:
            return "_anio"
        if carrera is not None:
            return "_carrera"
        return ""

    def responder(self, interpretacion: Interpretacion) -> Respuesta:
        if not interpretacion.aceptada:
            respuesta = self._armar(self.fuera_de_dominio, "", INTENCION_FUERA_DE_DOMINIO, 0.0, self._variables(None))
            return respuesta or self._derivar(INTENCION_FUERA_DE_DOMINIO, 0.0)

        intencion, confianza = interpretacion.intencion, interpretacion.confianza
        if confianza < self.umbral or intencion not in self.intenciones:
            return self._derivar(intencion, confianza)

        carrera = self.carreras.get(interpretacion.entidades.carrera or "")
        sufijo = self._sufijo(interpretacion, carrera)
        plantilla = _como_dict(self.intenciones[intencion])
        variables = self._variables(carrera)
        respuesta = self._armar(plantilla, sufijo, intencion, confianza, variables)
        if respuesta is None and sufijo == "_carrera":
            # El dato general vale para todas las carreras (p. ej. la sede).
            respuesta = self._armar(plantilla, "", intencion, confianza, variables)
        # Sin plantilla para el año pedido: el sitio no publica ese dato -> se deriva.
        return respuesta or self._derivar(intencion, confianza)
