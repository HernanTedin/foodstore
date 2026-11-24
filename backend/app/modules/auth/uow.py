from app.core.uow import UnitOfWork
from app.modules.auth.repository import RefreshTokenRepository
from app.modules.usuarios.repository import RolRepository, UsuarioRepository


class AuthUnitOfWork(UnitOfWork):
    usuarios: UsuarioRepository
    roles: RolRepository
    refresh_tokens: RefreshTokenRepository

    def _init_repositories(self) -> None:
        self.usuarios = UsuarioRepository(self.session)
        self.roles = RolRepository(self.session)
        self.refresh_tokens = RefreshTokenRepository(self.session)
