"""Tests unitarios del use case de autenticación, sin base de datos real."""

import pytest

from src.application.dtos.auth_dto import LoginInput
from src.application.gateways.password_hasher_gateway import PasswordHasherGateway
from src.application.use_cases.auth.authenticate_usuario import AuthenticateUsuarioUseCase
from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.common.exceptions import CredencialesInvalidasError


class FakePasswordHasher(PasswordHasherGateway):
    """Hasher determinístico, sin bcrypt real, para tests rápidos."""

    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == f"hashed:{password}"


class InMemoryUsuarioRepo(UsuarioRepository):
    def __init__(self, usuarios: list[Usuario]) -> None:
        self.by_id: dict[str, Usuario] = {u.id: u for u in usuarios}
        self.by_email: dict[str, Usuario] = {u.email: u for u in usuarios}

    async def save(self, usuario: Usuario) -> None:
        self.by_id[usuario.id] = usuario
        self.by_email[usuario.email] = usuario

    async def get_by_id(self, usuario_id: str) -> Usuario | None:
        return self.by_id.get(usuario_id)

    async def get_by_email(self, email: str) -> Usuario | None:
        return self.by_email.get(email)


def _crear_usuario(email: str = "directora@isft199.edu.ar", is_active: bool = True) -> Usuario:
    hasher = FakePasswordHasher()
    return Usuario.create(
        email=email,
        password_hash=hasher.hash("clave-segura-123"),
        nombre="Directora",
        is_active=is_active,
    )


@pytest.mark.asyncio
async def test_login_correcto_devuelve_usuario():
    usuario = _crear_usuario()
    repo = InMemoryUsuarioRepo([usuario])
    use_case = AuthenticateUsuarioUseCase(repository=repo, password_hasher=FakePasswordHasher())

    autenticado = await use_case.execute(LoginInput(email=usuario.email, password="clave-segura-123"))

    assert autenticado == usuario


@pytest.mark.asyncio
async def test_login_password_incorrecta_lanza_error():
    usuario = _crear_usuario()
    repo = InMemoryUsuarioRepo([usuario])
    use_case = AuthenticateUsuarioUseCase(repository=repo, password_hasher=FakePasswordHasher())

    with pytest.raises(CredencialesInvalidasError):
        await use_case.execute(LoginInput(email=usuario.email, password="clave-incorrecta"))


@pytest.mark.asyncio
async def test_login_usuario_inexistente_lanza_error():
    repo = InMemoryUsuarioRepo([])
    use_case = AuthenticateUsuarioUseCase(repository=repo, password_hasher=FakePasswordHasher())

    with pytest.raises(CredencialesInvalidasError):
        await use_case.execute(LoginInput(email="no-existe@isft199.edu.ar", password="cualquiera"))


@pytest.mark.asyncio
async def test_login_usuario_inactivo_lanza_error():
    usuario = _crear_usuario(is_active=False)
    repo = InMemoryUsuarioRepo([usuario])
    use_case = AuthenticateUsuarioUseCase(repository=repo, password_hasher=FakePasswordHasher())

    with pytest.raises(CredencialesInvalidasError):
        await use_case.execute(LoginInput(email=usuario.email, password="clave-segura-123"))
