import os
from typing import Any, cast

import yaml

from src.application.services.text_morphology_service import TextMorphologyService
from src.domain.conversacion.interpretacion import (
    CATEGORIA_CARRERA,
    CATEGORIA_MARCA_ANIO,
    CATEGORIA_NUCLEO,
    CATEGORIA_ORDINAL,
    CATEGORIA_PEDIDO,
    CATEGORIA_RUIDO,
    CATEGORIA_SALUDO,
    CATEGORIA_TRAMITE,
    Simbolo,
)
from src.domain.conversacion.token import Token

# Longitud mínima de una raíz para reconocer variantes morfológicas por stem
# (evita colisiones de raíces cortas, p. ej. "mesa" / "mes").
_LONGITUD_MINIMA_STEM = 4


def _leer_yaml(path: str) -> dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        loaded: Any = yaml.safe_load(f)
    if isinstance(loaded, dict):
        return cast(dict[str, Any], loaded)
    return {}


def _como_lista(valor: object) -> list[str]:
    if isinstance(valor, list):
        return [str(item) for item in cast(list[object], valor)]
    return []


def _como_dict(valor: object) -> dict[str, object]:
    if isinstance(valor, dict):
        return {str(k): v for k, v in cast(dict[object, object], valor).items()}
    return {}


class LexicoInstitucionalService:
    """Léxico controlado del dominio: etiqueta cada palabra de la consulta con su categoría."""

    def __init__(self, morphology_service: TextMorphologyService, data_dir: str | None = None) -> None:
        self.morphology_service: TextMorphologyService = morphology_service
        self.data_dir: str = data_dir or morphology_service.data_dir
        self.frases: dict[tuple[str, ...], tuple[str, str]] = {}
        self.raices: dict[str, tuple[str, str]] = {}
        self.carreras_validas: set[str] = set()
        self._cargar()

    @property
    def longitud_maxima(self) -> int:
        return max((len(frase) for frase in self.frases), default=1)

    def _registrar(self, forma: str, categoria: str, valor: str) -> None:
        palabras = tuple(self.morphology_service.normalize(forma).split())
        if not palabras:
            return
        self.frases.setdefault(palabras, (categoria, valor))
        if len(palabras) == 1:
            raiz = self.morphology_service.nlp_gateway.lemmatize_or_stem(palabras[0])
            if len(raiz) >= _LONGITUD_MINIMA_STEM:
                self.raices.setdefault(raiz, (categoria, valor))

    def _registrar_lista(self, formas: object, categoria: str, valor: str) -> None:
        for forma in _como_lista(formas):
            self._registrar(forma, categoria, valor)

    def _registrar_carreras(self, alias: dict[str, object]) -> None:
        """Títulos oficiales de carreras.yaml + alias coloquiales del léxico, por slug."""
        carreras_data = _leer_yaml(os.path.join(self.data_dir, "content", "carreras.yaml"))
        for carrera_obj in cast(list[object], carreras_data.get("carreras", [])):
            carrera = _como_dict(carrera_obj)
            slug = str(carrera.get("slug", ""))
            if not slug:
                continue
            self.carreras_validas.add(slug)
            self._registrar(str(carrera.get("title", "")), CATEGORIA_CARRERA, slug)
            self._registrar_lista(alias.get(slug), CATEGORIA_CARRERA, slug)

    def _cargar(self) -> None:
        lexico = _leer_yaml(os.path.join(self.data_dir, "chat", "lexico.yaml"))
        # Orden de registro = prioridad: lo específico antes que lo genérico.
        for tramite, formas in _como_dict(lexico.get("tramites")).items():
            self._registrar_lista(formas, CATEGORIA_TRAMITE, tramite)
        self._registrar_carreras(_como_dict(lexico.get("carreras")))
        self._registrar_lista(lexico.get("nucleo_carrera"), CATEGORIA_NUCLEO, "carrera")
        self._registrar_lista(lexico.get("saludos"), CATEGORIA_SALUDO, "saludo")
        for numero, formas in _como_dict(lexico.get("ordinales")).items():
            self._registrar_lista(formas, CATEGORIA_ORDINAL, numero)
        self._registrar_lista(lexico.get("marcador_anio"), CATEGORIA_MARCA_ANIO, "anio")
        self._registrar_lista(lexico.get("pedidos"), CATEGORIA_PEDIDO, "pedido")

    def etiquetar(self, tokens: list[Token]) -> list[Simbolo]:
        """Convierte los tokens en símbolos léxicos, priorizando la expresión más larga.

        Las stopwords sin significado en el léxico se descartan; las palabras de
        contenido no reconocidas se marcan como RUIDO.
        """
        palabras = [t.texto_limpio for t in tokens]
        simbolos: list[Simbolo] = []
        i = 0
        while i < len(tokens):
            reconocido = False
            for n in range(min(self.longitud_maxima, len(tokens) - i), 0, -1):
                frase = tuple(palabras[i : i + n])
                if frase in self.frases:
                    categoria, valor = self.frases[frase]
                    simbolos.append(Simbolo(categoria=categoria, valor=valor, texto=" ".join(frase)))
                    i += n
                    reconocido = True
                    break
            if reconocido:
                continue
            token = tokens[i]
            if token.lema in self.raices and not token.es_stopword:
                categoria, valor = self.raices[token.lema]
                simbolos.append(Simbolo(categoria=categoria, valor=valor, texto=token.texto_limpio))
            elif not token.es_stopword:
                simbolos.append(Simbolo(categoria=CATEGORIA_RUIDO, valor="", texto=token.texto_limpio))
            i += 1
        return simbolos
