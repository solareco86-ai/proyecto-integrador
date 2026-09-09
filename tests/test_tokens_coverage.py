"""Tests de cobertura e integridad de los tokens de diseño (tokens.css)."""

import re
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TOKENS = RAIZ / "static" / "css" / "src" / "tokens.css"
CRITICAL = RAIZ / "static" / "css" / "src" / "critical.css"
INPUT = RAIZ / "static" / "css" / "src" / "input.css"

_FRAMEWORK = ("--tw-", "--color-", "--default-")

_VAR_USO_RE = re.compile(r"var\((--[a-zA-Z0-9-]+)")
_VAR_DEF_RE = re.compile(r"^\s*(--[a-zA-Z0-9-]+)\s*:", re.MULTILINE)


def _vars_usados(texto: str) -> set[str]:
    return {m.group(1) for m in _VAR_USO_RE.finditer(texto) if not m.group(1).startswith(_FRAMEWORK)}


def _vars_definidos(texto: str) -> set[str]:
    return set(_VAR_DEF_RE.findall(texto))


def test_t1_critical_autocontenido_tokens() -> None:
    definidos = _vars_definidos(TOKENS.read_text(encoding="utf-8"))
    usados = _vars_usados(CRITICAL.read_text(encoding="utf-8"))
    faltantes = usados - definidos

    assert not faltantes, f"Tokens usados en critical.css sin definir en tokens.css: {sorted(faltantes)}"


def test_t2_input_tokens_definidos() -> None:
    definidos = _vars_definidos(TOKENS.read_text(encoding="utf-8"))
    usados = _vars_usados(INPUT.read_text(encoding="utf-8"))
    faltantes = usados - definidos

    assert not faltantes, f"Tokens usados en input.css sin definir en tokens.css: {sorted(faltantes)}"


def test_t3_sin_duplicados_en_tokens() -> None:
    nombres = _VAR_DEF_RE.findall(TOKENS.read_text(encoding="utf-8"))
    duplicados = [nombre for nombre, cuenta in Counter(nombres).items() if cuenta > 1]

    assert not duplicados, f"Tokens duplicados en tokens.css: {sorted(duplicados)}"
