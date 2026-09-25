from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.dtos.content_management_dto import CrearNoticiaInput, EditarNoticiaInput
from src.application.gateways.image_storage_gateway import ImageStorageGateway, ImageValidationError
from src.application.use_cases.content.create_noticia import CreateNoticiaUseCase
from src.application.use_cases.content.delete_noticia import DeleteNoticiaUseCase
from src.application.use_cases.content.get_noticia import GetNoticiaUseCase
from src.application.use_cases.content.list_noticias import ListNoticiasUseCase
from src.application.use_cases.content.update_noticia import UpdateNoticiaUseCase
from src.domain.auth.entities import Usuario
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.repositories import NoticiaRepository
from src.infrastructure.fastapi.csrf import get_or_create_csrf_token, verify_csrf
from src.infrastructure.fastapi.dependencies import get_image_storage_gateway, get_noticia_repository, require_authority, templates

_CATEGORIA_IMAGEN = "noticias"


async def _guardar_imagen_si_corresponde(
    imagen: UploadFile | None, image_gateway: ImageStorageGateway
) -> tuple[str | None, str | None]:
    """Valida y guarda una imagen opcional subida desde el formulario.

    Devuelve (ruta_relativa, error). `imagen` sin nombre de archivo se
    interpreta como "no se seleccionó ningún archivo" (comportamiento normal
    de un <input type="file"> vacío en un formulario multipart).
    """
    if imagen is None or not imagen.filename:
        return None, None
    contenido = await imagen.read()
    try:
        ruta = await image_gateway.save(_CATEGORIA_IMAGEN, imagen.filename, imagen.content_type, contenido)
    except ImageValidationError as exc:
        return None, str(exc)
    return ruta, None


def _form_error_response(
    request: Request,
    *,
    usuario: Usuario,
    error: str,
    titulo: str,
    cuerpo: str,
    publicada: bool,
    modo: str,
    noticia_id: str | None,
    imagen_actual: str | None,
) -> HTMLResponse:
    """Construye la respuesta 422 que reabre el formulario con el error y los datos ya ingresados."""
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
            "publicada": publicada,
            "modo": modo,
            "noticia_id": noticia_id,
            "imagen_actual": imagen_actual,
        },
        status_code=422,
    )


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
            "imagen_actual": None,
        },
    )


@router.post("/noticias/nueva", dependencies=[Depends(verify_csrf)], response_model=None)
async def crear_noticia(
    request: Request,
    titulo: str = Form(""),
    cuerpo: str = Form(""),
    publicada: str | None = Form(None),
    imagen: UploadFile | None = File(None),
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> HTMLResponse | RedirectResponse:
    """Crea una noticia nueva a partir del formulario. autor_id siempre sale de la sesión."""
    titulo_limpio = titulo.strip()
    cuerpo_limpio = cuerpo.strip()
    publicada_bool = publicada is not None

    error = _validar(titulo_limpio, cuerpo_limpio)
    ruta_imagen: str | None = None
    if not error:
        ruta_imagen, error = await _guardar_imagen_si_corresponde(imagen, image_gateway)

    if error:
        return _form_error_response(
            request,
            usuario=usuario,
            error=error,
            titulo=titulo,
            cuerpo=cuerpo,
            publicada=publicada_bool,
            modo="crear",
            noticia_id=None,
            imagen_actual=None,
        )

    use_case = CreateNoticiaUseCase(repository=noticia_repository)
    await use_case.execute(
        CrearNoticiaInput(
            titulo=titulo_limpio,
            cuerpo=cuerpo_limpio,
            autor_id=usuario.id,
            publicada=publicada_bool,
            imagen=ruta_imagen,
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
            "imagen_actual": noticia.imagen,
        },
    )


@router.post("/noticias/{noticia_id}/editar", dependencies=[Depends(verify_csrf)], response_model=None)
async def editar_noticia(
    request: Request,
    noticia_id: str,
    titulo: str = Form(""),
    cuerpo: str = Form(""),
    publicada: str | None = Form(None),
    imagen: UploadFile | None = File(None),
    quitar_imagen: str | None = Form(None),
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> HTMLResponse | RedirectResponse:
    """Edita una noticia existente. autor_id, id y created_at nunca se toman del body."""
    titulo_limpio = titulo.strip()
    cuerpo_limpio = cuerpo.strip()
    publicada_bool = publicada is not None
    quitar_imagen_bool = quitar_imagen is not None

    noticia_actual = await GetNoticiaUseCase(repository=noticia_repository).execute(noticia_id)
    if noticia_actual is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    error = _validar(titulo_limpio, cuerpo_limpio)
    ruta_imagen: str | None = None
    if not error:
        ruta_imagen, error = await _guardar_imagen_si_corresponde(imagen, image_gateway)

    if error:
        return _form_error_response(
            request,
            usuario=usuario,
            error=error,
            titulo=titulo,
            cuerpo=cuerpo,
            publicada=publicada_bool,
            modo="editar",
            noticia_id=noticia_id,
            imagen_actual=noticia_actual.imagen,
        )

    use_case = UpdateNoticiaUseCase(repository=noticia_repository, image_gateway=image_gateway)
    try:
        await use_case.execute(
            EditarNoticiaInput(
                id=noticia_id,
                titulo=titulo_limpio,
                cuerpo=cuerpo_limpio,
                publicada=publicada_bool,
                imagen=ruta_imagen,
                quitar_imagen=quitar_imagen_bool,
            )
        )
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    return RedirectResponse(url="/panel/noticias?ok=editada", status_code=303)


@router.get("/noticias/{noticia_id}/eliminar")
async def confirmar_eliminar_noticia(
    request: Request,
    noticia_id: str,
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
) -> HTMLResponse:
    """Muestra la página de confirmación de eliminación. No elimina nada."""
    noticia = await GetNoticiaUseCase(repository=noticia_repository).execute(noticia_id)
    if noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/noticias/eliminar.html",
        context={
            "usuario": usuario,
            "seccion_activa": "noticias",
            "csrf_token": csrf_token,
            "noticia": noticia,
        },
    )


@router.post("/noticias/{noticia_id}/eliminar", dependencies=[Depends(verify_csrf)], response_model=None)
async def eliminar_noticia(
    request: Request,
    noticia_id: str,
    usuario: Usuario = Depends(require_authority),
    noticia_repository: NoticiaRepository = Depends(get_noticia_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> RedirectResponse:
    """Elimina una noticia existente. DeleteNoticiaUseCase es idempotente, por eso se
    verifica existencia antes con GetNoticiaUseCase para poder responder 404."""
    noticia = await GetNoticiaUseCase(repository=noticia_repository).execute(noticia_id)
    if noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    await DeleteNoticiaUseCase(repository=noticia_repository, image_gateway=image_gateway).execute(noticia_id)

    return RedirectResponse(url="/panel/noticias?ok=eliminada", status_code=303)
