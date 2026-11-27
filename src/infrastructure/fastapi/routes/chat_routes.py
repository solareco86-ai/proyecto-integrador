from fastapi import APIRouter, Depends, status

from src.application.dtos.chat_dto import ChatHealthResponse, ChatTextRequest, ChatTextResponse
from src.application.gateways.nlp_gateway import NLPProcessorGateway
from src.application.services.text_morphology_service import TextMorphologyService
from src.application.use_cases.chat.process_chat_text_use_case import ProcessChatTextUseCase
from src.infrastructure.gateways.nltk_nlp_gateway import NltkNLPGateway

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


def get_nlp_gateway() -> NLPProcessorGateway:
    return NltkNLPGateway()


def get_morphology_service(
    gateway: NLPProcessorGateway = Depends(get_nlp_gateway),
) -> TextMorphologyService:
    return TextMorphologyService(nlp_gateway=gateway)


def get_process_chat_text_use_case(
    morphology_service: TextMorphologyService = Depends(get_morphology_service),
) -> ProcessChatTextUseCase:
    return ProcessChatTextUseCase(morphology_service=morphology_service)


@router.get(
    "/health",
    response_model=ChatHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Estado de salud del motor de chat y módulos activos",
)
def get_chat_health(
    use_case: ProcessChatTextUseCase = Depends(get_process_chat_text_use_case),
) -> ChatHealthResponse:
    return use_case.get_health()


@router.post(
    "/text",
    response_model=ChatTextResponse,
    status_code=status.HTTP_200_OK,
    summary="Procesar consulta de texto del usuario",
)
def process_chat_text(
    request: ChatTextRequest,
    use_case: ProcessChatTextUseCase = Depends(get_process_chat_text_use_case),
) -> ChatTextResponse:
    return use_case.execute(request)
