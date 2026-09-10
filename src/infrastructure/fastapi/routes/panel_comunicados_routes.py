from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.dtos.content_management_dto import CrearComunicadoInput
from src.application.use_cases.content.create_comunicado import CreateComunicadoUseCase
from src.application.use_cases.content.list_comunicados import ListComunicadosUseCase
from src.domain.auth.entities import Usuario
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.fastapi.csrf import get_or_create_csrf_token, verify_csrf
from src.infrastructure.fastapi.dependencies import get_comunicado_repository, require_authority, templates

router = APIRouter(prefix="/panel", dependencies=[Depends(require_authority)], tags=["panel-comunicados"])

_TITULO_MAX_LENGTH = 200


def _validar(titulo: str, cuerpo: str) -> str | None:
    """Valida título/cuerpo ya limpios (strip aplicado por el llamador). Devuelve el mensaje de error o None."""
    if not titulo:
        return "El título es obligatorio."
    if len(titulo) > _TITULO_MAX_LENGTH:
        return f"El título no puede superar los {_TITULO_MAX_LENGTH} caracteres."
    if not cuerpo:
        return "El cuerpo es obligatorio."
    return None


@router.get("/comunicados")
async def listar_comunicados(
    request: Request,
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
    ok: str | None = None,
) -> HTMLResponse:
    """Listado administrativo de comunicados."""
    use_case = ListComunicadosUseCase(repository=comunicado_repository)
    comunicados = await use_case.execute()
    return templates.TemplateResponse(
        request=request,
        name="panel/comunicados/list.html",
        context={"usuario": usuario, "comunicados": comunicados, "seccion_activa": "comunicados", "ok": ok},
    )


@router.get("/comunicados/nuevo")
async def form_nuevo_comunicado(
    request: Request,
    usuario: Usuario = Depends(require_authority),
) -> HTMLResponse:
    """Muestra el formulario de creación de comunicado."""
    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/comunicados/form.html",
        context={
            "usuario": usuario,
            "seccion_activa": "comunicados",
            "csrf_token": csrf_token,
            "error": None,
            "titulo": "",
            "cuerpo": "",
            "modo": "crear",
            "comunicado_id": None,
        },
    )


@router.post("/comunicados/nuevo", dependencies=[Depends(verify_csrf)], response_model=None)
async def crear_comunicado(
    request: Request,
    titulo: str = Form(""),
    cuerpo: str = Form(""),
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
) -> HTMLResponse | RedirectResponse:
    """Crea un comunicado nuevo a partir del formulario. autor_id siempre sale de la sesión."""
    titulo_limpio = titulo.strip()
    cuerpo_limpio = cuerpo.strip()

    error = _validar(titulo_limpio, cuerpo_limpio)
    if error:
        return templates.TemplateResponse(
            request=request,
            name="panel/comunicados/form.html",
            context={
                "usuario": usuario,
                "seccion_activa": "comunicados",
                "csrf_token": get_or_create_csrf_token(request),
                "error": error,
                "titulo": titulo,
                "cuerpo": cuerpo,
                "modo": "crear",
                "comunicado_id": None,
            },
            status_code=422,
        )

    use_case = CreateComunicadoUseCase(repository=comunicado_repository)
    await use_case.execute(
        CrearComunicadoInput(
            titulo=titulo_limpio,
            cuerpo=cuerpo_limpio,
            autor_id=usuario.id,
        )
    )

    return RedirectResponse(url="/panel/comunicados?ok=creado", status_code=303)
