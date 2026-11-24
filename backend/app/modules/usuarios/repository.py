from sqlalchemy import func
from sqlmodel import select

from app.core.repository import BaseRepository
from app.modules.usuarios.models import Rol, Usuario, UsuarioRol


class UsuarioRepository(BaseRepository[Usuario]):
    model = Usuario

    def get_by_email(self, email: str) -> Usuario | None:
        stmt = select(Usuario).where(func.lower(Usuario.email) == email.lower())
        return self.session.exec(stmt).first()

    def asignar_rol(self, usuario: Usuario, rol_codigo: str, asignado_por_id: int | None = None) -> None:
        usuario.roles.append(UsuarioRol(rol_codigo=rol_codigo, asignado_por_id=asignado_por_id))  # type: ignore
        self.session.flush()


class RolRepository(BaseRepository[Rol]):
    model = Rol
