from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.dtos.content_management_dto import CrearNoticiaInput, EditarNoticiaInput
from src.application.use_cases.content.create_noticia import CreateNoticiaUseCase
from src.application.use_cases.content.get_noticia import GetNoticiaUseCase
from src.application.use_cases.content.list_noticias import ListNoticiasUseCase
from src.application.use_cases.content.update_noticia import UpdateNoticiaUseCase
from src.domain.auth.entities import Usuario
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.fastapi.csrf import get_or_create_csrf_token, verify_csrf
from src.infrastructure.fastapi.dependencies import get_noticia_repository, require_authority, templates

router = APIRouter(prefix="/panel", dependencies=[Depends(require_authority)], tags=["panel-noticias"])

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


@router.get("/noticias")
async def listar_noticias(
    request: Request,
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
    ok: str | None = None,
) -> HTMLResponse:
    """Listado administrativo de noticias."""
    use_case = ListNoticiasUseCase(repository=noticia_repository)
    noticias = await use_case.execute()
    return templates.TemplateResponse(
        request=request,
        name="panel/noticias/list.html",
        context={"usuario": usuario, "noticias": noticias, "seccion_activa": "noticias", "ok": ok},
    )


@router.get("/noticias/nueva")
async def form_nueva_noticia(
    request: Request,
    usuario: Usuario = Depends(require_authority),
) -> HTMLResponse:
    """Muestra el formulario de creación de noticia."""
    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/noticias/form.html",
        context={
            "usuario": usuario,
            "seccion_activa": "noticias",
            "csrf_token": csrf_token,
            "error": None,
            "titulo": "",
            "cuerpo": "",
            "publicada": True,
            "modo": "crear",
            "noticia_id": None,
        },
    )


@router.post("/noticias/nueva", dependencies=[Depends(verify_csrf)], response_model=None)
async def crear_noticia(
    request: Request,
    titulo: str = Form(""),
    cuerpo: str = Form(""),
    publicada: str | None = Form(None),
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
) -> HTMLResponse | RedirectResponse:
    """Crea una noticia nueva a partir del formulario. autor_id siempre sale de la sesión."""
    titulo_limpio = titulo.strip()
    cuerpo_limpio = cuerpo.strip()
    publicada_bool = publicada is not None

    error = _validar(titulo_limpio, cuerpo_limpio)
    if error:
        return templates.TemplateResponse(
            request=request,
            name="panel/noticias/form.html",
            context={
                "usuario": usuario,
                "seccion_activa": "noticias",
                "csrf_token": get_or_create_csrf_token(request),
                "error": error,
                "titulo": titulo,
                "cuerpo": cuerpo,
                "publicada": publicada_bool,
                "modo": "crear",
                "noticia_id": None,
            },
            status_code=422,
        )

    use_case = CreateNoticiaUseCase(repository=noticia_repository)
    await use_case.execute(
        CrearNoticiaInput(
            titulo=titulo_limpio,
            cuerpo=cuerpo_limpio,
            autor_id=usuario.id,
            publicada=publicada_bool,
        )
    )

    return RedirectResponse(url="/panel/noticias?ok=creada", status_code=303)


@router.get("/noticias/{noticia_id}/editar")
async def form_editar_noticia(
    request: Request,
    noticia_id: str,
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
) -> HTMLResponse:
    """Muestra el formulario de edición de una noticia existente, precargado."""
    noticia = await GetNoticiaUseCase(repository=noticia_repository).execute(noticia_id)
    if noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/noticias/form.html",
        context={
            "usuario": usuario,
            "seccion_activa": "noticias",
            "csrf_token": csrf_token,
            "error": None,
            "titulo": noticia.titulo,
            "cuerpo": noticia.cuerpo,
            "publicada": noticia.publicada,
            "modo": "editar",
            "noticia_id": noticia.id,
        },
    )


@router.post("/noticias/{noticia_id}/editar", dependencies=[Depends(verify_csrf)], response_model=None)
async def editar_noticia(
    request: Request,
    noticia_id: str,
    titulo: str = Form(""),
    cuerpo: str = Form(""),
    publicada: str | None = Form(None),
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
) -> HTMLResponse | RedirectResponse:
    """Edita una noticia existente. autor_id, id y created_at nunca se toman del body."""
    titulo_limpio = titulo.strip()
    cuerpo_limpio = cuerpo.strip()
    publicada_bool = publicada is not None

    error = _validar(titulo_limpio, cuerpo_limpio)
    if error:
        return templates.TemplateResponse(
            request=request,
            name="panel/noticias/form.html",
            context={
                "usuario": usuario,
                "seccion_activa": "noticias",
                "csrf_token": get_or_create_csrf_token(request),
                "error": error,
                "titulo": titulo,
                "cuerpo": cuerpo,
                "publicada": publicada_bool,
                "modo": "editar",
                "noticia_id": noticia_id,
            },
            status_code=422,
        )

    use_case = UpdateNoticiaUseCase(repository=noticia_repository)
    try:
        await use_case.execute(
            EditarNoticiaInput(
                id=noticia_id,
                titulo=titulo_limpio,
                cuerpo=cuerpo_limpio,
                publicada=publicada_bool,
            )
        )
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    return RedirectResponse(url="/panel/noticias?ok=editada", status_code=303)
