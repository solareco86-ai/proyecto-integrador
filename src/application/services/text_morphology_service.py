import os
import re
import unicodedata
from typing import Any, cast

import yaml

from src.application.gateways.nlp_gateway import NLPProcessorGateway
from src.domain.conversacion.texto_analizado import TextoAnalizado
from src.domain.conversacion.token import Token


class TextMorphologyService:
    def __init__(
        self,
        nlp_gateway: NLPProcessorGateway,
        data_dir: str | None = None,
    ) -> None:
        self.nlp_gateway: NLPProcessorGateway = nlp_gateway
        if not data_dir or (data_dir == "data" and "DATA_DIR" in os.environ):
            self.data_dir = os.getenv("DATA_DIR", "data")
        else:
            self.data_dir = data_dir

        self.stopwords: set[str] = self._load_stopwords()
        self.abreviaturas: dict[str, str] = self._load_abreviaturas()

    def _load_stopwords(self) -> set[str]:
        path = os.path.join(self.data_dir, "chat", "stopwords.yaml")
        if not os.path.exists(path):
            return set()
        with open(path, encoding="utf-8") as f:
            data_obj: Any = yaml.safe_load(f)
            if isinstance(data_obj, dict):
                data_dict: dict[object, object] = cast(dict[object, object], data_obj)
                raw_list = data_dict.get("stopwords", [])
                if isinstance(raw_list, list):
                    cast_list: list[object] = cast(list[object], raw_list)
                    return {str(item).lower() for item in cast_list}
            return set()

    def _load_abreviaturas(self) -> dict[str, str]:
        path = os.path.join(self.data_dir, "chat", "abreviaturas.yaml")
        if not os.path.exists(path):
            return {}
        with open(path, encoding="utf-8") as f:
            data_obj: Any = yaml.safe_load(f)
            if isinstance(data_obj, dict):
                data_dict: dict[object, object] = cast(dict[object, object], data_obj)
                raw_dict = data_dict.get("abreviaturas", {})
                if isinstance(raw_dict, dict):
                    cast_dict: dict[object, object] = cast(dict[object, object], raw_dict)
                    return {str(k).lower(): str(v).lower() for k, v in cast_dict.items()}
            return {}

    def strip_accents(self, text: str) -> str:
        """Remueve tildes y diacríticos preservando la eñe."""
        # Protegemos la eñe antes de normalizar
        replaced = text.replace("ñ", "__enye__").replace("Ñ", "__enye__")
        nfkd_form = unicodedata.normalize("NFKD", replaced)
        without_accents = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        return without_accents.replace("__enye__", "ñ")

    def expand_abbreviations(self, text: str) -> str:
        """Expande abreviaturas y modismos informales definidos en data/chat/abreviaturas.yaml."""
        tokens = text.split()
        expanded_tokens: list[str] = []
        for token in tokens:
            lower_token = token.lower()
            if lower_token in self.abreviaturas:
                expanded_tokens.append(self.abreviaturas[lower_token])
            else:
                expanded_tokens.append(token)
        return " ".join(expanded_tokens)

    def normalize(self, text: str) -> str:
        """
        Fase de normalización:
        1. Minúsculas
        2. Expansión de abreviaturas/modismos
        3. Remoción de tildes
        4. Limpieza de puntuación repetida o símbolos innecesarios
        """
        if not text:
            return ""
        # 1. Minúsculas
        clean = text.lower().strip()
        # 2. Abreviaturas y modismos
        clean = self.expand_abbreviations(clean)
        # 3. Remover tildes
        clean = self.strip_accents(clean)
        # 4. Limpieza de signos de puntuación dejando palabras y espacios
        clean = re.sub(r"[^\w\sñ]", " ", clean, flags=re.UNICODE)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean

    def analyze(self, text: str) -> TextoAnalizado:
        """Ejecuta el pipeline completo: normalización, tokenización, lematización/stemming y POS tagging."""
        texto_norm = self.normalize(text)
        raw_tokens = self.nlp_gateway.tokenize(texto_norm)
        pos_tagged = self.nlp_gateway.pos_tag(raw_tokens)

        tokens_domain: list[Token] = []
        for word, pos_tag in pos_tagged:
            stem_or_lemma = self.nlp_gateway.lemmatize_or_stem(word)
            is_stop = word in self.stopwords
            tokens_domain.append(
                Token(
                    texto_original=word,
                    texto_limpio=word,
                    lema=stem_or_lemma,
                    pos=pos_tag,
                    es_stopword=is_stop,
                )
            )

        return TextoAnalizado(
            texto_original=text,
            texto_normalizado=texto_norm,
            tokens=tokens_domain,
        )
