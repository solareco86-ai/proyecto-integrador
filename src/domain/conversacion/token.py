from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    texto_original: str
    texto_limpio: str
    lema: str
    pos: str
    es_stopword: bool
