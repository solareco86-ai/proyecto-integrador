import os
from typing import Any, cast

import yaml

from src.application.dtos.chat_dto import ChatHealthResponse, ChatTextRequest, ChatTextResponse
from src.application.gateways.nlp_gateway import NLPProcessorGateway
from src.application.services.gramatica_intenciones_service import GramaticaIntencionesService
from src.application.services.lexico_institucional_service import LexicoInstitucionalService
from src.application.services.respuestas_chat_service import RespuestasChatService
from src.application.services.text_morphology_service import TextMorphologyService
from src.domain.conversacion.consulta import Consulta
from src.domain.conversacion.respuesta import Respuesta
from src.domain.conversacion.texto_analizado import TextoAnalizado


class ProcessChatTextUseCase:
    def __init__(
        self,
        data_dir: str | None = None,
        morphology_service: TextMorphologyService | None = None,
        nlp_gateway: NLPProcessorGateway | None = None,
        lexico_service: LexicoInstitucionalService | None = None,
        gramatica_service: GramaticaIntencionesService | None = None,
        respuestas_service: RespuestasChatService | None = None,
    ) -> None:
        if not data_dir or (data_dir == "data" and "DATA_DIR" in os.environ):
            self.data_dir = os.getenv("DATA_DIR", "data")
        else:
            self.data_dir = data_dir
        self.config_path = os.path.join(self.data_dir, "chat", "mock_response.yaml")

        if morphology_service is not None:
            self.morphology_service: TextMorphologyService | None = morphology_service
        elif nlp_gateway is not None:
            self.morphology_service = TextMorphologyService(
                nlp_gateway=nlp_gateway,
                data_dir=self.data_dir,
            )
        else:
            self.morphology_service = None

        # Análisis semántico (Eje 1.3): si falta alguna pieza se usa la respuesta simulada.
        self.lexico_service: LexicoInstitucionalService | None = lexico_service
        self.gramatica_service: GramaticaIntencionesService | None = gramatica_service
        self.respuestas_service: RespuestasChatService | None = respuestas_service

    def _load_data(self) -> dict[str, Any]:
        if not os.path.exists(self.config_path):
            return {
                "status": "ok",
                "modules": {
                    "nlp_normalization": True,
                    "intent_classification": False,
                    "speech_recognition": False,
                    "information_retrieval": False,
                },
                "mock_response": {
                    "reply": "Respuesta predeterminada del ISFT N° 199.",
                    "intent": "informacion_general",
                    "sources": ["/carreras"],
                    "confidence": 1.0,
                },
            }
        with open(self.config_path, encoding="utf-8") as file:
            loaded: Any = yaml.safe_load(file)
            if isinstance(loaded, dict):
                return cast(dict[str, Any], loaded)
            fallback: dict[str, Any] = {}
            return fallback

    def execute(self, request: ChatTextRequest) -> ChatTextResponse:
        # Fases de comunicación:
        # 1. Recepción y Creación de entidad de Dominio
        _consulta = Consulta(mensaje=request.message, session_id=request.session_id)

        # 2. Normalización y Análisis Morfológico (Eje 1.2)
        if self.morphology_service is not None:
            texto_analizado: TextoAnalizado = self.morphology_service.analyze(_consulta.mensaje)

            # 3. Análisis semántico: léxico + gramática -> intención y entidades (Eje 1.3)
            if self.lexico_service and self.gramatica_service and self.respuestas_service:
                simbolos = self.lexico_service.etiquetar(texto_analizado.tokens)
                interpretacion = self.gramatica_service.interpretar(simbolos)
                return self._serializar(self.respuestas_service.responder(interpretacion))

        # 4. Respuesta simulada (scaffolding Eje 1.1)
        data = self._load_data()
        raw_mock: Any = data.get("mock_response", {})
        mock_data: dict[str, Any] = cast(dict[str, Any], raw_mock) if isinstance(raw_mock, dict) else {}

        reply_text = str(mock_data.get("reply", ""))
        intent_text = str(mock_data.get("intent", "desconocido"))
        raw_sources: Any = mock_data.get("sources", [])
        sources_list: list[str] = []
        if isinstance(raw_sources, list):
            sources_iterable: list[object] = cast(list[object], raw_sources)
            for item in sources_iterable:
                sources_list.append(str(item))

        confidence_val = float(mock_data.get("confidence", 1.0))

        # Modelado de entidad de dominio de Respuesta
        _respuesta = Respuesta(
            texto=reply_text,
            intencion=intent_text,
            fuentes=sources_list,
            confianza=confidence_val,
        )

        return self._serializar(_respuesta)

    @staticmethod
    def _serializar(respuesta: Respuesta) -> ChatTextResponse:
        return ChatTextResponse(
            reply=respuesta.texto,
            intent=respuesta.intencion,
            sources=respuesta.fuentes,
            confidence=respuesta.confianza,
        )

    def get_health(self) -> ChatHealthResponse:
        data = self._load_data()
        status_val = str(data.get("status", "ok"))
        raw_modules: Any = data.get("modules", {})
        modules_dict: dict[str, bool] = {}
        if isinstance(raw_modules, dict):
            modules_mapping: dict[object, object] = cast(dict[object, object], raw_modules)
            for key, val in modules_mapping.items():
                modules_dict[str(key)] = bool(val)

        return ChatHealthResponse(status=status_val, modules=modules_dict)
