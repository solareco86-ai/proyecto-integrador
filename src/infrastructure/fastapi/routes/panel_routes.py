from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from src.domain.auth.entities import Usuario
from src.infrastructure.fastapi.dependencies import require_authority, templates

router = APIRouter(prefix="/panel", dependencies=[Depends(require_authority)], tags=["panel"])


@router.get("")
async def dashboard(request: Request, usuario: Usuario = Depends(require_authority)) -> HTMLResponse:
    """Dashboard mínimo del panel: bienvenida y navegación a las secciones."""
    return templates.TemplateResponse(
        request=request,
        name="panel/dashboard.html",
        context={"usuario": usuario, "seccion_activa": "inicio"},
    )
