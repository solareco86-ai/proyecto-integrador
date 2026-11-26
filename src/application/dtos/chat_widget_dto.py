"""DTOs de los textos del widget conversacional (data/config/chat_widget.yaml)."""

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


class ChatWidgetModel(BaseModel):
    titulo: str
    subtitulo: str
    avatar: ChatWidgetAvatarModel
    saludo: str
    aviso: str
    placeholder: str
    longitudMaxima: int = Field(gt=0)
    etiquetas: ChatWidgetEtiquetasModel
