from dataclasses import dataclass

from src.domain.conversacion.token import Token


@dataclass(frozen=True)
class TextoAnalizado:
    texto_original: str
    texto_normalizado: str
    tokens: list[Token]
