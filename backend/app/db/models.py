"""Importa todos los modelos para registrarlos en SQLModel.metadata.

Lo usan Alembic (autogenerate) y el seed. No agregar lógica acá.
"""

from app.modules.auth.models import RefreshToken
from app.modules.categorias.models import Categoria
from app.modules.config.models import (
    ConfiguracionLocal,
    DiaBloqueado,
    HorarioOperativo,
    ZonaCobertura,
)
from app.modules.direcciones.models import DireccionEntrega
from app.modules.pagos.models import FormaPago, Pago
from app.modules.pedidos.models import (
    DetallePedido,
    DetallePedidoExclusion,
    EstadoPedido,
    HistorialEstadoPedido,
    Pedido,
)
from app.modules.produccion.models import EstadoOrdenEnum, OrdenProduccion
from app.modules.productos.models import (
    Ingrediente,
    Lote,
    MovimientoIngrediente,
    MovimientoStock,
    Producto,
    ProductoCategoria,
    ProductoIngrediente,
    RecetaIngrediente,
    TipoMovimientoEnum,
)
from app.modules.usuarios.models import Rol, Usuario, UsuarioRol

__all__ = [
    "Categoria",
    "ConfiguracionLocal",
    "DetallePedido",
    "DetallePedidoExclusion",
    "DiaBloqueado",
    "DireccionEntrega",
    "EstadoOrdenEnum",
    "EstadoPedido",
    "FormaPago",
    "HistorialEstadoPedido",
    "HorarioOperativo",
    "Ingrediente",
    "Lote",
    "MovimientoIngrediente",
    "MovimientoStock",
    "OrdenProduccion",
    "Pago",
    "Pedido",
    "Producto",
    "ProductoCategoria",
    "ProductoIngrediente",
    "RecetaIngrediente",
    "RefreshToken",
    "Rol",
    "TipoMovimientoEnum",
    "Usuario",
    "UsuarioRol",
    "ZonaCobertura",
]
