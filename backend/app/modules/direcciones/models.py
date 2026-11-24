from datetime import datetime

from sqlalchemy import BigInteger, Column, Double, ForeignKey, Index, String, text
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field, deleted_at_field


class DireccionEntrega(SQLModel, table=True):
    __tablename__ = "direccion_entrega"  # type: ignore
    __table_args__ = (
        # RN-17: a lo sumo una dirección principal activa por usuario.
        Index(
            "uq_direccion_principal_activa",
            "usuario_id",
            unique=True,
            postgresql_where=text("es_principal AND deleted_at IS NULL"),
        ),
    )

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    usuario_id: int = Field(sa_column=Column(ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True))
    alias: str | None = Field(default=None, sa_type=String(50))
    linea1: str
    linea2: str | None = None
    ciudad: str | None = Field(default=None, sa_type=String(100))
    provincia: str | None = Field(default=None, sa_type=String(100))
    codigo_postal: str | None = Field(default=None, sa_type=String(20))
    lat: float | None = Field(default=None, sa_type=Double)
    lng: float | None = Field(default=None, sa_type=Double)
    es_principal: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})
    created_at: datetime = created_at_field()
    deleted_at: datetime | None = deleted_at_field()
