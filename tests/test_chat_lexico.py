from pathlib import Path

import pytest
import yaml

from src.application.services.lexico_institucional_service import LexicoInstitucionalService
from src.application.services.text_morphology_service import TextMorphologyService
from src.domain.conversacion.interpretacion import CATEGORIA_CARRERA, CATEGORIA_RUIDO, CATEGORIA_TRAMITE, Simbolo
from src.infrastructure.gateways.nltk_nlp_gateway import NltkNLPGateway


@pytest.fixture(scope="module")
def morphology() -> TextMorphologyService:
    return TextMorphologyService(nlp_gateway=NltkNLPGateway(), data_dir="data")


@pytest.fixture(scope="module")
def lexico(morphology: TextMorphologyService) -> LexicoInstitucionalService:
    return LexicoInstitucionalService(morphology_service=morphology)


# --- Léxico controlado -------------------------------------------------------


def test_alias_del_lexico_apuntan_a_slugs_de_carreras_yaml(lexico: LexicoInstitucionalService) -> None:
    with open("data/chat/lexico.yaml", encoding="utf-8") as f:
        alias: dict[str, list[str]] = yaml.safe_load(f)["carreras"]
    assert set(alias) <= lexico.carreras_validas
    assert len(lexico.carreras_validas) == 6


def test_titulo_oficial_se_reconoce_desde_carreras_yaml(
    morphology: TextMorphologyService, lexico: LexicoInstitucionalService
) -> None:
    tokens = morphology.analyze("Tecnicatura Superior en Hotelería").tokens
    assert lexico.etiquetar(tokens) == [
        Simbolo(categoria=CATEGORIA_CARRERA, valor="hoteleria", texto="tecnicatura superior en hoteleria")
    ]


def test_variante_morfologica_se_reconoce_por_raiz(
    morphology: TextMorphologyService, lexico: LexicoInstitucionalService
) -> None:
    simbolos = lexico.etiquetar(morphology.analyze("inscribimos").tokens)
    assert simbolos[0].categoria == CATEGORIA_TRAMITE
    assert simbolos[0].valor == "inscripcion"


def test_palabra_desconocida_es_ruido_y_stopword_se_descarta(
    morphology: TextMorphologyService, lexico: LexicoInstitucionalService
) -> None:
    simbolos = lexico.etiquetar(morphology.analyze("de la futbol").tokens)
    assert [s.categoria for s in simbolos] == [CATEGORIA_RUIDO]


def test_lexico_sin_archivos_queda_vacio(morphology: TextMorphologyService, tmp_path: Path) -> None:
    vacio = LexicoInstitucionalService(morphology_service=morphology, data_dir=str(tmp_path))
    assert vacio.frases == {}
    assert vacio.longitud_maxima == 1
    (tmp_path / "chat").mkdir()
    (tmp_path / "chat" / "lexico.yaml").write_text("- no es un mapa\n", encoding="utf-8")
    assert LexicoInstitucionalService(morphology_service=morphology, data_dir=str(tmp_path)).frases == {}
