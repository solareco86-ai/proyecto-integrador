import html
import re
from html.parser import HTMLParser

import markdown  # type: ignore

# Tags y atributos permitidos en el HTML de salida (whitelist mínimo)
_ALLOWED_TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "br",
    "hr",
    "strong",
    "em",
    "b",
    "i",
    "u",
    "s",
    "del",
    "ins",
    "a",
    "img",
    "ul",
    "ol",
    "li",
    "code",
    "pre",
    "blockquote",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "span",
    "div",
    "audio",
    "video",
    "source",
}
_ALLOWED_ATTRS = {
    "a": {"href", "title"},
    "img": {"src", "alt", "title", "width", "height"},
    "code": {"class"},
    "pre": {"class"},
    "audio": {"controls", "preload", "class"},
    "video": {"controls", "preload", "poster", "class"},
    "source": {"src", "type"},
}

# Atributos que llevan una URL: solo se aceptan rutas del sitio, anclas y http(s)/mailto.
_URL_ATTRS = {"href", "src", "poster"}
_ALLOWED_SCHEMES = {"http", "https", "mailto"}
_SCHEME_RE = re.compile(r"^([a-z][a-z0-9+.\-]*):")
_CLASS_RE = re.compile(r"^[a-zA-Z0-9_\-\s]+$")
# Caracteres que el navegador ignora dentro de una URL (sirven para esconder "javascript:").
_URL_IGNORED_RE = re.compile(r"[\x00-\x20\x7f]+")


def _is_safe_url(value: str) -> bool:
    """True si la URL es relativa o usa un esquema permitido (nunca javascript:, data:, etc.)."""
    normalized: str = _URL_IGNORED_RE.sub("", value).lower()
    match = _SCHEME_RE.match(normalized)
    return match is None or match.group(1) in _ALLOWED_SCHEMES


class _Sanitizer(HTMLParser):
    """Reconstruye el HTML dejando solo tags y atributos de la whitelist.

    Un tag no permitido se muestra como texto (escapado). Los atributos se vuelven a
    escribir siempre entre comillas, así que no importa cómo vinieron escritos
    (sin comillas, con comillas simples o sin valor).
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: list[str] = []

    def _open_tag(self, tag: str, attrs: list[tuple[str, str | None]]) -> str:
        allowed: set[str] = _ALLOWED_ATTRS.get(tag, set())
        kept: list[str] = []
        for name, value in attrs:
            if name not in allowed:
                continue
            if value is None:  # atributo booleano, como "controls"
                kept.append(name)
                continue
            if name == "class" and not _CLASS_RE.match(value):
                continue
            if name in _URL_ATTRS and not _is_safe_url(value):
                continue
            kept.append(f'{name}="{html.escape(value, quote=True)}"')
        attrs_str: str = " " + " ".join(kept) if kept else ""
        return f"<{tag}{attrs_str}>"

    def _raw_tag(self) -> str:
        return html.escape(self.get_starttag_text() or "")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.append(self._open_tag(tag, attrs) if tag in _ALLOWED_TAGS else self._raw_tag())

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.append(self._open_tag(tag, attrs) if tag in _ALLOWED_TAGS else self._raw_tag())

    def handle_endtag(self, tag: str) -> None:
        self.parts.append(f"</{tag}>" if tag in _ALLOWED_TAGS else html.escape(f"</{tag}>"))

    def handle_data(self, data: str) -> None:
        self.parts.append(html.escape(data, quote=False))

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")

    # Comentarios, declaraciones e instrucciones de procesamiento se descartan.


def _sanitize_html(html_text: str) -> str:
    """Elimina tags y atributos no permitidos del HTML generado por markdown."""
    sanitizer = _Sanitizer()
    sanitizer.feed(html_text)
    sanitizer.close()
    return "".join(sanitizer.parts)


class MarkdownParser:
    def __init__(self, extensions: list[str] | None = None) -> None:
        self.extensions = extensions or ["fenced_code", "tables"]

    def to_html(self, text: str) -> str:
        if not text:
            return ""
        raw_html = markdown.markdown(text, extensions=self.extensions)
        return _sanitize_html(raw_html)
