from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.deps import CurrentUser
from app.core.schemas import ErrorResponse
from app.core.security import REFRESH_COOKIE, clear_auth_cookies, set_auth_cookies
from app.modules.auth import service
from app.modules.auth.deps import get_auth_uow
from app.modules.auth.schemas import PasswordChangeRequest, RegisterRequest, UsuarioMe
from app.modules.auth.uow import AuthUnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])

AuthUoW = Annotated[AuthUnitOfWork, Depends(get_auth_uow)]
ERRORES = {
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
}


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UsuarioMe,
    responses={409: {"model": ErrorResponse}},
)
def register(body: RegisterRequest, uow: AuthUoW) -> UsuarioMe:
    """Registro público. Siempre asigna el rol CLIENT."""
    return service.registrar(uow, body)


@router.post("/token", response_model=UsuarioMe, responses=ERRORES)  # type: ignore
def login(
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: AuthUoW,
) -> UsuarioMe:
    """Login OAuth2 (username = email). Los tokens viajan solo en cookies HttpOnly."""
    tokens, usuario = service.login(uow, form.username, form.password)
    set_auth_cookies(response, tokens.access_token, tokens.refresh_token)
    return usuario


@router.post("/refresh", status_code=status.HTTP_204_NO_CONTENT, responses=ERRORES)  # type: ignore
def refresh(request: Request, response: Response, uow: AuthUoW) -> None:
    """Nuevo access token y rotación del refresh token (cookie de refresh)."""
    tokens = service.refrescar(uow, request.cookies.get(REFRESH_COOKIE))
    set_auth_cookies(response, tokens.access_token, tokens.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, responses=ERRORES)  # type: ignore
def logout(request: Request, response: Response, _: CurrentUser, uow: AuthUoW) -> None:
    service.logout(uow, request.cookies.get(REFRESH_COOKIE))
    clear_auth_cookies(response)


@router.get("/me", response_model=UsuarioMe, responses=ERRORES)  # type: ignore
def me(usuario: CurrentUser) -> UsuarioMe:
    return service.to_usuario_me(usuario)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT, responses=ERRORES)  # type: ignore
def cambiar_password(body: PasswordChangeRequest, usuario: CurrentUser, response: Response, uow: AuthUoW) -> None:
    """Cambia la contraseña y cierra todas las sesiones."""
    service.cambiar_password(uow, usuario.id or 0, body)
    clear_auth_cookies(response)
