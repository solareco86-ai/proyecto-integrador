from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.application.use_cases.content.list_noticias import ListNoticiasUseCase
from src.domain.auth.entities import Usuario
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.fastapi.dependencies import get_noticia_repository, require_authority, templates

router = APIRouter(prefix="/panel", dependencies=[Depends(require_authority)], tags=["panel-noticias"])


@router.get("/noticias")
async def listar_noticias(
    request: Request,
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
) -> HTMLResponse:
    """Listado administrativo de noticias. Solo lectura en esta subetapa (4B-1)."""
    use_case = ListNoticiasUseCase(repository=noticia_repository)
    noticias = await use_case.execute()
    return templates.TemplateResponse(
        request=request,
        name="panel/noticias/list.html",
        context={"usuario": usuario, "noticias": noticias, "seccion_activa": "noticias"},
    )
