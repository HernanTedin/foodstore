import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, CheckConstraint, Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field, updated_at_field


class EstadoOrdenEnum(enum.StrEnum):
    PLANIFICADA = "PLANIFICADA"
    EN_PROCESO = "EN_PROCESO"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"


# Tipo ENUM de PostgreSQL. Se crea a mano en la migración, por eso create_type=False.
estado_orden_pg = ENUM(
    EstadoOrdenEnum,
    name="estado_orden_enum",
    create_type=False,
    values_callable=lambda e: [m.value for m in e],
)


class OrdenProduccion(SQLModel, table=True):
    __tablename__ = "orden_produccion"  # type: ignore
    __table_args__ = (
        CheckConstraint("cantidad_a_producir > 0", name="cantidad_positiva"),
        # Produce un producto O un ingrediente elaborado, nunca los dos ni ninguno.
        CheckConstraint("num_nonnulls(producto_id, ingrediente_id) = 1", name="salida_xor"),
    )

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    producto_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("producto.id", ondelete="RESTRICT"), nullable=True),
    )
    ingrediente_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("ingrediente.id", ondelete="RESTRICT"), nullable=True),
    )
    cantidad_a_producir: Decimal = Field(sa_type=Numeric(12, 3))
    estado: EstadoOrdenEnum = Field(
        default=EstadoOrdenEnum.PLANIFICADA,
        sa_column=Column(estado_orden_pg, nullable=False, server_default="PLANIFICADA", index=True),
    )
    motivo_cancelacion: str | None = Field(default=None, sa_type=String(200))
    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()
