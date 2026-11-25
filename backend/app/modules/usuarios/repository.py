from sqlalchemy import ColumnElement, func, or_
from sqlmodel import col, select

from app.core.repository import BaseRepository
from app.modules.usuarios.models import Rol, Usuario, UsuarioRol


class UsuarioRepository(BaseRepository[Usuario]):
    model = Usuario

    def get_by_email(self, email: str) -> Usuario | None:
        stmt = select(Usuario).where(func.lower(Usuario.email) == email.lower())
        return self.session.exec(stmt).first()

    def filtros(self, search: str | None, rol: str | None, solo_inactivos: bool = False) -> list[ColumnElement[bool]]:
        """Arma las condiciones del listado: búsqueda parcial, rol y solo dados de baja."""
        condiciones: list[ColumnElement[bool]] = []
        if search and search.strip():
            patron = f"%{search.strip()}%"
            condiciones.append(
                or_(
                    col(Usuario.nombre).ilike(patron),
                    col(Usuario.apellido).ilike(patron),
                    col(Usuario.email).ilike(patron),
                )
            )
        if rol:
            condiciones.append(Usuario.roles.any(UsuarioRol.rol_codigo == rol))  # type: ignore[attr-defined]
        if solo_inactivos:
            condiciones.append(col(Usuario.deleted_at).is_not(None))
        return condiciones

    def asignar_rol(self, usuario: Usuario, rol_codigo: str, asignado_por_id: int | None = None) -> None:
        usuario.roles.append(UsuarioRol(rol_codigo=rol_codigo, asignado_por_id=asignado_por_id))  # type: ignore
        self.session.flush()

    def reemplazar_roles(self, usuario: Usuario, codigos: list[str], asignado_por_id: int | None) -> None:
        """Deja al usuario con exactamente esos roles: quita los que sobran y suma los nuevos."""
        actuales = {r.rol_codigo: r for r in usuario.roles}
        for codigo, relacion in actuales.items():
            if codigo not in codigos:
                usuario.roles.remove(relacion)
        for codigo in codigos:
            if codigo not in actuales:
                usuario.roles.append(UsuarioRol(rol_codigo=codigo, asignado_por_id=asignado_por_id))  # type: ignore
        self.session.flush()


class RolRepository(BaseRepository[Rol]):
    model = Rol
