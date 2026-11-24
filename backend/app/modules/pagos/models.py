from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Column, ForeignKey, Numeric, String
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field, updated_at_field


class FormaPago(SQLModel, table=True):
    """Seed: EFECTIVO, TRANSFERENCIA (habilitadas) y MERCADOPAGO (deshabilitada)."""

    __tablename__ = "forma_pago"

    codigo: str = Field(sa_type=String(20), primary_key=True)
    nombre: str = Field(sa_type=String(80))
    habilitado: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})


class Pago(SQLModel, table=True):
    __tablename__ = "pago"

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    pedido_id: int = Field(sa_column=Column(ForeignKey("pedido.id", ondelete="CASCADE"), nullable=False, index=True))
    forma_pago_codigo: str = Field(
        sa_column=Column(String(20), ForeignKey("forma_pago.codigo", ondelete="RESTRICT"), nullable=False)
    )
    monto: Decimal = Field(sa_type=Numeric(10, 2))
    mp_payment_id: int | None = Field(default=None, sa_column=Column(BigInteger, unique=True, nullable=True))
    mp_status: str = Field(default="pending", sa_type=String(30), sa_column_kwargs={"server_default": "pending"})
    mp_status_detail: str | None = Field(default=None, sa_type=String(120))
    external_reference: str = Field(sa_type=String(100), unique=True, index=True)
    idempotency_key: str = Field(sa_type=String(100), unique=True)
    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()
