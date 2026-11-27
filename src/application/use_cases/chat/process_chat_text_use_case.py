import os
from typing import Any, cast

import yaml

from src.application.dtos.chat_dto import ChatHealthResponse, ChatTextRequest, ChatTextResponse
from src.application.services.text_morphology_service import TextMorphologyService
from src.domain.conversacion.consulta import Consulta
from src.domain.conversacion.respuesta import Respuesta
from src.domain.conversacion.texto_analizado import TextoAnalizado
from src.infrastructure.gateways.nltk_nlp_gateway import NltkNLPGateway


class ProcessChatTextUseCase:
    def __init__(
        self,
        data_dir: str | None = None,
        morphology_service: TextMorphologyService | None = None,
    ) -> None:
        if not data_dir or (data_dir == "data" and "DATA_DIR" in os.environ):
            self.data_dir = os.getenv("DATA_DIR", "data")
        else:
            self.data_dir = data_dir
        self.config_path = os.path.join(self.data_dir, "chat", "mock_response.yaml")

        if morphology_service is None:
            self.morphology_service = TextMorphologyService(
                nlp_gateway=NltkNLPGateway(),
                data_dir=self.data_dir,
            )
        else:
            self.morphology_service = morphology_service

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
        _texto_analizado: TextoAnalizado = self.morphology_service.analyze(request.message)

        # 3. Carga y generación de respuesta
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

        return ChatTextResponse(
            reply=_respuesta.texto,
            intent=_respuesta.intencion,
            sources=_respuesta.fuentes,
            confidence=_respuesta.confianza,
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
