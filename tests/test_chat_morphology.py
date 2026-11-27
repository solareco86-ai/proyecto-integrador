import pytest

from src.application.gateways.nlp_gateway import NLPProcessorGateway
from src.application.services.text_morphology_service import TextMorphologyService
from src.infrastructure.gateways.nltk_nlp_gateway import NltkNLPGateway


@pytest.fixture
def nlp_gateway() -> NLPProcessorGateway:
    return NltkNLPGateway()


@pytest.fixture
def morphology_service(nlp_gateway: NLPProcessorGateway) -> TextMorphologyService:
    return TextMorphologyService(nlp_gateway=nlp_gateway, data_dir="data")


def test_normalizacion_elimina_tildes_y_minusculas(morphology_service: TextMorphologyService) -> None:
    texto = "¡INFORMACIÓN SOBRE LOGÍSTICA Y EDUCACIÓN TÉCNICA!"
    norm = morphology_service.normalize(texto)
    assert norm == "informacion sobre logistica y educacion tecnica"


def test_normalizacion_expande_abreviaturas_y_modismos(morphology_service: TextMorphologyService) -> None:
    texto = "q carreras tienen y xq cobran inscripcion"
    norm = morphology_service.normalize(texto)
    assert "que carreras tienen" in norm
    assert "por que" in norm


def test_consulta_real_kiero_anotarme_en_logistica(morphology_service: TextMorphologyService) -> None:
    texto = "kiero anotarme en logistica"
    analizado = morphology_service.analyze(texto)
    assert "quiero" in analizado.texto_normalizado
    assert "inscribirme" in analizado.texto_normalizado
    assert "logistica" in analizado.texto_normalizado
    assert len(analizado.tokens) >= 4


def test_consulta_real_q_carreras_tienen_a_la_noche(morphology_service: TextMorphologyService) -> None:
    texto = "q carreras tienen a la noche"
    analizado = morphology_service.analyze(texto)
    assert analizado.texto_normalizado.startswith("que carreras")
    tokens_textos = [t.texto_limpio for t in analizado.tokens]
    assert "que" in tokens_textos
    assert "carreras" in tokens_textos
    # Verificar detección de stopwords
    stop_flags = [t.es_stopword for t in analizado.tokens if t.texto_limpio in ("que", "a", "la")]
    assert all(stop_flags)


def test_tokenizacion_aislada(nlp_gateway: NLPProcessorGateway) -> None:
    tokens = nlp_gateway.tokenize("hola mundo 123 prueba")
    assert tokens == ["hola", "mundo", "123", "prueba"]
    assert nlp_gateway.tokenize("") == []


def test_stemming_lematizacion_aislada(nlp_gateway: NLPProcessorGateway) -> None:
    # En español, 'carreras' se reduce a su raíz morfológica 'carrer'
    stem = nlp_gateway.lemmatize_or_stem("carreras")
    assert stem == "carrer"
    assert nlp_gateway.lemmatize_or_stem("") == ""


def test_pos_tagging_aislado(nlp_gateway: NLPProcessorGateway) -> None:
    tokens = ["el", "instituto", "ofrece", "carreras", "gratuitas", "en", "2026"]
    tagged = nlp_gateway.pos_tag(tokens)
    tag_dict = dict(tagged)
    assert tag_dict["el"] == "DET"
    assert tag_dict["en"] == "ADP"
    assert tag_dict["2026"] == "NUM"
    assert tag_dict["ofrece"] == "VERB"
