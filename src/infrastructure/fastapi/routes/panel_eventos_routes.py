from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.dtos.content_management_dto import CrearEventoInput, EditarEventoInput
from src.application.gateways.image_storage_gateway import ImageStorageGateway, ImageValidationError
from src.application.use_cases.content.create_evento import CreateEventoUseCase
from src.application.use_cases.content.delete_evento import DeleteEventoUseCase
from src.application.use_cases.content.get_evento import GetEventoUseCase
from src.application.use_cases.content.list_eventos import ListEventosUseCase
from src.application.use_cases.content.update_evento import UpdateEventoUseCase
from src.domain.auth.entities import Usuario
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.repositories import EventoRepository
from src.infrastructure.fastapi.csrf import get_or_create_csrf_token, verify_csrf
from src.infrastructure.fastapi.dependencies import get_evento_repository, get_image_storage_gateway, require_authority, templates

_CATEGORIA_IMAGEN = "eventos"


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
    descripcion: str,
    fecha_evento: str,
    lugar: str,
    publicada: bool,
    modo: str,
    evento_id: str | None,
    imagen_actual: str | None,
) -> HTMLResponse:
    """Construye la respuesta 422 que reabre el formulario con el error y los datos ya ingresados."""
    return templates.TemplateResponse(
        request=request,
        name="panel/eventos/form.html",
        context={
            "usuario": usuario,
            "seccion_activa": "eventos",
            "csrf_token": get_or_create_csrf_token(request),
            "error": error,
            "titulo": titulo,
            "descripcion": descripcion,
            "fecha_evento": fecha_evento,
            "lugar": lugar,
            "publicada": publicada,
            "modo": modo,
            "evento_id": evento_id,
            "imagen_actual": imagen_actual,
        },
        status_code=422,
    )


router = APIRouter(prefix="/panel", dependencies=[Depends(require_authority)], tags=["panel-eventos"])

_TITULO_MAX_LENGTH = 200


def _normalizar_campos(
    titulo: str, descripcion: str, fecha_evento: str, lugar: str, publicada: str | None, quitar_imagen: str | None
) -> tuple[str, str, str, str | None, bool, bool]:
    """Limpia (strip) y convierte los campos crudos del form a los tipos que esperan los DTOs."""
    return (
        titulo.strip(),
        descripcion.strip(),
        fecha_evento.strip(),
        lugar.strip() or None,
        publicada is not None,
        quitar_imagen is not None,
    )


async def _persistir_edicion(use_case: UpdateEventoUseCase, input: EditarEventoInput) -> RedirectResponse:
    """Ejecuta la edición y redirige; traduce EntityNotFoundError a 404 HTTP."""
    try:
        await use_case.execute(input)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return RedirectResponse(url="/panel/eventos?ok=editado", status_code=303)


def _validar(titulo: str, descripcion: str, fecha_evento: str) -> str | None:
    """Valida título/descripción/fecha ya limpios (strip aplicado por el llamador). Devuelve el mensaje de error o None."""
    if not titulo:
        return "El título es obligatorio."
    if len(titulo) > _TITULO_MAX_LENGTH:
        return f"El título no puede superar los {_TITULO_MAX_LENGTH} caracteres."
    if not descripcion:
        return "La descripción es obligatoria."
    if not fecha_evento:
        return "La fecha del evento es obligatoria."
    try:
        datetime.fromisoformat(fecha_evento)
    except ValueError:
        return "La fecha del evento no es válida."
    return None


@router.get("/eventos")
async def listar_eventos(
    request: Request,
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
    ok: str | None = None,
) -> HTMLResponse:
    """Listado administrativo de eventos."""
    use_case = ListEventosUseCase(repository=evento_repository)
    eventos = await use_case.execute()
    return templates.TemplateResponse(
        request=request,
        name="panel/eventos/list.html",
        context={"usuario": usuario, "eventos": eventos, "seccion_activa": "eventos", "ok": ok},
    )


@router.get("/eventos/nuevo")
async def form_nuevo_evento(
    request: Request,
    usuario: Usuario = Depends(require_authority),
) -> HTMLResponse:
    """Muestra el formulario de creación de evento."""
    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/eventos/form.html",
        context={
            "usuario": usuario,
            "seccion_activa": "eventos",
            "csrf_token": csrf_token,
            "error": None,
            "titulo": "",
            "descripcion": "",
            "fecha_evento": "",
            "lugar": "",
            "publicada": False,
            "modo": "crear",
            "evento_id": None,
            "imagen_actual": None,
        },
    )


@router.post("/eventos/nuevo", dependencies=[Depends(verify_csrf)], response_model=None)
async def crear_evento(
    request: Request,
    titulo: str = Form(""),
    descripcion: str = Form(""),
    fecha_evento: str = Form(""),
    lugar: str = Form(""),
    publicada: str | None = Form(None),
    imagen: UploadFile | None = File(None),
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> HTMLResponse | RedirectResponse:
    """Crea un evento nuevo a partir del formulario. autor_id siempre sale de la sesión."""
    titulo_limpio = titulo.strip()
    descripcion_limpia = descripcion.strip()
    fecha_evento_limpia = fecha_evento.strip()
    lugar_limpio = lugar.strip() or None
    publicada_bool = publicada is not None

    error = _validar(titulo_limpio, descripcion_limpia, fecha_evento_limpia)
    ruta_imagen: str | None = None
    if not error:
        ruta_imagen, error = await _guardar_imagen_si_corresponde(imagen, image_gateway)

    if error:
        return _form_error_response(
            request,
            usuario=usuario,
            error=error,
            titulo=titulo,
            descripcion=descripcion,
            fecha_evento=fecha_evento,
            lugar=lugar,
            publicada=publicada_bool,
            modo="crear",
            evento_id=None,
            imagen_actual=None,
        )

    use_case = CreateEventoUseCase(repository=evento_repository)
    await use_case.execute(
        CrearEventoInput(
            titulo=titulo_limpio,
            descripcion=descripcion_limpia,
            fecha_evento=fecha_evento_limpia,
            lugar=lugar_limpio,
            autor_id=usuario.id,
            publicada=publicada_bool,
            imagen=ruta_imagen,
        )
    )

    return RedirectResponse(url="/panel/eventos?ok=creado", status_code=303)


@router.get("/eventos/{evento_id}/editar")
async def form_editar_evento(
    request: Request,
    evento_id: str,
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
) -> HTMLResponse:
    """Muestra el formulario de edición de un evento existente, precargado."""
    evento = await GetEventoUseCase(repository=evento_repository).execute(evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/eventos/form.html",
        context={
            "usuario": usuario,
            "seccion_activa": "eventos",
            "csrf_token": csrf_token,
            "error": None,
            "titulo": evento.titulo,
            "descripcion": evento.descripcion,
            # datetime-local espera "YYYY-MM-DDTHH:MM" (sin segundos); el dominio guarda ISO completo.
            "fecha_evento": evento.fecha_evento[:16],
            "lugar": evento.lugar or "",
            "publicada": evento.publicada,
            "modo": "editar",
            "evento_id": evento.id,
            "imagen_actual": evento.imagen,
        },
    )


@router.post("/eventos/{evento_id}/editar", dependencies=[Depends(verify_csrf)], response_model=None)
async def editar_evento(
    request: Request,
    evento_id: str,
    titulo: str = Form(""),
    descripcion: str = Form(""),
    fecha_evento: str = Form(""),
    lugar: str = Form(""),
    publicada: str | None = Form(None),
    imagen: UploadFile | None = File(None),
    quitar_imagen: str | None = Form(None),
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> HTMLResponse | RedirectResponse:
    """Edita un evento existente. autor_id, id y created_at nunca se toman del body."""
    titulo_limpio, descripcion_limpia, fecha_evento_limpia, lugar_limpio, publicada_bool, quitar_imagen_bool = (
        _normalizar_campos(titulo, descripcion, fecha_evento, lugar, publicada, quitar_imagen)
    )

    evento_actual = await GetEventoUseCase(repository=evento_repository).execute(evento_id)
    if evento_actual is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    error = _validar(titulo_limpio, descripcion_limpia, fecha_evento_limpia)
    ruta_imagen: str | None = None
    if not error:
        ruta_imagen, error = await _guardar_imagen_si_corresponde(imagen, image_gateway)

    if error:
        return _form_error_response(
            request,
            usuario=usuario,
            error=error,
            titulo=titulo,
            descripcion=descripcion,
            fecha_evento=fecha_evento,
            lugar=lugar,
            publicada=publicada_bool,
            modo="editar",
            evento_id=evento_id,
            imagen_actual=evento_actual.imagen,
        )

    use_case = UpdateEventoUseCase(repository=evento_repository, image_gateway=image_gateway)
    return await _persistir_edicion(
        use_case,
        EditarEventoInput(
            id=evento_id,
            titulo=titulo_limpio,
            descripcion=descripcion_limpia,
            fecha_evento=fecha_evento_limpia,
            lugar=lugar_limpio,
            publicada=publicada_bool,
            imagen=ruta_imagen,
            quitar_imagen=quitar_imagen_bool,
        ),
    )


@router.get("/eventos/{evento_id}/eliminar")
async def confirmar_eliminar_evento(
    request: Request,
    evento_id: str,
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
) -> HTMLResponse:
    """Muestra la página de confirmación de eliminación. No elimina nada."""
    evento = await GetEventoUseCase(repository=evento_repository).execute(evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    csrf_token = get_or_create_csrf_token(request)
    return templates.TemplateResponse(
        request=request,
        name="panel/eventos/eliminar.html",
        context={
            "usuario": usuario,
            "seccion_activa": "eventos",
            "csrf_token": csrf_token,
            "evento": evento,
        },
    )


@router.post("/eventos/{evento_id}/eliminar", dependencies=[Depends(verify_csrf)], response_model=None)
async def eliminar_evento(
    request: Request,
    evento_id: str,
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
    image_gateway: ImageStorageGateway = Depends(get_image_storage_gateway),
) -> RedirectResponse:
    """Elimina un evento existente. DeleteEventoUseCase es idempotente, por eso se
    verifica existencia antes con GetEventoUseCase para poder responder 404."""
    evento = await GetEventoUseCase(repository=evento_repository).execute(evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    await DeleteEventoUseCase(repository=evento_repository, image_gateway=image_gateway).execute(evento_id)

    return RedirectResponse(url="/panel/eventos?ok=eliminado", status_code=303)
