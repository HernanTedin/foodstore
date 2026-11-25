"""Endpoints de usuarios (/usuarios). Solo ADMIN. HTTP puro: valida y delega."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.deps import require_roles
from app.core.schemas import ErrorResponse, PageParams, Paginated
from app.modules.usuarios import service
from app.modules.usuarios.deps import get_usuarios_uow
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.schemas import (
    EstadoUpdate,
    RolesUpdate,
    UsuarioRead,
    UsuarioUpdate,
)
from app.modules.usuarios.uow import UsuariosUnitOfWork

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

UsuariosUoW = Annotated[UsuariosUnitOfWork, Depends(get_usuarios_uow)]
Admin = Annotated[Usuario, Depends(require_roles("ADMIN"))]
ERRORES = {
    401: {"model": ErrorResponse},
    403: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
}


@router.get("", response_model=Paginated[UsuarioRead], responses=ERRORES)  # type: ignore
def listar(
    _: Admin,
    uow: UsuariosUoW,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    search: str | None = None,
    rol: str | None = None,
    incluir_inactivos: bool = False,
    solo_inactivos: bool = False,
) -> Paginated[UsuarioRead]:
    return service.listar(uow, PageParams(page=page, size=size), search, rol, incluir_inactivos, solo_inactivos)


@router.get("/{usuario_id}", response_model=UsuarioRead, responses=ERRORES)  # type: ignore
def obtener(usuario_id: int, _: Admin, uow: UsuariosUoW) -> UsuarioRead:
    return service.obtener(uow, usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioRead, responses=ERRORES)  # type: ignore
def actualizar(usuario_id: int, body: UsuarioUpdate, _: Admin, uow: UsuariosUoW) -> UsuarioRead:
    return service.actualizar(uow, usuario_id, body)


@router.put("/{usuario_id}/roles", response_model=UsuarioRead, responses=ERRORES)  # type: ignore
def cambiar_roles(usuario_id: int, body: RolesUpdate, admin: Admin, uow: UsuariosUoW) -> UsuarioRead:
    """Reemplaza los roles del usuario y guarda quién los asignó."""
    return service.cambiar_roles(uow, usuario_id, body, admin.id or 0)


@router.patch("/{usuario_id}/estado", response_model=UsuarioRead, responses=ERRORES)  # type: ignore
def cambiar_estado(usuario_id: int, body: EstadoUpdate, admin: Admin, uow: UsuariosUoW) -> UsuarioRead:
    """Bloquea (disabled=true) o desbloquea (disabled=false) al usuario."""
    return service.cambiar_estado(uow, usuario_id, body, admin.id or 0)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, responses=ERRORES)  # type: ignore
def dar_de_baja(usuario_id: int, admin: Admin, uow: UsuariosUoW) -> None:
    """Baja lógica: el usuario queda con deleted_at, no se borra de la base."""
    service.dar_de_baja(uow, usuario_id, admin.id or 0)
