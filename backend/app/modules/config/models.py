from datetime import datetime, time
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Double,
    Numeric,
    SmallInteger,
    String,
    Time,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field, timestamptz_field


class ConfiguracionLocal(SQLModel, table=True):
    """Registro único: zona horaria y punto de origen para el cálculo de distancia."""

    __tablename__ = "configuracion_local"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre: str = Field(sa_type=String(120))
    zona_horaria: str = Field(sa_type=String(60))
    direccion_origen: str | None = None
    lat_origen: float | None = Field(default=None, sa_type=Double)
    lng_origen: float | None = Field(default=None, sa_type=Double)


class HorarioOperativo(SQLModel, table=True):
    """Admite varias franjas por día. dia_semana: 0 = lunes … 6 = domingo."""

    __tablename__ = "horario_operativo"  # type: ignore
    __table_args__ = (CheckConstraint("dia_semana BETWEEN 0 AND 6", name="dia_semana_valido"),)

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    dia_semana: int = Field(sa_type=SmallInteger)
    hora_apertura: time = Field(sa_type=Time)
    hora_cierre: time = Field(sa_type=Time)
    activo: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})


class DiaBloqueado(SQLModel, table=True):
    """Feriados y cierres totales (todo_el_dia) o parciales (hora_desde/hasta)."""

    __tablename__ = "dia_bloqueado"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    fecha: datetime = timestamptz_field(nullable=False)
    motivo: str | None = Field(default=None, sa_type=String(120))
    todo_el_dia: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    hora_desde: time | None = Field(default=None, sa_type=Time)
    hora_hasta: time | None = Field(default=None, sa_type=Time)


class ZonaCobertura(SQLModel, table=True):
    """Zona de entrega con tarifa propia. poligono: lista de [lat, lng] en JSONB."""

    __tablename__ = "zona_cobertura"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    nombre: str = Field(sa_type=String(120))
    poligono: Any = Field(sa_column=Column(JSONB, nullable=False))
    tarifa_base: Decimal = Field(default=Decimal("0"), sa_type=Numeric(10, 2), sa_column_kwargs={"server_default": "0"})
    tarifa_por_km: Decimal = Field(
        default=Decimal("0"), sa_type=Numeric(10, 2), sa_column_kwargs={"server_default": "0"}
    )
    pedido_minimo: Decimal = Field(
        default=Decimal("0"), sa_type=Numeric(10, 2), sa_column_kwargs={"server_default": "0"}
    )
    activo: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    created_at: datetime = created_at_field()
