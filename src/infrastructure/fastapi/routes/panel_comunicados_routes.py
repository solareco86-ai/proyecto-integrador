from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.application.use_cases.content.list_comunicados import ListComunicadosUseCase
from src.domain.auth.entities import Usuario
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.fastapi.dependencies import get_comunicado_repository, require_authority, templates

router = APIRouter(prefix="/panel", dependencies=[Depends(require_authority)], tags=["panel-comunicados"])


@router.get("/comunicados")
async def listar_comunicados(
    request: Request,
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
) -> HTMLResponse:
    """Listado administrativo de comunicados. Solo lectura en esta subetapa (4D-1)."""
    use_case = ListComunicadosUseCase(repository=comunicado_repository)
    comunicados = await use_case.execute()
    return templates.TemplateResponse(
        request=request,
        name="panel/comunicados/list.html",
        context={"usuario": usuario, "comunicados": comunicados, "seccion_activa": "comunicados"},
    )
