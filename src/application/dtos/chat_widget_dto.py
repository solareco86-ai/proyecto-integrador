"""DTOs de los textos del widget conversacional (data/config/chat_widget.yaml)."""

from typing import Any

from pydantic import BaseModel, Field


class ChatWidgetAvatarModel(BaseModel):
    src: str
    alt: str


class ChatWidgetEtiquetasModel(BaseModel):
    """Textos accesibles (aria-label y label) de los controles del widget."""

    abrir: str
    cerrar: str
    conversacion: str
    campo: str
    enviar: str
    grabar: str


class ChatWidgetInterfazModel(BaseModel):
    """Textos que el JavaScript muestra durante la conversación (FE 4.2)."""

    escribiendo: str
    fuentes: str
    reintentar: str


class ChatWidgetApiModel(BaseModel):
    """Conexión del widget con el motor conversacional (contrato del Epic #144)."""

    baseUrl: str
    mock: bool
    timeoutTextoMs: int = Field(gt=0)
    timeoutAudioMs: int = Field(gt=0)


class ChatWidgetErroresModel(BaseModel):
    """Mensajes que ve el público ante cada tipo de error del cliente de la API."""

    timeout: str
    red: str
    servidor: str
    validacion: str
    audioVacio: str
    respuestaInvalida: str


class ChatWidgetMockModel(BaseModel):
    """Respuestas simuladas para probar el widget sin el backend (FE 4.4)."""

    respuesta: str
    transcripcion: str
    intencion: str
    fuentes: list[str]
    confianza: float = Field(ge=0, le=1)
    demoraMs: int = Field(ge=0)


class ChatWidgetModel(BaseModel):
    titulo: str
    subtitulo: str
    avatar: ChatWidgetAvatarModel
    saludo: str
    aviso: str
    placeholder: str
    longitudMaxima: int = Field(gt=0)
    etiquetas: ChatWidgetEtiquetasModel
    interfaz: ChatWidgetInterfazModel
    api: ChatWidgetApiModel
    errores: ChatWidgetErroresModel
    mock: ChatWidgetMockModel

    def configuracion_cliente(self) -> dict[str, Any]:
        """Datos que necesita el JavaScript del widget, para serializar en la plantilla."""
        return {
            "longitudMaxima": self.longitudMaxima,
            "interfaz": self.interfaz.model_dump(),
            "api": self.api.model_dump(),
            "errores": self.errores.model_dump(),
            "mock": self.mock.model_dump(),
        }
