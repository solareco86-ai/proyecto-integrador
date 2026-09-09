import pytest

from src.domain.value_objects import Price, Slug


def test_slug_value_object_valid():
    """Valida que slugs correctos no lancen excepciones y se comporten como strings."""
    s1 = Slug.validate("mi-slug-valido-123")
    assert s1 == "mi-slug-valido-123"
    assert isinstance(s1, Slug)
    assert isinstance(s1, str)


def test_slug_value_object_invalid():
    """Valida que slugs incorrectos (con mayúsculas, espacios o caracteres especiales) lancen ValueError."""
    with pytest.raises(ValueError, match="Slug inválido"):
        Slug.validate("Slug-Con-Mayusculas")

    with pytest.raises(ValueError, match="Slug inválido"):
        Slug.validate("slug con espacios")

    with pytest.raises(ValueError, match="Slug inválido"):
        Slug.validate("slug_con_guion_bajo")

    with pytest.raises(ValueError, match="Slug inválido"):
        Slug.validate("slug-con-simbolos$")


def test_price_value_object_valid():
    """Valida que precios válidos (positivos o cero) no lancen excepciones y se comporten como floats."""
    p1 = Price.validate(199.99)
    p2 = Price.validate(0.0)
    assert p1 == 199.99
    assert p2 == 0.0
    assert isinstance(p1, Price)
    assert isinstance(p1, float)


def test_price_value_object_invalid():
    """Valida que precios negativos lancen ValueError."""
    with pytest.raises(ValueError, match="Precio inválido"):
        Price.validate(-10.50)

    with pytest.raises(ValueError, match="Precio inválido"):
        Price.validate(-0.01)
