from datetime import UTC, datetime

from sqlmodel import select, update

from app.core.repository import BaseRepository
from app.modules.auth.models import RefreshToken


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken

    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return self.session.exec(stmt).first()

    def revocar(self, token: RefreshToken) -> None:
        self.update(token, {"revoked_at": datetime.now(UTC)})

    def revocar_todos(self, usuario_id: int) -> None:
        """Cierra todas las sesiones del usuario (por ejemplo, al cambiar la contraseña)."""
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.usuario_id == usuario_id)  # type: ignore[arg-type]
            .where(RefreshToken.revoked_at.is_(None))  # type: ignore[union-attr]
            .values(revoked_at=datetime.now(UTC))
        )
        self.session.exec(stmt)  # type: ignore[call-overload]
