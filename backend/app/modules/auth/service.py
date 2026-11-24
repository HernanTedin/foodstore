from dataclasses import dataclass
from datetime import UTC, datetime

from app.core.errors import (
    AccountStateError,
    AuthenticationError,
    ConflictError,
    ValidationError,
)
from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    refresh_expiration,
    verify_password,
)
from app.modules.auth.models import RefreshToken
from app.modules.auth.schemas import PasswordChangeRequest, RegisterRequest, UsuarioMe
from app.modules.auth.uow import AuthUnitOfWork
from app.modules.usuarios.models import Usuario

ROL_CLIENTE = "CLIENT"


@dataclass(frozen=True)
class Tokens:
    access_token: str
    refresh_token: str


def to_usuario_me(usuario: Usuario) -> UsuarioMe:
    return UsuarioMe(
        id=usuario.id or 0,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        telefono=usuario.telefono,
        roles=usuario.codigos_rol,
    )


def _emitir_tokens(uow: AuthUnitOfWork, usuario_id: int) -> Tokens:
    refresh_claro, refresh_hash = generate_refresh_token()
    uow.refresh_tokens.create(
        RefreshToken(usuario_id=usuario_id, token_hash=refresh_hash, expires_at=refresh_expiration())
    )
    return Tokens(create_access_token(usuario_id), refresh_claro)


def registrar(uow: AuthUnitOfWork, datos: RegisterRequest) -> UsuarioMe:
    """El registro público siempre asigna el rol CLIENT."""
    with uow:
        if uow.usuarios.get_by_email(datos.email):
            raise ConflictError("El email ya está registrado", code="EMAIL_EN_USO", field="email")
        usuario = uow.usuarios.create(
            Usuario(
                nombre=datos.nombre.strip(),
                apellido=datos.apellido.strip(),
                email=datos.email.lower(),
                telefono=datos.telefono,
                password_hash=hash_password(datos.password),
            )
        )
        uow.usuarios.asignar_rol(usuario, ROL_CLIENTE)
        return to_usuario_me(usuario)


def login(uow: AuthUnitOfWork, email: str, password: str) -> tuple[Tokens, UsuarioMe]:
    with uow:
        usuario = uow.usuarios.get_by_email(email)
        # Se compara siempre (aunque el email no exista) para no filtrar por tiempo.
        valido = verify_password(password, usuario.password_hash if usuario else DUMMY_HASH)
        if usuario is None or not valido:
            raise AuthenticationError("Email o contraseña incorrectos", code="INVALID_CREDENTIALS")
        if usuario.deleted_at is not None or usuario.disabled:
            raise AccountStateError("La cuenta está bloqueada o dada de baja")
        return _emitir_tokens(uow, usuario.id or 0), to_usuario_me(usuario)


def refrescar(uow: AuthUnitOfWork, refresh_token: str | None) -> Tokens:
    """Emite un access token nuevo y rota el refresh token (revoca el anterior)."""
    if not refresh_token:
        raise AuthenticationError("Falta el refresh token", code="REFRESH_INVALID")
    with uow:
        guardado = uow.refresh_tokens.get_by_hash(hash_refresh_token(refresh_token))
        if guardado is None or guardado.revoked_at is not None or guardado.expires_at <= datetime.now(UTC):
            raise AuthenticationError("Refresh token inválido o expirado", code="REFRESH_INVALID")
        usuario = uow.usuarios.get_by_id(guardado.usuario_id)
        if usuario is None or usuario.deleted_at is not None or usuario.disabled:
            raise AuthenticationError("Usuario inexistente o bloqueado", code="REFRESH_INVALID")
        uow.refresh_tokens.revocar(guardado)
        return _emitir_tokens(uow, usuario.id or 0)


def logout(uow: AuthUnitOfWork, refresh_token: str | None) -> None:
    if not refresh_token:
        return
    with uow:
        guardado = uow.refresh_tokens.get_by_hash(hash_refresh_token(refresh_token))
        if guardado and guardado.revoked_at is None:
            uow.refresh_tokens.revocar(guardado)


def cambiar_password(uow: AuthUnitOfWork, usuario_id: int, datos: PasswordChangeRequest) -> None:
    with uow:
        usuario = uow.usuarios.get_by_id(usuario_id)
        if usuario is None or not verify_password(datos.password_actual, usuario.password_hash):
            raise ValidationError(
                "La contraseña actual no es correcta",
                code="PASSWORD_INCORRECTA",
                field="password_actual",
            )
        uow.usuarios.update(usuario, {"password_hash": hash_password(datos.password_nueva)})
        uow.refresh_tokens.revocar_todos(usuario_id)
