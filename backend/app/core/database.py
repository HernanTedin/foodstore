from collections.abc import Iterator
from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Session, SQLModel, create_engine

from app.core.config import settings

# Nombres estables para las constraints (pk_, fk_, uq_, ck_, ix_).
# Sirve para que las migraciones de Alembic sean predecibles.
SQLModel.metadata.naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 5},
)

SessionFactory = sessionmaker(bind=engine, class_=Session, autoflush=False, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    with SessionFactory() as session:
        yield session


def created_at_field(index: bool = False) -> datetime:
    return Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=index),
    )


def updated_at_field() -> datetime:
    return Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )


def deleted_at_field() -> datetime | None:
    return Field(default=None, sa_column=Column(DateTime(timezone=True), index=True))


def timestamptz_field(nullable: bool = True, index: bool = False) -> datetime:
    return Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=nullable, index=index))
