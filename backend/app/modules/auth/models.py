from datetime import datetime

from sqlalchemy import CHAR, BigInteger, Column, DateTime, ForeignKey
from sqlmodel import Field, SQLModel

from app.core.database import created_at_field


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_token"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, sa_type=BigInteger)
    usuario_id: int = Field(sa_column=Column(ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True))
    token_hash: str = Field(sa_type=CHAR(64), unique=True, index=True)
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    revoked_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = created_at_field()
