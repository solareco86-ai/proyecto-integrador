"""Pruebas unitarias para el Eje 1.3 — Análisis semántico y clasificación de intenciones.

Cubre:
- Detección de cada intención definida en intenciones.yaml.
- Extracción de entidades y detección de carreras.
- Consulta fuera de dominio → fallback.
- Intenciones sin datos (becas, mesas, correlatividades) → derivación a Secretaría.
- Ejemplo de gramática CFG/DCG (estructura VERBO + ENTIDAD).
"""

from __future__ import annotations

import os

import pytest

from src.application.services.intent_classification_service import IntentClassificationService
from src.application.services.text_morphology_service import TextMorphologyService
from src.domain.conversacion.intencion import Intencion
from src.infrastructure.gateways.nltk_nlp_gateway import NltkNLPGateway

DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "data")


@pytest.fixture()
def intent_service() -> IntentClassificationService:
    return IntentClassificationService(data_dir=DATA_DIR)


@pytest.fixture()
def morph_service() -> TextMorphologyService:
    return TextMorphologyService(nlp_gateway=NltkNLPGateway(), data_dir=DATA_DIR)


def _normalize_and_classify(
    morph: TextMorphologyService,
    intent_svc: IntentClassificationService,
    text: str,
) -> Intencion:
    """Helper: normaliza y clasifica en un paso."""
    normalizado = morph.normalize(text)
    return intent_svc.classify(normalizado)


# -- Tests de detección de intenciones -----------------------------------------


class TestIntentDetection:
    def test_consulta_carreras(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Qué carreras tienen?")
        assert result.nombre == "consulta_carreras"
        assert result.confianza >= 0.8

    def test_inscripcion(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "Quiero inscribirme")
        assert result.nombre == "inscripcion"

    def test_horarios(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿A qué hora se cursa?")
        assert result.nombre == "horarios"

    def test_ubicacion(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Dónde queda el instituto?")
        assert result.nombre == "ubicacion"

    def test_contacto(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Cuál es el mail de contacto?")
        assert result.nombre == "contacto"

    def test_modalidad(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Es presencial o virtual?")
        assert result.nombre == "modalidad"

    def test_duracion(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Cuánto dura la carrera?")
        assert result.nombre == "duracion"

    def test_gratuidad(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Cuánto cuesta?")
        assert result.nombre == "gratuidad"

    def test_saludo(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "Hola, buen día")
        assert result.nombre == "saludo"
        assert result.confianza == 1.0


# -- Tests de extracción de entidades y carreras --------------------------------


class TestEntityExtraction:
    def test_detecta_carrera_por_sinonimo(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        """El léxico debe detectar 'logistica' como carrera vía sinónimos."""
        result = _normalize_and_classify(
            morph_service, intent_service, "Quiero anotarme en logística",
        )
        assert result.carrera_detectada == "logistica"
        assert "carrera" in result.entidades

    def test_detecta_carrera_ia(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(
            morph_service, intent_service, "Info de ciencia de datos",
        )
        assert result.carrera_detectada == "ciencia-de-datos-ia"

    def test_info_carrera_respuesta_template(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        """info_carrera debe usar el template de respuesta con el nombre oficial."""
        normalizado = morph_service.normalize("Quiero saber de hotelería")
        intencion = intent_service.classify(normalizado)
        respuesta, sources = intent_service.get_response(intencion)
        assert "Hotelería" in respuesta
        assert "/carreras" in sources


# -- Tests de derivación a Secretaría (§7.5) -----------------------------------


class TestDerivacionSecretaria:
    def test_becas_deriva_secretaria(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Hay becas disponibles?")
        assert result.nombre == "becas"
        respuesta, _ = intent_service.get_response(result)
        assert "isft199@abc.gob.ar" in respuesta

    def test_mesas_examen_deriva_secretaria(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Cuándo son las mesas de examen?")
        assert result.nombre == "mesas_de_examen"
        respuesta, _ = intent_service.get_response(result)
        assert "isft199@abc.gob.ar" in respuesta

    def test_correlatividades_deriva_secretaria(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(morph_service, intent_service, "¿Cuáles son las correlatividades?")
        assert result.nombre == "correlatividades"
        respuesta, _ = intent_service.get_response(result)
        assert "isft199@abc.gob.ar" in respuesta


# -- Test de fallback (fuera de dominio) ----------------------------------------


class TestFallback:
    def test_consulta_fuera_de_dominio(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        result = _normalize_and_classify(
            morph_service, intent_service, "¿Cómo está el clima hoy?",
        )
        assert result.nombre == "fallback"
        assert result.confianza == 0.0

    def test_texto_vacio(self, intent_service: IntentClassificationService) -> None:
        result = intent_service.classify("")
        assert result.nombre == "fallback"


# -- Test de gramática CFG/DCG -------------------------------------------------


class TestGramaticaCFG:
    def test_estructura_verbo_entidad(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        """Verifica que la CFG detecte la estructura VERBO_CONSULTA + ENTIDAD.

        Frase: 'quiero inscribirme' → S → VERBO('quiero') ENTIDAD('inscribirme')
        La regla de la gramática: S → VERBO_CONSULTA ENTIDAD
        """
        result = _normalize_and_classify(morph_service, intent_service, "quiero inscribirme")
        assert result.nombre == "inscripcion"

    def test_estructura_verbo_entidad_complemento(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        """Verifica la regla S → VERBO_CONSULTA ENTIDAD COMPLEMENTO.

        Frase: 'quiero inscribirme en logistica'
        Derivación: S → VERBO('quiero') ENTIDAD('inscribirme') COMPLEMENTO(PREP('en') CARRERA('logistica'))
        """
        result = _normalize_and_classify(
            morph_service, intent_service, "quiero inscribirme en logística",
        )
        assert result.nombre == "inscripcion"
        assert result.carrera_detectada == "logistica"

    def test_dcg_consulta_entidad_carrera(
        self, morph_service: TextMorphologyService, intent_service: IntentClassificationService,
    ) -> None:
        """Ejemplo DCG: consulta(info(carrera(turismo))) --> [info, de, turismo].

        La gramática de cláusulas definidas modela:
          consulta(Intent) --> verbo_consulta, [de], entidad(E), { Intent = info(E) }.
          entidad(carrera(X)) --> [X], { es_carrera(X) }.
        """
        result = _normalize_and_classify(morph_service, intent_service, "info de turismo")
        assert result.carrera_detectada == "turismo"
