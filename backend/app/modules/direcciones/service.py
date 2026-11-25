"""Lógica de direcciones de entrega. Cada usuario ve y modifica solo las suyas."""

from app.core.errors import NotFoundError
from app.modules.direcciones.models import DireccionEntrega
from app.modules.direcciones.schemas import (
    DireccionCreate,
    DireccionRead,
    DireccionUpdate,
)
from app.modules.direcciones.uow import DireccionesUnitOfWork


def to_read(d: DireccionEntrega) -> DireccionRead:
    return DireccionRead(
        id=d.id or 0,
        alias=d.alias,
        linea1=d.linea1,
        linea2=d.linea2,
        ciudad=d.ciudad,
        provincia=d.provincia,
        codigo_postal=d.codigo_postal,
        lat=d.lat,
        lng=d.lng,
        es_principal=d.es_principal,
        created_at=d.created_at,
    )


def _propia_o_404(uow: DireccionesUnitOfWork, direccion_id: int, usuario_id: int):
    direccion = uow.direcciones.get_propia(direccion_id, usuario_id)
    if direccion is None:
        # Si es de otro usuario también damos 404: no revelamos que existe.
        raise NotFoundError("Dirección no encontrada", code="DIRECCION_NO_ENCONTRADA")
    return direccion


def listar(uow: DireccionesUnitOfWork, usuario_id: int) -> list[DireccionRead]:
    with uow:
        return [to_read(d) for d in uow.direcciones.listar_de_usuario(usuario_id)]


def crear(uow: DireccionesUnitOfWork, usuario_id: int, datos: DireccionCreate) -> DireccionRead:
    with uow:
        es_primera = not uow.direcciones.listar_de_usuario(usuario_id)
        # La primera dirección es principal sí o sí; si no, solo si lo piden.
        principal = datos.es_principal or es_primera
        if principal:
            uow.direcciones.quitar_principal(usuario_id)
        campos = datos.model_dump(exclude={"es_principal"})
        direccion = uow.direcciones.create(DireccionEntrega(usuario_id=usuario_id, es_principal=principal, **campos))
        return to_read(direccion)


def actualizar(uow: DireccionesUnitOfWork, usuario_id: int, direccion_id: int, datos: DireccionUpdate) -> DireccionRead:
    with uow:
        direccion = _propia_o_404(uow, direccion_id, usuario_id)
        uow.direcciones.update(direccion, datos.model_dump())
        return to_read(direccion)


def marcar_principal(uow: DireccionesUnitOfWork, usuario_id: int, direccion_id: int) -> DireccionRead:
    with uow:
        direccion = _propia_o_404(uow, direccion_id, usuario_id)
        if not direccion.es_principal:
            uow.direcciones.quitar_principal(usuario_id)
            uow.direcciones.update(direccion, {"es_principal": True})
        return to_read(direccion)


def eliminar(uow: DireccionesUnitOfWork, usuario_id: int, direccion_id: int) -> None:
    with uow:
        direccion = _propia_o_404(uow, direccion_id, usuario_id)
        uow.direcciones.soft_delete(direccion)
