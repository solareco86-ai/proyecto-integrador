from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.dtos.content_management_dto import CrearComunicadoInput, EditarComunicadoInput
from src.application.gateways.image_storage_gateway import ImageStorageGateway, ImageValidationError
from src.application.use_cases.content.create_comunicado import CreateComunicadoUseCase
from src.application.use_cases.content.delete_comunicado import DeleteComunicadoUseCase
from src.application.use_cases.content.get_comunicado import GetComunicadoUseCase
from src.application.use_cases.content.list_comunicados import ListComunicadosUseCase
from src.application.use_cases.content.update_comunicado import UpdateComunicadoUseCase
from src.domain.auth.entities import Usuario
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.repositories import ComunicadoRepository
from src.infrastructure.fastapi.csrf import get_or_create_csrf_token, verify_csrf
from src.infrastructure.fastapi.dependencies import get_comunicado_repository, get_image_storage_gateway, require_authority, templates

_CATEGORIA_IMAGEN = "comunicados"


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
    comunicado_id: str | None,
    imagen_actual: str | None,
) -> HTMLResponse:
    """Construye la respuesta 422 que reabre el formulario con el error y los datos ya ingresados."""
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
            "publicada": publicada,
            "modo": modo,
            "comunicado_id": comunicado_id,
            "imagen_actual": imagen_actual,
        },
        status_code=422,
    )


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
            "publicada": False,
            "modo": "crear",
            "comunicado_id": None,
            "imagen_actual": None,
        },
    )


@router.post("/comunicados/nuevo", dependencies=[Depends(verify_csrf)], response_model=None)
async def crear_comunicado(
    request: Request,
    titulo: str = Form(""),
    cuerpo: str = Form(""),
    publicada: str | None = Form(None),
    imagen: UploadFile | None = File(None),
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> HTMLResponse | RedirectResponse:
    """Crea un comunicado nuevo a partir del formulario. autor_id siempre sale de la sesión."""
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
            comunicado_id=None,
            imagen_actual=None,
        )

    use_case = CreateComunicadoUseCase(repository=comunicado_repository)
    await use_case.execute(
        CrearComunicadoInput(
            titulo=titulo_limpio,
            cuerpo=cuerpo_limpio,
            autor_id=usuario.id,
            publicada=publicada_bool,
            imagen=ruta_imagen,
        )
    )

    return RedirectResponse(url="/panel/comunicados?ok=creado", status_code=303)


@router.get("/comunicados/{comunicado_id}/editar")
async def form_editar_comunicado(
    request: Request,
    comunicado_id: str,
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
) -> HTMLResponse:
    """Muestra el formulario de edición de un comunicado existente, precargado."""
    comunicado = await GetComunicadoUseCase(repository=comunicado_repository).execute(comunicado_id)
    if comunicado is None:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")

    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/comunicados/form.html",
        context={
            "usuario": usuario,
            "seccion_activa": "comunicados",
            "csrf_token": csrf_token,
            "error": None,
            "titulo": comunicado.titulo,
            "cuerpo": comunicado.cuerpo,
            "publicada": comunicado.publicada,
            "modo": "editar",
            "comunicado_id": comunicado.id,
            "imagen_actual": comunicado.imagen,
        },
    )


@router.post("/comunicados/{comunicado_id}/editar", dependencies=[Depends(verify_csrf)], response_model=None)
async def editar_comunicado(
    request: Request,
    comunicado_id: str,
    titulo: str = Form(""),
    cuerpo: str = Form(""),
    publicada: str | None = Form(None),
    imagen: UploadFile | None = File(None),
    quitar_imagen: str | None = Form(None),
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> HTMLResponse | RedirectResponse:
    """Edita un comunicado existente. autor_id, id y created_at nunca se toman del body."""
    titulo_limpio = titulo.strip()
    cuerpo_limpio = cuerpo.strip()
    publicada_bool = publicada is not None
    quitar_imagen_bool = quitar_imagen is not None

    comunicado_actual = await GetComunicadoUseCase(repository=comunicado_repository).execute(comunicado_id)
    if comunicado_actual is None:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")

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
            comunicado_id=comunicado_id,
            imagen_actual=comunicado_actual.imagen,
        )

    use_case = UpdateComunicadoUseCase(repository=comunicado_repository, image_gateway=image_gateway)
    try:
        await use_case.execute(
            EditarComunicadoInput(
                id=comunicado_id,
                titulo=titulo_limpio,
                cuerpo=cuerpo_limpio,
                publicada=publicada_bool,
                imagen=ruta_imagen,
                quitar_imagen=quitar_imagen_bool,
            )
        )
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")

    return RedirectResponse(url="/panel/comunicados?ok=editado", status_code=303)


@router.get("/comunicados/{comunicado_id}/eliminar")
async def confirmar_eliminar_comunicado(
    request: Request,
    comunicado_id: str,
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
) -> HTMLResponse:
    """Muestra la página de confirmación de eliminación. No elimina nada."""
    comunicado = await GetComunicadoUseCase(repository=comunicado_repository).execute(comunicado_id)
    if comunicado is None:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")

    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/comunicados/eliminar.html",
        context={
            "usuario": usuario,
            "seccion_activa": "comunicados",
            "csrf_token": csrf_token,
            "comunicado": comunicado,
        },
    )


@router.post("/comunicados/{comunicado_id}/eliminar", dependencies=[Depends(verify_csrf)], response_model=None)
async def eliminar_comunicado(
    request: Request,
    comunicado_id: str,
    usuario: Usuario = Depends(require_authority),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> RedirectResponse:
    """Elimina un comunicado existente. DeleteComunicadoUseCase es idempotente, por eso se
    verifica existencia antes con GetComunicadoUseCase para poder responder 404."""
    comunicado = await GetComunicadoUseCase(repository=comunicado_repository).execute(comunicado_id)
    if comunicado is None:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")

    await DeleteComunicadoUseCase(repository=comunicado_repository, image_gateway=image_gateway).execute(
        comunicado_id
    )

    return RedirectResponse(url="/panel/comunicados?ok=eliminado", status_code=303)
