from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, CheckConstraint, Column, ForeignKey, Numeric, String
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field, updated_at_field


class EstadoPedido(SQLModel, table=True):
    """Catálogo de estados (seed). Las transiciones permitidas van en core/fsm.py."""

    __tablename__ = "estado_pedido"  # type: ignore

    codigo: str = Field(sa_type=String(20), primary_key=True)
    descripcion: str = Field(sa_type=String(120))
    orden: int
    es_terminal: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})


class Pedido(SQLModel, table=True):
    __tablename__ = "pedido"  # type: ignore
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="subtotal_no_negativo"),
        CheckConstraint("total >= 0", name="total_no_negativo"),
    )

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    usuario_id: int = Field(sa_column=Column(ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False, index=True))
    estado_codigo: str = Field(
        sa_column=Column(
            String(20),
            ForeignKey("estado_pedido.codigo", ondelete="RESTRICT"),
            nullable=False,
            index=True,
        )
    )
    forma_pago_codigo: str = Field(
        sa_column=Column(String(20), ForeignKey("forma_pago.codigo", ondelete="RESTRICT"), nullable=False)
    )
    # NULL = retiro en el local.
    direccion_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("direccion_entrega.id", ondelete="SET NULL"), nullable=True),
    )
    # Snapshot monetario inmutable: los importes quedan fijos aunque cambien los precios.
    subtotal: Decimal = Field(sa_type=Numeric(10, 2))
    descuento: Decimal = Field(
        default=Decimal("0.00"),
        sa_type=Numeric(10, 2),
        sa_column_kwargs={"server_default": "0.00"},
    )
    costo_envio: Decimal = Field(sa_type=Numeric(10, 2))
    total: Decimal = Field(sa_type=Numeric(10, 2))
    # Es la clave de idempotencia del checkout (evita pedidos duplicados).
    external_reference: str = Field(sa_type=String(100), unique=True, index=True)
    notas: str | None = None
    created_at: datetime = created_at_field(index=True)
    updated_at: datetime = updated_at_field()


class DetallePedido(SQLModel, table=True):
    """Clave propia: el mismo producto puede repetirse con distintas exclusiones."""

    __tablename__ = "detalle_pedido"  # type: ignore
    __table_args__ = (CheckConstraint("cantidad >= 1", name="cantidad_minima"),)

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    pedido_id: int = Field(sa_column=Column(ForeignKey("pedido.id", ondelete="CASCADE"), nullable=False, index=True))
    producto_id: int = Field(sa_column=Column(ForeignKey("producto.id", ondelete="RESTRICT"), nullable=False))
    nombre_snapshot: str = Field(sa_type=String(200))
    precio_snapshot: Decimal = Field(sa_type=Numeric(10, 2))
    cantidad: int


class DetallePedidoExclusion(SQLModel, table=True):
    """Ingredientes quitados de una línea ("sin cebolla")."""

    __tablename__ = "detalle_pedido_exclusion"  # type: ignore

    detalle_pedido_id: int = Field(
        sa_column=Column(ForeignKey("detalle_pedido.id", ondelete="CASCADE"), primary_key=True)
    )
    ingrediente_id: int = Field(sa_column=Column(ForeignKey("ingrediente.id", ondelete="RESTRICT"), primary_key=True))


class HistorialEstadoPedido(SQLModel, table=True):
    """Solo se agregan registros, nunca se modifican. El primero tiene estado_desde nulo."""

    __tablename__ = "historial_estado_pedido"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    pedido_id: int = Field(sa_column=Column(ForeignKey("pedido.id", ondelete="CASCADE"), nullable=False, index=True))
    estado_desde: str | None = Field(
        default=None,
        sa_column=Column(String(20), ForeignKey("estado_pedido.codigo", ondelete="RESTRICT"), nullable=True),
    )
    estado_hasta: str = Field(
        sa_column=Column(String(20), ForeignKey("estado_pedido.codigo", ondelete="RESTRICT"), nullable=False)
    )
    usuario_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("usuario.id", ondelete="SET NULL"), nullable=True),
    )
    motivo: str | None = None
    created_at: datetime = created_at_field(index=True)
