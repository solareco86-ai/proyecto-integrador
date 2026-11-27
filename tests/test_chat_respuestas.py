from pathlib import Path
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient

from src.application.dtos.chat_dto import ChatTextRequest
from src.application.services.respuestas_chat_service import RespuestasChatService
from src.application.use_cases.chat.process_chat_text_use_case import ProcessChatTextUseCase
from src.domain.conversacion.interpretacion import INTENCION_FUERA_DE_DOMINIO, Entidades, Interpretacion
from src.infrastructure.fastapi.app import app
from src.infrastructure.gateways.nltk_nlp_gateway import NltkNLPGateway


def aceptada(intencion: str, confianza: float = 0.9, **entidades: Any) -> Interpretacion:
    return Interpretacion(intencion=intencion, entidades=Entidades(**entidades), confianza=confianza, aceptada=True)


@pytest.fixture(scope="module")
def servicio() -> RespuestasChatService:
    return RespuestasChatService(data_dir="data")


# --- Servicio de respuestas ----------------------------------------------------


def test_respuesta_de_carrera_usa_datos_de_carreras_yaml(servicio: RespuestasChatService) -> None:
    respuesta = servicio.responder(aceptada("duracion", carrera="hoteleria"))
    assert respuesta.texto == "La Tecnicatura Superior en Hotelería dura 3 años."
    assert respuesta.fuentes == ["/carreras/hoteleria"]
    assert respuesta.confianza == 0.9


def test_respuesta_general_lista_las_seis_carreras(servicio: RespuestasChatService) -> None:
    respuesta = servicio.responder(aceptada("info_carrera"))
    assert respuesta.texto.count("Tecnicatura Superior en") == 6
    assert respuesta.fuentes == ["/carreras"]


def test_dato_general_aplica_aunque_se_mencione_una_carrera(servicio: RespuestasChatService) -> None:
    respuesta = servicio.responder(aceptada("sedes", carrera="logistica"))
    assert "Celina Voena 1750" in respuesta.texto


@pytest.mark.parametrize(
    "interpretacion",
    [
        aceptada("becas"),
        aceptada("mesas_examen", carrera="turismo"),
        aceptada("correlatividades"),
        aceptada("plan_estudios", carrera="turismo", anio=1),
        aceptada("intencion_sin_configurar"),
        aceptada("horarios", confianza=0.3),
    ],
)
def test_sin_dato_o_baja_confianza_deriva_a_secretaria(
    interpretacion: Interpretacion, servicio: RespuestasChatService
) -> None:
    respuesta = servicio.responder(interpretacion)
    assert "Secretaría" in respuesta.texto
    assert "isft199@abc.gob.ar" in respuesta.texto
    assert respuesta.fuentes == ["/contact"]
    assert respuesta.intencion == interpretacion.intencion


def test_consulta_rechazada_responde_fuera_de_dominio(servicio: RespuestasChatService) -> None:
    rechazo = Interpretacion(intencion=INTENCION_FUERA_DE_DOMINIO, entidades=Entidades(), confianza=0.0, aceptada=False)
    respuesta = servicio.responder(rechazo)
    assert respuesta.intencion == INTENCION_FUERA_DE_DOMINIO
    assert respuesta.confianza == 0.0
    assert respuesta.fuentes == ["/carreras"]


def test_sin_archivos_de_datos_igual_deriva_sin_inventar(tmp_path: Path) -> None:
    vacio = RespuestasChatService(data_dir=str(tmp_path))
    assert vacio.umbral == 0.6
    rechazo = Interpretacion(intencion=INTENCION_FUERA_DE_DOMINIO, entidades=Entidades(), confianza=0.0, aceptada=False)
    assert vacio.responder(rechazo).fuentes == []
    assert vacio.responder(aceptada("horarios")).texto == ""


def test_marcador_desconocido_no_rompe_la_plantilla(tmp_path: Path) -> None:
    (tmp_path / "chat").mkdir()
    (tmp_path / "chat" / "intenciones.yaml").write_text(
        "intenciones:\n  saludo:\n    reply: 'Hola {desconocido}'\n", encoding="utf-8"
    )
    assert RespuestasChatService(data_dir=str(tmp_path)).responder(aceptada("saludo")).texto == "Hola {desconocido}"


def test_caso_de_uso_sin_servicios_semanticos_usa_respuesta_simulada() -> None:
    request = ChatTextRequest(session_id="eje13", message="kiero anotarme en logistica")
    respuesta = ProcessChatTextUseCase(data_dir="data", nlp_gateway=NltkNLPGateway()).execute(request)
    assert respuesta.intent == "informacion_general"


# --- Endpoint integrado --------------------------------------------------------


async def consultar(mensaje: str) -> dict[str, Any]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as cliente:
        response = await cliente.post("/api/v1/chat/text", json={"session_id": "eje13", "message": mensaje})
    assert response.status_code == 200
    data: dict[str, Any] = response.json()
    return data


@pytest.mark.asyncio
async def test_endpoint_devuelve_intencion_real_y_no_el_mock() -> None:
    data = await consultar("kiero anotarme en logistica")
    assert data["intent"] == "inscripcion"
    assert "Tecnicatura Superior en Logística" in data["reply"]
    assert data["sources"] == ["/carreras/logistica", "/contact"]


@pytest.mark.asyncio
async def test_endpoint_deriva_becas_a_secretaria() -> None:
    data = await consultar("hay becas?")
    assert data["intent"] == "becas"
    assert "Secretaría" in data["reply"]


@pytest.mark.asyncio
async def test_endpoint_consulta_fuera_de_dominio() -> None:
    data = await consultar("me gusta el futbol")
    assert data["intent"] == INTENCION_FUERA_DE_DOMINIO
    assert data["confidence"] == 0.0


@pytest.mark.asyncio
async def test_health_informa_clasificacion_de_intenciones_activa() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as cliente:
        response = await cliente.get("/api/v1/chat/health")
    assert response.json()["modules"]["intent_classification"] is True
