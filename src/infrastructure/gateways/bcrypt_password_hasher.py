"""Implementación de PasswordHasherGateway con bcrypt."""

import bcrypt

from src.application.gateways.password_hasher_gateway import PasswordHasherGateway


class BcryptPasswordHasher(PasswordHasherGateway):
    """Hasher de contraseñas basado en bcrypt."""

    def hash(self, password: str) -> str:
        """Genera un hash bcrypt de la contraseña en texto plano."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, password: str, password_hash: str) -> bool:
        """Verifica la contraseña contra el hash bcrypt almacenado."""
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except ValueError:
            # Hash con formato inválido (corrupto o no-bcrypt): tratar como no coincidente.
            return False
