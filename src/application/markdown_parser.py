import html
import re

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
}
_ALLOWED_ATTRS = {"a": {"href", "title"}, "img": {"src", "alt", "title", "width", "height"}}

_TAG_RE = re.compile(r"</?(\w+)[^>]*/?>")


def _sanitize_html(html_text: str) -> str:
    """Elimina tags y atributos no permitidos del HTML generado por markdown."""

    def _replace_tag(match: re.Match[str]) -> str:
        tag: str = match.group(1).lower()
        full_tag: str = match.group(0)

        if tag not in _ALLOWED_TAGS:
            # Escapar tag no permitido
            return html.escape(full_tag)

        if full_tag.startswith("</"):
            # Closing tag: no attributes to check
            return full_tag

        # Opening/self-closing tag: filtrar atributos
        allowed = _ALLOWED_ATTRS.get(tag, set())
        if not allowed:
            # Tag permitido pero sin atributos: permitir solo el tag puro
            return re.sub(rf"<{re.escape(tag)}[^>]*>", f"<{tag}>", full_tag, flags=re.IGNORECASE)

        # Mantener solo los atributos permitidos
        def _filter_attrs(m: re.Match[str]) -> str:
            tag_name: str = m.group(1).lower()
            attrs_str: str = m.group(2).strip()
            # Parsear atributos simples key="value"
            kept: list[str] = []
            for attr_match in re.finditer(r'(\w+)=(?:"([^"]*)"|\'([^\']*)\')', attrs_str):
                attr_name = attr_match.group(1).lower()
                if attr_name in allowed:
                    kept.append(attr_match.group(0))
            attrs = " " + " ".join(kept) if kept else ""
            return f"<{tag_name}{attrs}>"

        return re.sub(
            r"<(\w+)((?:\s+\w+=(?:\"[^\"]*\"|'[^']*'))*)\s*/?>",
            _filter_attrs,
            full_tag,
            flags=re.IGNORECASE,
        )

    return _TAG_RE.sub(_replace_tag, html_text)


class MarkdownParser:
    def __init__(self, extensions: list[str] | None = None) -> None:
        self.extensions = extensions or ["fenced_code", "tables"]

    def to_html(self, text: str) -> str:
        if not text:
            return ""
        raw_html = markdown.markdown(text, extensions=self.extensions)
        return _sanitize_html(raw_html)
