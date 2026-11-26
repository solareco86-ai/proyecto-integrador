"""Pruebas de seguridad del filtro de HTML de las lecciones (src/application/markdown_parser.py).

Antes, un tag con atributos sin comillas (`<img src=x onerror=alert(1)>`) pasaba sin
filtrar, y los enlaces `javascript:` se conservaban. Estas pruebas fijan que eso no vuelva.
"""

import pytest

from src.application.markdown_parser import MarkdownParser, _sanitize_html


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("<img src=x onerror=alert(1)>", '<img src="x">'),
        ("<img src='x' onerror='alert(1)'>", '<img src="x">'),
        ('<img src="x" onerror>', '<img src="x">'),
        ('<img src="x" ONERROR="alert(1)">', '<img src="x">'),
        ('<a href="/cursos" onclick="robar()">ir</a>', '<a href="/cursos">ir</a>'),
    ],
)
def test_descarta_atributos_no_permitidos_sin_importar_como_se_escriben(entrada: str, esperado: str) -> None:
    assert _sanitize_html(entrada) == esperado


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "JavaScript:alert(1)",
        " javascript:alert(1)",
        "jav&#x09;ascript:alert(1)",
        "java\nscript:alert(1)",
        "data:text/html;base64,PHNjcmlwdD4=",
        "vbscript:msgbox(1)",
        "file:///home/alguien/leccion.md",
    ],
)
def test_descarta_urls_peligrosas(url: str) -> None:
    assert _sanitize_html(f'<a href="{url}">x</a>') == "<a>x</a>"
    assert _sanitize_html(f'<img src="{url}">') == "<img>"


@pytest.mark.parametrize(
    "url",
    [
        "/static/img/a.webp",
        "#seccion",
        "https://isftn199.com.ar",
        "http://ejemplo.com",
        "mailto:isft199@abc.gob.ar",
        "a.png",
    ],
)
def test_conserva_urls_seguras(url: str) -> None:
    assert _sanitize_html(f'<a href="{url}">x</a>') == f'<a href="{url}">x</a>'


def test_un_enlace_markdown_con_javascript_queda_sin_href() -> None:
    assert MarkdownParser().to_html("[clic](javascript:alert(1))") == "<p><a>clic</a></p>"


def test_tags_no_permitidos_se_muestran_como_texto() -> None:
    assert _sanitize_html("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;"
    assert _sanitize_html('<iframe src="https://x.com"></iframe>') == (
        "&lt;iframe src=&quot;https://x.com&quot;&gt;&lt;/iframe&gt;"
    )


def test_descarta_comentarios_html() -> None:
    assert _sanitize_html("<p>a<!-- <script>x</script> -->b</p>") == "<p>ab</p>"


def test_conserva_atributos_booleanos_permitidos() -> None:
    assert _sanitize_html('<audio controls preload="none"></audio>') == '<audio controls preload="none"></audio>'


def test_descarta_clases_con_caracteres_raros() -> None:
    assert _sanitize_html('<code class="language-python">x</code>') == '<code class="language-python">x</code>'
    assert _sanitize_html('<code class="a&quot;b">x</code>') == "<code>x</code>"


def test_el_codigo_y_las_entidades_quedan_escapados() -> None:
    html: str = MarkdownParser().to_html("```python\nif a < b and c > d:\n    print('&')\n```")
    assert "if a &lt; b and c &gt; d:" in html
    assert "print('&amp;')" in html
    assert _sanitize_html("<p>Tom &amp; Jerry &#169; &lt;3</p>") == "<p>Tom &amp; Jerry &#169; &lt;3</p>"


def test_los_valores_de_los_atributos_se_vuelven_a_escapar() -> None:
    assert _sanitize_html('<img alt="a &quot;b&quot; <c>" src="x">') == '<img alt="a &quot;b&quot; &lt;c&gt;" src="x">'
