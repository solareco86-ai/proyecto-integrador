import pytest

from src.application.services.gramatica_intenciones_service import (
    REGLA_CARRERA,
    REGLA_CONFLICTO,
    REGLA_SALUDO,
    REGLA_SIN_NUCLEO,
    REGLA_TRAMITE,
    GramaticaIntencionesService,
)
from src.application.services.lexico_institucional_service import LexicoInstitucionalService
from src.application.services.text_morphology_service import TextMorphologyService
from src.domain.conversacion.interpretacion import (
    INTENCION_FUERA_DE_DOMINIO,
    Interpretacion,
)
from src.infrastructure.gateways.nltk_nlp_gateway import NltkNLPGateway


@pytest.fixture(scope="module")
def morphology() -> TextMorphologyService:
    return TextMorphologyService(nlp_gateway=NltkNLPGateway(), data_dir="data")


@pytest.fixture(scope="module")
def lexico(morphology: TextMorphologyService) -> LexicoInstitucionalService:
    return LexicoInstitucionalService(morphology_service=morphology)


def interpretar(texto: str, morphology: TextMorphologyService, lexico: LexicoInstitucionalService) -> Interpretacion:
    simbolos = lexico.etiquetar(morphology.analyze(texto).tokens)
    return GramaticaIntencionesService().interpretar(simbolos)


# --- Intenciones y entidades --------------------------------------------------


@pytest.mark.parametrize(
    ("texto", "intencion", "carrera"),
    [
        ("kiero anotarme en logistica", "inscripcion", "logistica"),
        ("¿Cuáles son los requisitos?", "inscripcion", None),
        ("que materias tiene turismo", "plan_estudios", "turismo"),
        ("cuanto dura la tecnicatura en ciencia de datos", "duracion", "ciencia-de-datos-ia"),
        ("q carreras tienen a la noche", "horarios", None),
        ("como llego a la sede", "sedes", None),
        ("cuanto cuesta? cobran algo?", "costos", None),
        ("correlativas de rrhh", "correlatividades", "recursos-humanos"),
        ("cuando son las mesas de examen", "mesas_examen", None),
        ("hay becas", "becas", None),
        ("info de higiene y seguridad", "info_carrera", "higiene-y-seguridad"),
        ("que carreras hay", "info_carrera", None),
        ("Hola, buenas tardes", "saludo", None),
    ],
)
def test_detecta_intencion_y_carrera(
    texto: str,
    intencion: str,
    carrera: str | None,
    morphology: TextMorphologyService,
    lexico: LexicoInstitucionalService,
) -> None:
    resultado = interpretar(texto, morphology, lexico)
    assert resultado.aceptada
    assert resultado.intencion == intencion
    assert resultado.entidades.carrera == carrera


@pytest.mark.parametrize(
    "texto",
    ["materias de primer año de logistica", "materias de logistica del año 1", "materias del 1er año de logistica"],
)
def test_subgramatica_de_anio_en_ambos_ordenes(
    texto: str, morphology: TextMorphologyService, lexico: LexicoInstitucionalService
) -> None:
    resultado = interpretar(texto, morphology, lexico)
    assert resultado.regla == REGLA_TRAMITE
    assert resultado.entidades.anio == 1
    assert resultado.entidades.carrera == "logistica"
    assert resultado.entidades.tramite == "plan_estudios"


def test_reglas_aplicadas(morphology: TextMorphologyService, lexico: LexicoInstitucionalService) -> None:
    assert interpretar("hola", morphology, lexico).regla == REGLA_SALUDO
    assert interpretar("turismo", morphology, lexico).regla == REGLA_CARRERA
    assert interpretar("hola, horarios?", morphology, lexico).regla == REGLA_TRAMITE


# --- Frases rechazadas --------------------------------------------------------


@pytest.mark.parametrize(
    ("texto", "regla"),
    [
        ("me gusta el futbol", REGLA_SIN_NUCLEO),
        ("primer año", REGLA_SIN_NUCLEO),
        ("", REGLA_SIN_NUCLEO),
        ("horarios de logistica y de turismo", REGLA_CONFLICTO),
        ("inscripcion y becas", REGLA_CONFLICTO),
        ("materias de primer año y de segundo año", REGLA_CONFLICTO),
    ],
)
def test_frases_rechazadas(
    texto: str, regla: str, morphology: TextMorphologyService, lexico: LexicoInstitucionalService
) -> None:
    resultado = interpretar(texto, morphology, lexico)
    assert not resultado.aceptada
    assert resultado.intencion == INTENCION_FUERA_DE_DOMINIO
    assert resultado.confianza == 0.0
    assert resultado.regla == regla


def test_confianza_baja_con_palabras_no_reconocidas(
    morphology: TextMorphologyService, lexico: LexicoInstitucionalService
) -> None:
    limpia = interpretar("horarios de logistica", morphology, lexico)
    ruidosa = interpretar("horarios logistica perro gato auto", morphology, lexico)
    assert limpia.confianza == 0.9
    assert 0.0 < ruidosa.confianza < limpia.confianza
