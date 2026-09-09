"""Tests del hasher de contraseñas concreto con bcrypt."""

from src.infrastructure.gateways.bcrypt_password_hasher import BcryptPasswordHasher


def test_hash_no_es_texto_plano():
    hasher = BcryptPasswordHasher()
    password_hash = hasher.hash("clave-segura-123")

    assert password_hash != "clave-segura-123"
    assert password_hash.startswith("$2b$")


def test_verify_password_correcta():
    hasher = BcryptPasswordHasher()
    password_hash = hasher.hash("clave-segura-123")

    assert hasher.verify("clave-segura-123", password_hash) is True


def test_verify_password_incorrecta():
    hasher = BcryptPasswordHasher()
    password_hash = hasher.hash("clave-segura-123")

    assert hasher.verify("otra-clave", password_hash) is False


def test_verify_hash_invalido_no_lanza_excepcion():
    hasher = BcryptPasswordHasher()

    assert hasher.verify("clave-segura-123", "hash-corrupto-no-bcrypt") is False


def test_hash_es_distinto_en_cada_llamada():
    """El salt aleatorio garantiza hashes distintos para la misma contraseña."""
    hasher = BcryptPasswordHasher()

    assert hasher.hash("clave-segura-123") != hasher.hash("clave-segura-123")
