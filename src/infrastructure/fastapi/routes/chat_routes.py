from fastapi import APIRouter, Depends, status

from src.application.dtos.chat_dto import ChatHealthResponse, ChatTextRequest, ChatTextResponse
from src.application.use_cases.chat.process_chat_text_use_case import ProcessChatTextUseCase

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


def get_process_chat_text_use_case() -> ProcessChatTextUseCase:
    return ProcessChatTextUseCase()


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
