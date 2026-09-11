from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.dtos.auth_dto import LoginInput
from src.application.gateways.password_hasher_gateway import PasswordHasherGateway
from src.application.use_cases.auth.authenticate_usuario import AuthenticateUsuarioUseCase
from src.domain.auth.repositories import UsuarioRepository
from src.domain.common.exceptions import CredencialesInvalidasError
from src.infrastructure.fastapi.dependencies import get_current_user, get_password_hasher, get_usuario_repository, templates

router = APIRouter(prefix="/panel", tags=["auth"])


@router.get("/login", response_model=None)
async def login_form(
    request: Request,
    usuario_repository: UsuarioRepository = Depends(get_usuario_repository),
) -> HTMLResponse | RedirectResponse:
    """Muestra el formulario de login. Si ya hay sesión válida, redirige al panel."""
    usuario = await get_current_user(request, usuario_repository=usuario_repository)
    if usuario is not None:
        return RedirectResponse(url="/panel", status_code=303)

    return templates.TemplateResponse(request=request, name="panel/login.html", context={"error": None})


@router.post("/login", response_model=None)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    usuario_repository: UsuarioRepository = Depends(get_usuario_repository),
    password_hasher: PasswordHasherGateway = Depends(get_password_hasher),
) -> HTMLResponse | RedirectResponse:
    """Autentica a una autoridad por email y contraseña (formulario HTML, sin JS)."""
    use_case = AuthenticateUsuarioUseCase(repository=usuario_repository, password_hasher=password_hasher)
    try:
        usuario = await use_case.execute(LoginInput(email=email, password=password))
    except CredencialesInvalidasError:
        return templates.TemplateResponse(
            request=request,
            name="panel/login.html",
            context={"error": "Email o contraseña incorrectos"},
            status_code=401,
        )

    request.session["user_id"] = usuario.id
    return RedirectResponse(url="/panel", status_code=303)


@router.post("/logout")
async def logout(request: Request) -> RedirectResponse:
    """Cierra la sesión de la autoridad autenticada."""
    request.session.clear()
    return RedirectResponse(url="/panel/login", status_code=303)
