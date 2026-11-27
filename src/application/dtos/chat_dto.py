import os

from pydantic import BaseModel, ConfigDict, Field, field_validator


def get_chat_max_message_length() -> int:
    return int(os.getenv("CHAT_MAX_MESSAGE_LENGTH", "1000"))


class ChatTextRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    session_id: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Identificador único de la sesión del usuario",
    )
    message: str = Field(
        ...,
        min_length=1,
        description="Consulta textual del usuario sobre el instituto",
    )

    @field_validator("message")
    @classmethod
    def validate_message_length(cls, value: str) -> str:
        max_len = get_chat_max_message_length()
        if len(value) > max_len:
            raise ValueError(
                f"El mensaje supera la longitud máxima permitida de {max_len} caracteres."
            )
        return value


class ChatTextResponse(BaseModel):
    reply: str = Field(..., description="Respuesta textual generada para el usuario")
    intent: str = Field(..., description="Intención detectada o clasificada")
    sources: list[str] = Field(
        default_factory=list,
        description="Rutas o URLs oficiales del sitio que respaldan la respuesta",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Nivel de confianza de la respuesta (0.0 a 1.0)",
    )


class ChatAudioResponse(BaseModel):
    transcript: str = Field(..., description="Transcripción del audio recibido")
    reply: str = Field(..., description="Respuesta textual generada")
    intent: str = Field(..., description="Intención detectada")
    sources: list[str] = Field(
        default_factory=list,
        description="Rutas o URLs oficiales del sitio que respaldan la respuesta",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Nivel de confianza de la respuesta (0.0 a 1.0)",
    )


class ChatHealthResponse(BaseModel):
    status: str = Field(..., description="Estado general del servicio de chat")
    modules: dict[str, bool] = Field(
        default_factory=dict,
        description="Estado de activación de los módulos del motor",
    )
