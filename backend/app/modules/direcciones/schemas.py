from datetime import datetime

from pydantic import BaseModel, Field


class DireccionBase(BaseModel):
    alias: str | None = Field(default=None, max_length=50)
    linea1: str = Field(min_length=1, max_length=200)
    linea2: str | None = Field(default=None, max_length=200)
    ciudad: str | None = Field(default=None, max_length=100)
    provincia: str | None = Field(default=None, max_length=100)
    codigo_postal: str | None = Field(default=None, max_length=20)
    lat: float | None = Field(default=None, ge=-90, le=90)
    lng: float | None = Field(default=None, ge=-180, le=180)


class DireccionCreate(DireccionBase):
    es_principal: bool = False


class DireccionUpdate(DireccionBase):
    """Para editar. La principal se cambia con su propio endpoint."""


class DireccionRead(DireccionBase):
    id: int
    es_principal: bool
    created_at: datetime
