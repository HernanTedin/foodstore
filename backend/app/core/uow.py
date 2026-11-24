from types import TracebackType
from typing import Self

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from app.core.database import SessionFactory


class UnitOfWork:
    session: Session

    def __init__(self, session_factory: sessionmaker[Session] = SessionFactory):
        self._session_factory = session_factory

    def _init_repositories(self) -> None:
        """Las subclases crean acá sus repositorios con self.session."""

    def __enter__(self) -> Self:
        self.session = self._session_factory()
        self._init_repositories()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
