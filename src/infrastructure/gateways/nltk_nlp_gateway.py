import re
from collections.abc import Callable
from typing import Any, cast

from nltk.stem.snowball import SpanishStemmer

from src.application.gateways.nlp_gateway import NLPProcessorGateway


class NltkNLPGateway(NLPProcessorGateway):
    def __init__(self) -> None:
        self.stemmer: SpanishStemmer = SpanishStemmer()
        # Patrón simple de tokenización por palabras y números
        self.token_pattern: re.Pattern[str] = re.compile(r"\b\w+\b", re.UNICODE)

        # Reglas heurísticas de POS Tagging en español (Universal POS Tags simplificados)
        # VERB, NOUN, ADJ, ADV, PRON, DET, ADP, CONJ, NUM, NOUN (default)
        self.verb_endings: tuple[str, ...] = (
            "ar", "er", "ir", "ando", "iendo", "ado", "ido", "aron", "ieron",
            "aba", "abas", "abamos", "aban", "ia", "ias", "iamos", "ian",
            "an", "en", "amos", "emos", "imos", "e", "aste", "o", "io"
        )
        self.adj_endings: tuple[str, ...] = ("al", "ales", "ico", "ica", "icos", "icas", "oso", "osa", "osos", "osas", "ble", "bles")
        self.adv_words: set[str] = {"no", "si", "muy", "mas", "menos", "bien", "mal", "ya", "hoy", "tarde", "temprano", "cerca", "lejos"}
        self.pron_words: set[str] = {"yo", "tu", "el", "ella", "nosotros", "vosotros", "ellos", "ellas", "me", "te", "se", "nos", "les", "que", "quien"}
        self.adp_words: set[str] = {"a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre", "hacia", "hasta", "para", "por", "segun", "sin", "so", "sobre", "tras"}
        self.det_words: set[str] = {"el", "la", "los", "las", "un", "una", "unos", "unas", "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella"}

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
        result: list[tuple[str, str]] = []
        for token in tokens:
            lower = token.lower()
            if lower.isdigit():
                tag = "NUM"
            elif lower in self.adp_words:
                tag = "ADP"
            elif lower in self.det_words:
                tag = "DET"
            elif lower in self.pron_words:
                tag = "PRON"
            elif lower in self.adv_words or lower.endswith("mente"):
                tag = "ADV"
            elif lower.endswith(self.verb_endings) and len(lower) > 3:
                tag = "VERB"
            elif lower.endswith(self.adj_endings) and len(lower) > 3:
                tag = "ADJ"
            else:
                tag = "NOUN"
            result.append((token, tag))
        return result
