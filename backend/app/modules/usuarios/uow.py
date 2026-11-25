from app.core.uow import UnitOfWork
from app.modules.usuarios.repository import RolRepository, UsuarioRepository


class UsuariosUnitOfWork(UnitOfWork):
    usuarios: UsuarioRepository
    roles: RolRepository

    def _init_repositories(self) -> None:
        self.usuarios = UsuarioRepository(self.session)
        self.roles = RolRepository(self.session)
