import re
from collections.abc import Callable
from typing import Any, cast

from nltk.stem.snowball import SpanishStemmer

from src.application.gateways.nlp_gateway import NLPProcessorGateway

# Constantes a nivel de módulo para reglas morfológicas y POS tagging
_VERB_ENDINGS: tuple[str, ...] = (
    "ar", "er", "ir", "ando", "iendo", "ado", "ido", "aron", "ieron",
    "aba", "abas", "abamos", "aban", "ia", "ias", "iamos", "ian",
    "an", "en", "amos", "emos", "imos", "e", "aste", "o", "io",
)
_ADJ_ENDINGS: tuple[str, ...] = (
    "al", "ales", "ico", "ica", "icos", "icas", "oso", "osa", "osos", "osas", "ble", "bles",
)
_ADV_WORDS: frozenset[str] = frozenset({
    "no", "si", "muy", "mas", "menos", "bien", "mal", "ya", "hoy", "tarde", "temprano", "cerca", "lejos",
})
_PRON_WORDS: frozenset[str] = frozenset({
    "yo", "tu", "el", "ella", "nosotros", "vosotros", "ellos", "ellas",
    "me", "te", "se", "nos", "les", "que", "quien",
})
_ADP_WORDS: frozenset[str] = frozenset({
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre",
    "hacia", "hasta", "para", "por", "segun", "sin", "so", "sobre", "tras",
})
_DET_WORDS: frozenset[str] = frozenset({
    "el", "la", "los", "las", "un", "una", "unos", "unas", "este", "esta", "estos", "estas",
    "ese", "esa", "esos", "esas", "aquel", "aquella",
})


def _classify_token(lower: str) -> str:
    """Clasifica un token en una categoría gramatical (Universal POS simplificado)."""
    if lower.isdigit():
        return "NUM"
    if lower in _ADP_WORDS:
        return "ADP"
    if lower in _DET_WORDS:
        return "DET"
    if lower in _PRON_WORDS:
        return "PRON"
    if lower in _ADV_WORDS or lower.endswith("mente"):
        return "ADV"
    if len(lower) > 3:
        if lower.endswith(_VERB_ENDINGS):
            return "VERB"
        if lower.endswith(_ADJ_ENDINGS):
            return "ADJ"
    return "NOUN"


class NltkNLPGateway(NLPProcessorGateway):
    def __init__(self) -> None:
        self.stemmer: SpanishStemmer = SpanishStemmer()
        # Patrón simple de tokenización por palabras y números
        self.token_pattern: re.Pattern[str] = re.compile(r"\b\w+\b", re.UNICODE)

    @property
    def verb_endings(self) -> tuple[str, ...]:
        return _VERB_ENDINGS

    @property
    def adj_endings(self) -> tuple[str, ...]:
        return _ADJ_ENDINGS

    @property
    def adv_words(self) -> set[str]:
        return set(_ADV_WORDS)

    @property
    def pron_words(self) -> set[str]:
        return set(_PRON_WORDS)

    @property
    def adp_words(self) -> set[str]:
        return set(_ADP_WORDS)

    @property
    def det_words(self) -> set[str]:
        return set(_DET_WORDS)

    def tokenize(self, text: str) -> list[str]:
        if not text:
            return []
        matches: list[Any] = self.token_pattern.findall(text)
        return [str(m) for m in matches]

    def lemmatize_or_stem(self, word: str) -> str:
        if not word:
            return ""
        # Normalizamos a minúsculas
        clean = word.lower()
        stem_method: Callable[[str], str] = cast(Callable[[str], str], getattr(self.stemmer, "stem"))
        return stem_method(clean)

    def pos_tag(self, tokens: list[str]) -> list[tuple[str, str]]:
        return [(token, _classify_token(token.lower())) for token in tokens]
