from datetime import datetime

from pydantic import BaseModel, Field


class UsuarioRead(BaseModel):
    """Lo que el administrador ve de un usuario. Nunca incluye el hash de la contraseña."""

    id: int
    nombre: str
    apellido: str
    email: str
    telefono: str | None
    disabled: bool
    roles: list[str]
    created_at: datetime
    deleted_at: datetime | None


class UsuarioUpdate(BaseModel):
    """Datos editables de un usuario. El email no se modifica."""

    nombre: str = Field(min_length=1, max_length=80)
    apellido: str = Field(min_length=1, max_length=80)
    telefono: str | None = Field(default=None, max_length=30)


class RolesUpdate(BaseModel):
    """Reemplaza todos los roles del usuario por esta lista (al menos uno)."""

    roles: list[str] = Field(min_length=1)


class EstadoUpdate(BaseModel):
    """True bloquea al usuario, False lo desbloquea."""

    disabled: bool
