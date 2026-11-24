from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, ForeignKey, String, func
from sqlmodel import Field, Relationship, SQLModel

from app.core.database import created_at_field, deleted_at_field, updated_at_field


class Rol(SQLModel, table=True):
    """Catálogo con clave semántica. Seed: ADMIN, STOCK, PEDIDOS, CLIENT."""

    __tablename__ = "rol"  # type: ignore

    codigo: str = Field(sa_type=String(20), primary_key=True)
    nombre: str = Field(sa_type=String(80))
    descripcion: str | None = None


class UsuarioRol(SQLModel, table=True):
    __tablename__ = "usuario_rol"  # type: ignore

    usuario_id: int = Field(sa_column=Column(ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True))
    rol_codigo: str = Field(
        sa_column=Column(String(20), ForeignKey("rol.codigo", ondelete="RESTRICT"), primary_key=True)
    )
    asignado_por_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("usuario.id", ondelete="SET NULL"), nullable=True),
    )
    asignado_at: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()),
    )

    # Hay dos FK a usuario: se indica cuál usa cada relación.
    usuario: "Usuario" = Relationship(
        back_populates="roles",
        sa_relationship_kwargs={"foreign_keys": "[UsuarioRol.usuario_id]"},
    )


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre: str = Field(sa_type=String(80))
    apellido: str = Field(sa_type=String(80))
    email: str = Field(sa_type=String(254), unique=True, index=True)
    telefono: str | None = Field(default=None, sa_type=String(30))
    password_hash: str = Field(sa_type=CHAR(60))
    disabled: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})
    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()
    deleted_at: datetime | None = deleted_at_field()

    roles: list[UsuarioRol] = Relationship(
        back_populates="usuario",
        sa_relationship_kwargs={
            "foreign_keys": "[UsuarioRol.usuario_id]",
            "cascade": "all, delete-orphan",
            "lazy": "selectin",
        },
    )

    @property
    def codigos_rol(self) -> list[str]:
        return sorted(r.rol_codigo for r in self.roles)
