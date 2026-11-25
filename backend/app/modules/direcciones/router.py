"""Endpoints de direcciones (/direcciones). Solo el dueño de cada dirección."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import CurrentUser
from app.core.schemas import ErrorResponse
from app.modules.direcciones import service
from app.modules.direcciones.deps import get_direcciones_uow
from app.modules.direcciones.schemas import (
    DireccionCreate,
    DireccionRead,
    DireccionUpdate,
)
from app.modules.direcciones.uow import DireccionesUnitOfWork

router = APIRouter(prefix="/direcciones", tags=["direcciones"])

DireccionesUoW = Annotated[DireccionesUnitOfWork, Depends(get_direcciones_uow)]
ERRORES = {401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}


@router.get("", response_model=list[DireccionRead], responses=ERRORES)  # type: ignore
def listar(usuario: CurrentUser, uow: DireccionesUoW) -> list[DireccionRead]:
    return service.listar(uow, usuario.id or 0)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DireccionRead, responses=ERRORES)  # type: ignore
def crear(body: DireccionCreate, usuario: CurrentUser, uow: DireccionesUoW) -> DireccionRead:
    return service.crear(uow, usuario.id or 0, body)


@router.put("/{direccion_id}", response_model=DireccionRead, responses=ERRORES)  # type: ignore
def actualizar(direccion_id: int, body: DireccionUpdate, usuario: CurrentUser, uow: DireccionesUoW) -> DireccionRead:
    return service.actualizar(uow, usuario.id or 0, direccion_id, body)


@router.patch("/{direccion_id}/principal", response_model=DireccionRead, responses=ERRORES)  # type: ignore
def marcar_principal(direccion_id: int, usuario: CurrentUser, uow: DireccionesUoW) -> DireccionRead:
    """Marca esta dirección como principal y desmarca la anterior (RN-17)."""
    return service.marcar_principal(uow, usuario.id or 0, direccion_id)


@router.delete("/{direccion_id}", status_code=status.HTTP_204_NO_CONTENT, responses=ERRORES)  # type: ignore
def eliminar(direccion_id: int, usuario: CurrentUser, uow: DireccionesUoW) -> None:
    """Baja lógica de la dirección."""
    service.eliminar(uow, usuario.id or 0, direccion_id)
