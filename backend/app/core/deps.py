from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Request
from sqlmodel import Session

from app.core.database import get_session
from app.core.errors import AuthenticationError, ForbiddenError
from app.core.security import ACCESS_COOKIE, decode_access_token
from app.modules.usuarios.models import Usuario

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(request: Request, session: SessionDep) -> Usuario:
    token = request.cookies.get(ACCESS_COOKIE)
    if not token:
        raise AuthenticationError("No autenticado")
    usuario_id = decode_access_token(token)
    if usuario_id is None:
        raise AuthenticationError("Token inválido o expirado", code="TOKEN_INVALID")
    usuario = session.get(Usuario, usuario_id)
    if usuario is None or usuario.deleted_at is not None or usuario.disabled:
        raise AuthenticationError("Usuario inexistente o bloqueado", code="TOKEN_INVALID")
    return usuario


CurrentUser = Annotated[Usuario, Depends(get_current_user)]


def require_roles(*roles: str) -> Callable[[Usuario], Usuario]:
    """Exige al menos uno de los roles indicados (403 si no lo tiene)."""
    permitidos = set(roles)

    def _verificar(usuario: CurrentUser) -> Usuario:
        if not permitidos.intersection(usuario.codigos_rol):
            raise ForbiddenError("No tenés permisos para esta acción")
        return usuario

    return _verificar
