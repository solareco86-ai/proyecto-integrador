from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.dtos.content_management_dto import CrearEventoInput, EditarEventoInput
from src.application.use_cases.content.create_evento import CreateEventoUseCase
from src.application.use_cases.content.delete_evento import DeleteEventoUseCase
from src.application.use_cases.content.get_evento import GetEventoUseCase
from src.application.use_cases.content.list_eventos import ListEventosUseCase
from src.application.use_cases.content.update_evento import UpdateEventoUseCase
from src.domain.auth.entities import Usuario
from src.domain.common.exceptions import EntityNotFoundError
from src.domain.content.repositories import EventoRepository
from src.infrastructure.fastapi.csrf import get_or_create_csrf_token, verify_csrf
from src.infrastructure.fastapi.dependencies import get_evento_repository, require_authority, templates

router = APIRouter(prefix="/panel", dependencies=[Depends(require_authority)], tags=["panel-eventos"])

_TITULO_MAX_LENGTH = 200


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
            "modo": "crear",
            "evento_id": None,
        },
    )


@router.post("/eventos/nuevo", dependencies=[Depends(verify_csrf)], response_model=None)
async def crear_evento(
    request: Request,
    titulo: str = Form(""),
    descripcion: str = Form(""),
    fecha_evento: str = Form(""),
    lugar: str = Form(""),
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
) -> HTMLResponse | RedirectResponse:
    """Crea un evento nuevo a partir del formulario. autor_id siempre sale de la sesión."""
    titulo_limpio = titulo.strip()
    descripcion_limpia = descripcion.strip()
    fecha_evento_limpia = fecha_evento.strip()
    lugar_limpio = lugar.strip() or None

    error = _validar(titulo_limpio, descripcion_limpia, fecha_evento_limpia)
    if error:
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
                "modo": "crear",
                "evento_id": None,
            },
            status_code=422,
        )

    use_case = CreateEventoUseCase(repository=evento_repository)
    await use_case.execute(
        CrearEventoInput(
            titulo=titulo_limpio,
            descripcion=descripcion_limpia,
            fecha_evento=fecha_evento_limpia,
            lugar=lugar_limpio,
            autor_id=usuario.id,
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
            "modo": "editar",
            "evento_id": evento.id,
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
    usuario: Usuario = Depends(require_authority),
    evento_repository: EventoRepository = Depends(get_evento_repository),
) -> HTMLResponse | RedirectResponse:
    """Edita un evento existente. autor_id, id y created_at nunca se toman del body."""
    titulo_limpio = titulo.strip()
    descripcion_limpia = descripcion.strip()
    fecha_evento_limpia = fecha_evento.strip()
    lugar_limpio = lugar.strip() or None

    error = _validar(titulo_limpio, descripcion_limpia, fecha_evento_limpia)
    if error:
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
                "modo": "editar",
                "evento_id": evento_id,
            },
            status_code=422,
        )

    use_case = UpdateEventoUseCase(repository=evento_repository)
    try:
        await use_case.execute(
            EditarEventoInput(
                id=evento_id,
                titulo=titulo_limpio,
                descripcion=descripcion_limpia,
                fecha_evento=fecha_evento_limpia,
                lugar=lugar_limpio,
            )
        )
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return RedirectResponse(url="/panel/eventos?ok=editado", status_code=303)


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
) -> RedirectResponse:
    """Elimina un evento existente. DeleteEventoUseCase es idempotente, por eso se
    verifica existencia antes con GetEventoUseCase para poder responder 404."""
    evento = await GetEventoUseCase(repository=evento_repository).execute(evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    await DeleteEventoUseCase(repository=evento_repository).execute(evento_id)

    return RedirectResponse(url="/panel/eventos?ok=eliminado", status_code=303)
