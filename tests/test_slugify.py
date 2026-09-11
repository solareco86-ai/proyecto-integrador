"""Tests unitarios de slugify (dominio, sin dependencias externas)."""

from src.domain.common.slugify import slugify


def test_slugify_minusculas_y_guiones():
    assert slugify("Inscripción 2027") == "inscripcion-2027"


def test_slugify_elimina_tildes():
    assert slugify("Última función") == "ultima-funcion"


def test_slugify_elimina_signos_de_puntuacion():
    assert slugify("¡Últimas vacantes!") == "ultimas-vacantes"


def test_slugify_colapsa_espacios_multiples():
    assert slugify("Muchos   espacios   aca") == "muchos-espacios-aca"


def test_slugify_recorta_guiones_en_extremos():
    assert slugify("  -Hola Mundo-  ") == "hola-mundo"


def test_slugify_texto_vacio_devuelve_item():
    assert slugify("") == "item"


def test_slugify_solo_simbolos_devuelve_item():
    assert slugify("!!!???") == "item"
