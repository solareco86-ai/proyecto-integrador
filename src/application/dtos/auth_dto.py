"""DTOs internos para los casos de uso de autenticación.

Dataclass simple desacoplada de la capa web, igual que `SubmitLeadInput`
en `use_cases/submit_lead.py` y los DTOs de `content_management_dto.py`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LoginInput:
    """Datos de entrada para autenticar un usuario."""

    email: str
    password: str
