from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from sqlalchemy import ColumnElement, func
from sqlmodel import Session, SQLModel, select

from app.core.schemas import PageParams

ModelT = TypeVar("ModelT", bound=SQLModel)


class _ReadRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: Session):
        self.session = session

    @property
    def _soft_deletable(self) -> bool:
        return hasattr(self.model, "deleted_at")

    def _base_filters(self, incluir_inactivos: bool) -> list[ColumnElement[bool]]:
        if self._soft_deletable and not incluir_inactivos:
            return [self.model.deleted_at.is_(None)]  # type: ignore[attr-defined]
        return []

    def get_by_id(self, id_: Any) -> ModelT | None:
        return self.session.get(self.model, id_)

    def list(
        self,
        filtros: Sequence[ColumnElement[bool]] = (),
        params: PageParams | None = None,
        incluir_inactivos: bool = False,
        order_by: Sequence[Any] = (),
    ) -> Sequence[ModelT]:
        stmt = select(self.model).where(*self._base_filters(incluir_inactivos), *filtros)
        if order_by:
            stmt = stmt.order_by(*order_by)
        if params:
            stmt = stmt.offset(params.offset).limit(params.size)
        return self.session.exec(stmt).all()

    def count(self, filtros: Sequence[ColumnElement[bool]] = (), incluir_inactivos: bool = False) -> int:
        stmt = select(func.count()).select_from(self.model).where(*self._base_filters(incluir_inactivos), *filtros)
        return self.session.exec(stmt).one()

    def create(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        self.session.flush()  # asigna el id sin confirmar la transacción
        self.session.refresh(entity)
        return entity


class BaseRepository(_ReadRepository[ModelT]):
    def update(self, entity: ModelT, data: dict[str, Any]) -> ModelT:
        for campo, valor in data.items():
            setattr(entity, campo, valor)
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def soft_delete(self, entity: ModelT) -> ModelT:
        if not self._soft_deletable:
            raise TypeError(f"{self.model.__name__} no admite baja lógica")
        return self.update(entity, {"deleted_at": datetime.now(UTC)})

    def restore(self, entity: ModelT) -> ModelT:
        return self.update(entity, {"deleted_at": None})

    def hard_delete(self, entity: ModelT) -> None:
        if self._soft_deletable:
            raise TypeError(f"{self.model.__name__} solo admite baja lógica (RN-16)")
        self.session.delete(entity)
        self.session.flush()


class AppendOnlyRepository(_ReadRepository[ModelT]):
    """Ledgers e historial: solo INSERT. No expone update ni delete (RN-03, RN-06)."""
