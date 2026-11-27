from abc import ABC, abstractmethod


class NLPProcessorGateway(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        """Divide el texto en tokens léxicos."""
        ...

    @abstractmethod
    def lemmatize_or_stem(self, word: str) -> str:
        """Obtiene la raíz o lema de una palabra en español."""
        ...

    @abstractmethod
    def pos_tag(self, tokens: list[str]) -> list[tuple[str, str]]:
        """Devuelve pares (token, categoría_gramatical_POS)."""
        ...
