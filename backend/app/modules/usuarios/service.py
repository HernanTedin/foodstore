"""Lógica de administración de usuarios. Lanza excepciones de dominio.

Cada función abre su transacción con `with uow:`; ninguna hace commit().
"""

from app.core.errors import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
)
from app.core.schemas import PageParams, Paginated
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.schemas import (
    EstadoUpdate,
    RolesUpdate,
    UsuarioRead,
    UsuarioUpdate,
)
from app.modules.usuarios.uow import UsuariosUnitOfWork


def to_read(usuario: Usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id or 0,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        telefono=usuario.telefono,
        disabled=usuario.disabled,
        roles=usuario.codigos_rol,
        created_at=usuario.created_at,
        deleted_at=usuario.deleted_at,
    )


def _get_or_404(uow: UsuariosUnitOfWork, usuario_id: int) -> Usuario:
    usuario = uow.usuarios.get_by_id(usuario_id)
    if usuario is None:
        raise NotFoundError("Usuario no encontrado", code="USUARIO_NO_ENCONTRADO")
    return usuario


def listar(
    uow: UsuariosUnitOfWork,
    params: PageParams,
    search: str | None,
    rol: str | None,
    incluir_inactivos: bool,
    solo_inactivos: bool = False,
) -> Paginated[UsuarioRead]:
    with uow:
        filtros = uow.usuarios.filtros(search, rol, solo_inactivos)
        incluir = incluir_inactivos or solo_inactivos
        total = uow.usuarios.count(filtros, incluir)
        usuarios = uow.usuarios.list(filtros, params, incluir, order_by=[Usuario.id])
        return Paginated.build([to_read(u) for u in usuarios], total, params)


def obtener(uow: UsuariosUnitOfWork, usuario_id: int) -> UsuarioRead:
    with uow:
        return to_read(_get_or_404(uow, usuario_id))


def actualizar(uow: UsuariosUnitOfWork, usuario_id: int, datos: UsuarioUpdate) -> UsuarioRead:
    with uow:
        usuario = _get_or_404(uow, usuario_id)
        uow.usuarios.update(
            usuario,
            {
                "nombre": datos.nombre.strip(),
                "apellido": datos.apellido.strip(),
                "telefono": datos.telefono,
            },
        )
        return to_read(usuario)


def cambiar_roles(uow: UsuariosUnitOfWork, usuario_id: int, datos: RolesUpdate, admin_id: int) -> UsuarioRead:
    with uow:
        usuario = _get_or_404(uow, usuario_id)
        pedidos = set(datos.roles)
        existentes = {r.codigo for r in uow.roles.list()}
        invalidos = pedidos - existentes
        if invalidos:
            raise ValidationError(
                f"Roles inexistentes: {', '.join(sorted(invalidos))}",
                code="ROL_INEXISTENTE",
                field="roles",
            )
        if usuario_id == admin_id and "ADMIN" not in pedidos:
            raise ForbiddenError("No podés quitarte a vos mismo el rol ADMIN", code="AUTO_QUITAR_ADMIN")
        uow.usuarios.reemplazar_roles(usuario, sorted(pedidos), admin_id)
        return to_read(usuario)


def cambiar_estado(uow: UsuariosUnitOfWork, usuario_id: int, datos: EstadoUpdate, admin_id: int) -> UsuarioRead:
    with uow:
        usuario = _get_or_404(uow, usuario_id)
        if usuario_id == admin_id and datos.disabled:
            raise ForbiddenError("No podés bloquearte a vos mismo", code="AUTO_BLOQUEO")
        uow.usuarios.update(usuario, {"disabled": datos.disabled})
        return to_read(usuario)


def dar_de_baja(uow: UsuariosUnitOfWork, usuario_id: int, admin_id: int) -> None:
    with uow:
        usuario = _get_or_404(uow, usuario_id)
        if usuario_id == admin_id:
            raise ForbiddenError("No podés darte de baja a vos mismo", code="AUTO_BAJA")
        if usuario.deleted_at is not None:
            raise ConflictError("El usuario ya está dado de baja", code="YA_DADO_DE_BAJA")
        uow.usuarios.soft_delete(usuario)
