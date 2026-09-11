"""Caso de uso para autenticar un usuario por email y contraseña."""

from src.application.dtos.auth_dto import LoginInput
from src.application.gateways.password_hasher_gateway import PasswordHasherGateway
from src.domain.auth.entities import Usuario
from src.domain.auth.repositories import UsuarioRepository
from src.domain.common.exceptions import CredencialesInvalidasError


class AuthenticateUsuarioUseCase:
    """Valida credenciales y devuelve el usuario autenticado."""

    def __init__(
        self,
        repository: UsuarioRepository,
        password_hasher: PasswordHasherGateway,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher

    async def execute(self, input: LoginInput) -> Usuario:
        """Autentica al usuario. Lanza CredencialesInvalidasError si falla cualquier chequeo."""
        usuario = await self._repository.get_by_email(input.email)

        # Mismo error para email inexistente, password incorrecta o usuario
        # inactivo: evita filtrar si un email está registrado o no.
        if usuario is None:
            raise CredencialesInvalidasError("Email o contraseña incorrectos")

        if not self._password_hasher.verify(input.password, usuario.password_hash):
            raise CredencialesInvalidasError("Email o contraseña incorrectos")

        if not usuario.is_active:
            raise CredencialesInvalidasError("Email o contraseña incorrectos")

        return usuario
