from datetime import datetime

from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field, deleted_at_field


class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    parent_id: int | None = Field(
        default=None,
        sa_column=Column(ForeignKey("categoria.id", ondelete="RESTRICT"), nullable=True, index=True),
    )
    nombre: str = Field(sa_type=String(100), index=True)
    descripcion: str | None = None
    created_at: datetime = created_at_field()
    deleted_at: datetime | None = deleted_at_field()
