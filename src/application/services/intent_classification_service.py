"""Servicio de clasificación de intenciones mediante léxico controlado y gramática CFG.

Implementa análisis semántico basado en:
- Gramática independiente del contexto (CFG) para la estructura de la consulta.
- Gramática de cláusulas definidas (DCG) como caso especial documentado.
- Léxico del dominio institucional (data/chat/lexico.yaml).
- Catálogo de intenciones con patrones (data/chat/intenciones.yaml).
"""

from __future__ import annotations

import os
import re
from typing import Any, cast

import yaml

from src.domain.conversacion.intencion import Intencion

# ---------------------------------------------------------------------------
# Gramática independiente del contexto (CFG) del dominio institucional
# ---------------------------------------------------------------------------
# S        → VERBO_CONSULTA ENTIDAD
# S        → VERBO_CONSULTA ENTIDAD COMPLEMENTO
# S        → SALUDO
# ENTIDAD  → CARRERA | TRAMITE | ATRIBUTO
# ATRIBUTO → "horario" | "ubicacion" | "contacto" | "modalidad" | "duracion"
# COMPLEMENTO → PREP CARRERA | PREP ATRIBUTO | ε
# VERBO_CONSULTA → "quiero" | "necesito" | "busco" | "cual" | "que" | "como"
# PREP     → "de" | "en" | "sobre" | "para"
# SALUDO   → "hola" | "buen dia" | "buenas tardes" | "buenas noches"
#
# Gramática de cláusulas definidas (DCG) — ejemplo formal:
#   consulta(Intent) --> verbo_consulta, entidad(E), { Intent = info(E) }.
#   consulta(Intent) --> verbo_consulta, entidad(E), complemento(C),
#                        { Intent = info(E, C) }.
#   entidad(carrera(X)) --> [X], { es_carrera(X) }.
#   entidad(tramite(X)) --> [X], { es_tramite(X) }.
#   verbo_consulta --> [quiero].
#   verbo_consulta --> [necesito].
# ---------------------------------------------------------------------------

_VERBOS_CONSULTA: set[str] = {
    "quiero", "necesito", "busco", "cual", "que", "como",
    "donde", "cuando", "cuanto", "puedo", "hay", "tienen",
    "ofrecen", "informacion", "info", "contame", "decime",
}

_PREPOSICIONES: set[str] = {"de", "en", "sobre", "para", "por", "con", "a"}


class IntentClassificationService:
    """Clasifica intenciones y extrae entidades de consultas textuales."""

    def __init__(self, data_dir: str | None = None) -> None:
        if not data_dir or (data_dir == "data" and "DATA_DIR" in os.environ):
            self.data_dir: str = os.getenv("DATA_DIR", "data")
        else:
            self.data_dir = data_dir

        self.lexico: dict[str, Any] = self._load_yaml("lexico.yaml")
        self.intenciones_data: dict[str, Any] = self._load_yaml("intenciones.yaml")

        # Índice invertido: sinónimo → (slug, nombre_oficial)
        self.career_index: dict[str, tuple[str, str]] = self._build_career_index()
        # Índice de entidades del léxico: palabra → categoría
        self.entity_index: dict[str, str] = self._build_entity_index()

    # -- Carga de datos -------------------------------------------------------

    def _load_yaml(self, filename: str) -> dict[str, Any]:
        path = os.path.join(self.data_dir, "chat", filename)
        if not os.path.exists(path):
            return {}
        with open(path, encoding="utf-8") as f:
            loaded: Any = yaml.safe_load(f)
            if isinstance(loaded, dict):
                return cast(dict[str, Any], loaded)
            return {}

    def _build_career_index(self) -> dict[str, tuple[str, str]]:
        """Construye índice invertido sinónimo → (slug, nombre)."""
        index: dict[str, tuple[str, str]] = {}
        raw_carreras: Any = self.lexico.get("carreras", {})
        if not isinstance(raw_carreras, dict):
            return index
        carreras: dict[object, object] = cast(dict[object, object], raw_carreras)
        for slug_obj, info_obj in carreras.items():
            slug = str(slug_obj)
            if not isinstance(info_obj, dict):
                continue
            info: dict[object, object] = cast(dict[object, object], info_obj)
            nombre = str(info.get("nombre", slug))
            # El slug sin guiones también es buscable
            index[slug.replace("-", " ")] = (slug, nombre)
            raw_sins: Any = info.get("sinonimos", [])
            if isinstance(raw_sins, list):
                sins: list[object] = cast(list[object], raw_sins)
                for s in sins:
                    index[str(s).lower()] = (slug, nombre)
        return index

    def _build_entity_index(self) -> dict[str, str]:
        """Construye índice palabra → categoría de entidad."""
        index: dict[str, str] = {}
        raw_entidades: Any = self.lexico.get("entidades", {})
        if not isinstance(raw_entidades, dict):
            return index
        entidades: dict[object, object] = cast(dict[object, object], raw_entidades)
        for cat_obj, words_obj in entidades.items():
            cat = str(cat_obj)
            if isinstance(words_obj, list):
                words: list[object] = cast(list[object], words_obj)
                for w in words:
                    index[str(w).lower()] = cat
        return index

    # -- Clasificación --------------------------------------------------------

    def classify(self, texto_normalizado: str) -> Intencion:
        """Clasifica la intención de un texto ya normalizado (sin tildes, minúsculas).

        Pipeline:
        1. Detectar carrera mencionada (léxico controlado).
        2. Intentar match por patrones de intención (CFG simplificada).
        3. Analizar estructura gramatical: verbo + entidad + complemento.
        4. Fallback si no se detecta intención.
        """
        texto = texto_normalizado.strip().lower()
        if not texto:
            return self._fallback()

        # 1. Detectar carrera mencionada
        carrera_slug, carrera_nombre = self._detect_career(texto)

        # 2. Match por patrones definidos en intenciones.yaml
        matched_intent = self._match_patterns(texto)
        if matched_intent is not None:
            return self._build_intencion(
                matched_intent, texto, carrera_slug, carrera_nombre,
            )

        # 3. Análisis CFG: extraer entidades del léxico y derivar intención
        cfg_intent = self._cfg_analysis(texto, carrera_slug)
        if cfg_intent is not None:
            return self._build_intencion(
                cfg_intent, texto, carrera_slug, carrera_nombre,
            )

        # 4. Si se detectó carrera pero no intención específica → info_carrera
        if carrera_slug:
            return self._build_intencion(
                "info_carrera", texto, carrera_slug, carrera_nombre,
            )

        return self._fallback()

    def _detect_career(self, texto: str) -> tuple[str | None, str | None]:
        """Busca la primera carrera mencionada ordenando sinónimos de mayor a menor longitud."""
        sorted_synonyms: list[tuple[str, tuple[str, str]]] = sorted(
            self.career_index.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        )
        for synonym, (slug, nombre) in sorted_synonyms:
            pattern = r"\b" + re.escape(synonym) + r"\b"
            if re.search(pattern, texto):
                return slug, nombre
        return None, None

    def _match_patterns(self, texto: str) -> str | None:
        """Busca coincidencia con los patrones definidos en intenciones.yaml."""
        raw_intenciones: Any = self.intenciones_data.get("intenciones", {})
        if not isinstance(raw_intenciones, dict):
            return None

        intenciones: dict[object, object] = cast(dict[object, object], raw_intenciones)
        best_match: str | None = None
        best_length: int = 0

        for intent_obj, config_obj in intenciones.items():
            if not isinstance(config_obj, dict):
                continue
            config: dict[object, object] = cast(dict[object, object], config_obj)
            raw_patterns: Any = config.get("patrones", [])
            if not isinstance(raw_patterns, list):
                continue
            patterns: list[object] = cast(list[object], raw_patterns)
            for pattern_obj in patterns:
                pattern_str = str(pattern_obj).lower()
                if pattern_str in texto and len(pattern_str) > best_length:
                    best_match = str(intent_obj)
                    best_length = len(pattern_str)

        return best_match

    def _cfg_analysis(self, texto: str, carrera_slug: str | None) -> str | None:
        """Análisis CFG simplificado: busca estructura VERBO + ENTIDAD."""
        words = texto.split()
        # Verificar presencia de verbo de consulta
        has_verb = any(w in _VERBOS_CONSULTA for w in words)
        if not has_verb and not carrera_slug:
            return None

        # Buscar entidades del léxico en el texto
        matched_entities: list[str] = []
        for word in words:
            if word in _PREPOSICIONES or word in _VERBOS_CONSULTA:
                continue
            cat = self.entity_index.get(word)
            if cat and cat not in matched_entities:
                matched_entities.append(cat)

        # Mapear categoría de entidad → intención
        category_intent_map: dict[str, str] = {
            "tramites": "inscripcion",
            "horarios": "horarios",
            "ubicacion": "ubicacion",
            "contacto": "contacto",
            "correlatividades": "correlatividades",
            "mesas_de_examen": "mesas_de_examen",
            "becas": "becas",
            "modalidad": "modalidad",
            "duracion": "duracion",
        }

        for entity_cat in matched_entities:
            mapped = category_intent_map.get(entity_cat)
            if mapped:
                return mapped

        return None

    def _build_intencion(
        self,
        intent_name: str,
        texto: str,
        carrera_slug: str | None,
        carrera_nombre: str | None,
    ) -> Intencion:
        """Construye la entidad Intencion con la respuesta y datos del YAML."""
        raw_intenciones: Any = self.intenciones_data.get("intenciones", {})
        if not isinstance(raw_intenciones, dict):
            return self._fallback()
        intenciones: dict[object, object] = cast(dict[object, object], raw_intenciones)
        raw_config: Any = intenciones.get(intent_name, {})
        if not isinstance(raw_config, dict):
            return self._fallback()
        config: dict[object, object] = cast(dict[object, object], raw_config)

        raw_confidence: Any = config.get("confidence", 0.7)
        confidence = float(str(raw_confidence))

        # Extraer entidades detectadas del texto
        detected_entities: list[str] = []
        words = texto.split()
        for word in words:
            cat = self.entity_index.get(word)
            if cat and cat not in detected_entities:
                detected_entities.append(cat)
        if carrera_slug and "carrera" not in detected_entities:
            detected_entities.append("carrera")

        return Intencion(
            nombre=intent_name,
            entidades=detected_entities,
            carrera_detectada=carrera_slug,
            confianza=confidence,
        )

    def get_response(self, intencion: Intencion) -> tuple[str, list[str]]:
        """Obtiene la respuesta textual y fuentes para una intención clasificada.

        Returns:
            Tupla (respuesta, fuentes).
        """
        raw_intenciones: Any = self.intenciones_data.get("intenciones", {})
        if not isinstance(raw_intenciones, dict):
            return self._fallback_response()

        intenciones: dict[object, object] = cast(dict[object, object], raw_intenciones)
        raw_config: Any = intenciones.get(intencion.nombre, {})
        if not isinstance(raw_config, dict):
            return self._fallback_response()
        config: dict[object, object] = cast(dict[object, object], raw_config)

        # Manejar respuesta con template (info_carrera)
        raw_respuesta: Any = config.get("respuesta_template") or config.get("respuesta", "")
        respuesta = str(raw_respuesta)

        if intencion.carrera_detectada and "{carrera}" in respuesta:
            # Obtener nombre oficial de la carrera
            raw_carreras: Any = self.lexico.get("carreras", {})
            nombre_carrera = intencion.carrera_detectada
            if isinstance(raw_carreras, dict):
                carreras: dict[object, object] = cast(dict[object, object], raw_carreras)
                raw_info: Any = carreras.get(intencion.carrera_detectada, {})
                if isinstance(raw_info, dict):
                    info: dict[object, object] = cast(dict[object, object], raw_info)
                    nombre_carrera = str(info.get("nombre", intencion.carrera_detectada))
            respuesta = respuesta.replace("{carrera}", nombre_carrera)
            respuesta = respuesta.replace("{slug}", intencion.carrera_detectada)

        raw_sources: Any = config.get("sources", [])
        sources: list[str] = []
        if isinstance(raw_sources, list):
            sources_list: list[object] = cast(list[object], raw_sources)
            for s in sources_list:
                sources.append(str(s))

        return respuesta, sources

    def _fallback(self) -> Intencion:
        return Intencion(nombre="fallback", entidades=[], carrera_detectada=None, confianza=0.0)

    def _fallback_response(self) -> tuple[str, list[str]]:
        raw_fallback: Any = self.intenciones_data.get("fallback", {})
        if isinstance(raw_fallback, dict):
            fb: dict[object, object] = cast(dict[object, object], raw_fallback)
            resp = str(fb.get("respuesta", ""))
            raw_src: Any = fb.get("sources", [])
            src: list[str] = []
            if isinstance(raw_src, list):
                src_list: list[object] = cast(list[object], raw_src)
                src = [str(s) for s in src_list]
            return resp, src
        return "No pude procesar tu consulta. Escribí a isft199@abc.gob.ar.", []
