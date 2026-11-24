import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field, deleted_at_field, updated_at_field


class TipoMovimientoEnum(enum.StrEnum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    RESERVA = "RESERVA"
    LIBERACION_RESERVA = "LIBERACION_RESERVA"
    MERMA = "MERMA"
    AJUSTE_POSITIVO = "AJUSTE_POSITIVO"
    AJUSTE_NEGATIVO = "AJUSTE_NEGATIVO"


# Tipo ENUM compartido por ambos libros. Se crea a mano en la migración.
tipo_movimiento_pg = ENUM(
    TipoMovimientoEnum,
    name="tipo_movimiento_enum",
    create_type=False,
    values_callable=lambda e: [m.value for m in e],
)


def _fecha_registro() -> datetime:
    return Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True),
    )


class Producto(SQLModel, table=True):
    __tablename__ = "producto"  # type: ignore
    __table_args__ = (
        CheckConstraint("precio_base >= 0", name="precio_base_no_negativo"),
        CheckConstraint("stock_minimo >= 0", name="stock_minimo_no_negativo"),
        CheckConstraint("stock_cantidad >= 0", name="stock_cantidad_no_negativo"),
    )

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre: str = Field(sa_type=String(200), index=True)
    descripcion: str | None = None
    imagen_url: str | None = Field(default=None, sa_type=String(500))
    precio_base: Decimal = Field(sa_type=Numeric(10, 2))
    disponible: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    stock_minimo: int = Field(default=0, sa_column_kwargs={"server_default": "0"})
    stock_cantidad: int | None = None  # caché de solo lectura de stock_real
    created_at: datetime = created_at_field()
    updated_at: datetime = updated_at_field()
    deleted_at: datetime | None = deleted_at_field()


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"  # type: ignore

    producto_id: int = Field(sa_column=Column(ForeignKey("producto.id", ondelete="CASCADE"), primary_key=True))
    cat_id: int = Field(sa_column=Column(ForeignKey("categoria.id", ondelete="RESTRICT"), primary_key=True))
    es_principal: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})


class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingrediente"  # type: ignore
    __table_args__ = (CheckConstraint("stock_minimo >= 0", name="stock_minimo_no_negativo"),)

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre: str = Field(sa_type=String(100), unique=True, index=True)
    es_alergeno: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})
    es_elaborado: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})
    stock_minimo: int = Field(default=0, sa_column_kwargs={"server_default": "0"})
    deleted_at: datetime | None = deleted_at_field()


class ProductoIngrediente(SQLModel, table=True):
    """Receta de venta (BOM nivel producto)."""

    __tablename__ = "producto_ingrediente"  # type: ignore
    __table_args__ = (CheckConstraint("cantidad_requerida > 0", name="cantidad_requerida_positiva"),)

    producto_id: int = Field(sa_column=Column(ForeignKey("producto.id", ondelete="CASCADE"), primary_key=True))
    ingrediente_id: int = Field(sa_column=Column(ForeignKey("ingrediente.id", ondelete="RESTRICT"), primary_key=True))
    cantidad_requerida: Decimal = Field(
        default=Decimal("1"), sa_type=Numeric(10, 3), sa_column_kwargs={"server_default": "1"}
    )
    unidad_medida: str = Field(default="UN", sa_type=String(10), sa_column_kwargs={"server_default": "UN"})
    es_removible: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})


class RecetaIngrediente(SQLModel, table=True):
    """Receta de un ingrediente elaborado (BOM recursiva entre insumos)."""

    __tablename__ = "receta_ingrediente"  # type: ignore
    __table_args__ = (
        CheckConstraint("cantidad_requerida > 0", name="cantidad_requerida_positiva"),
        CheckConstraint("ingrediente_padre_id <> componente_id", name="padre_distinto_componente"),
    )

    ingrediente_padre_id: int = Field(
        sa_column=Column(ForeignKey("ingrediente.id", ondelete="CASCADE"), primary_key=True)
    )
    componente_id: int = Field(sa_column=Column(ForeignKey("ingrediente.id", ondelete="RESTRICT"), primary_key=True))
    cantidad_requerida: Decimal = Field(sa_type=Numeric(10, 3))
    unidad_medida: str = Field(default="UN", sa_type=String(10), sa_column_kwargs={"server_default": "UN"})


class Lote(SQLModel, table=True):
    __tablename__ = "lote"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    producto_id: int = Field(
        sa_column=Column(ForeignKey("producto.id", ondelete="RESTRICT"), nullable=False, index=True)
    )
    codigo_lote: str = Field(sa_type=String(50))
    fecha_vencimiento: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    fecha_ingreso: datetime = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()),
    )
    cantidad_inicial: Decimal = Field(sa_type=Numeric(12, 3))


class MovimientoStock(SQLModel, table=True):
    """Libro de movimientos del PRODUCTO terminado. Solo se agregan filas."""

    __tablename__ = "movimiento_stock"  # type: ignore
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="cantidad_positiva"),
        # A lo sumo un origen (pedido u orden). Ambos nulos = movimiento manual.
        CheckConstraint("num_nonnulls(pedido_id, orden_produccion_id) <= 1", name="origen_xor"),
    )

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    producto_id: int = Field(
        sa_column=Column(ForeignKey("producto.id", ondelete="CASCADE"), nullable=False, index=True)
    )
    lote_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("lote.id", ondelete="RESTRICT"), nullable=True),
    )
    pedido_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("pedido.id", ondelete="RESTRICT"), nullable=True),
    )
    orden_produccion_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("orden_produccion.id", ondelete="RESTRICT"), nullable=True),
    )
    tipo_movimiento: TipoMovimientoEnum = Field(sa_column=Column(tipo_movimiento_pg, nullable=False))
    cantidad: Decimal = Field(sa_type=Numeric(12, 3))
    motivo: str | None = Field(default=None, sa_type=String(120))
    fecha_registro: datetime = _fecha_registro()


class MovimientoIngrediente(SQLModel, table=True):
    """Libro de movimientos de INSUMOS. Solo se agregan filas."""

    __tablename__ = "movimiento_ingrediente"  # type: ignore
    __table_args__ = (CheckConstraint("cantidad > 0", name="cantidad_positiva"),)

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    ingrediente_id: int = Field(
        sa_column=Column(ForeignKey("ingrediente.id", ondelete="CASCADE"), nullable=False, index=True)
    )
    orden_produccion_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("orden_produccion.id", ondelete="RESTRICT"), nullable=True),
    )
    tipo_movimiento: TipoMovimientoEnum = Field(sa_column=Column(tipo_movimiento_pg, nullable=False))
    cantidad: Decimal = Field(sa_type=Numeric(12, 3))
    motivo: str | None = Field(default=None, sa_type=String(120))
    fecha_registro: datetime = _fecha_registro()
