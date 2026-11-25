from sqlmodel import col

from app.core.repository import BaseRepository
from app.modules.direcciones.models import DireccionEntrega


class DireccionRepository(BaseRepository[DireccionEntrega]):
    model = DireccionEntrega

    def listar_de_usuario(self, usuario_id: int) -> list[DireccionEntrega]:
        """Las direcciones activas del usuario, la principal primero."""
        return list(
            self.list(
                [DireccionEntrega.usuario_id == usuario_id],  # type: ignore
                order_by=[col(DireccionEntrega.es_principal).desc(), DireccionEntrega.id],
            )
        )

    def get_propia(self, direccion_id: int, usuario_id: int) -> DireccionEntrega | None:
        """Devuelve la dirección solo si es del usuario y no está dada de baja."""
        direccion = self.get_by_id(direccion_id)
        if direccion is None or direccion.usuario_id != usuario_id or direccion.deleted_at is not None:
            return None
        return direccion

    def quitar_principal(self, usuario_id: int) -> None:
        """Deja al usuario sin dirección principal (antes de marcar otra)."""
        for d in self.listar_de_usuario(usuario_id):
            if d.es_principal:
                self.update(d, {"es_principal": False})
