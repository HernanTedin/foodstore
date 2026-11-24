"""Datos iniciales. Uso:  python -m app.db.seed

Es idempotente: busca cada registro por su código antes de insertarlo,
así que se puede correr todas las veces que haga falta.
"""

from datetime import time
from decimal import Decimal

from sqlmodel import Session, select

import app.db.models  # noqa: F401  (registra todos los modelos)
from app.core.database import SessionFactory
from app.core.security import hash_password
from app.modules.config.models import (
    ConfiguracionLocal,
    HorarioOperativo,
    ZonaCobertura,
)
from app.modules.pagos.models import FormaPago
from app.modules.pedidos.models import EstadoPedido
from app.modules.usuarios.models import Rol, Usuario, UsuarioRol

ROLES = [
    ("ADMIN", "Administrador", "Acceso total"),
    ("STOCK", "Gestor de stock", "Inventario, lotes y órdenes de producción"),
    ("PEDIDOS", "Gestor de pedidos", "Pagos y estados de CONFIRMADO a ENTREGADO"),
    ("CLIENT", "Cliente", "Catálogo, carrito, sus direcciones y sus pedidos"),
]

# (código, descripción, orden, es_terminal)
ESTADOS_PEDIDO = [
    ("PENDIENTE", "Pedido creado, pago pendiente", 1, False),
    ("CONFIRMADO", "Pago registrado", 2, False),
    ("EN_PREPARACION", "En cocina", 3, False),
    ("EN_CAMINO", "Despachado o listo para retirar", 4, False),
    ("ENTREGADO", "Entrega confirmada", 5, True),
    ("CANCELADO", "Pedido cancelado", 6, True),
]

# (código, nombre, habilitado)
FORMAS_PAGO = [
    ("EFECTIVO", "Efectivo", True),
    ("TRANSFERENCIA", "Transferencia bancaria", True),
    ("MERCADOPAGO", "MercadoPago", False),  # se habilita si se hace el bonus
]

ADMIN_EMAIL = "admin@foodstore.com"
ADMIN_PASSWORD = "FoodStore2026!"  # cambiar en producción

# Local de ejemplo: centro de Mendoza. Se puede editar desde el panel más adelante.
LOCAL = {
    "nombre": "Food Store Centro",
    "zona_horaria": "America/Argentina/Buenos_Aires",
    "direccion_origen": "Av. San Martín 1000, Mendoza",
    "lat_origen": -32.8895,
    "lng_origen": -68.8458,
}

# Polígono [lat, lng] que rodea el centro (aprox. 3 km por lado).
ZONA_CENTRO = [
    [-32.8700, -68.8700],
    [-32.8700, -68.8200],
    [-32.9100, -68.8200],
    [-32.9100, -68.8700],
]


def _crear_si_no_existe(session: Session, modelo: type, codigo: str, **valores: object) -> None:
    """Inserta un registro de catálogo solo si su código todavía no existe."""
    if session.get(modelo, codigo) is None:
        session.add(modelo(codigo=codigo, **valores))


def seed_catalogos(session: Session) -> None:
    for codigo, nombre, descripcion in ROLES:
        _crear_si_no_existe(session, Rol, codigo, nombre=nombre, descripcion=descripcion)
    for codigo, descripcion, orden, terminal in ESTADOS_PEDIDO:
        _crear_si_no_existe(
            session,
            EstadoPedido,
            codigo,
            descripcion=descripcion,
            orden=orden,
            es_terminal=terminal,
        )
    for codigo, nombre, habilitado in FORMAS_PAGO:
        _crear_si_no_existe(session, FormaPago, codigo, nombre=nombre, habilitado=habilitado)
    session.flush()


def seed_admin(session: Session) -> None:
    admin = session.exec(select(Usuario).where(Usuario.email == ADMIN_EMAIL)).first()
    if admin is None:
        admin = Usuario(
            nombre="Admin",
            apellido="Food Store",
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
        )
        session.add(admin)
        session.flush()
    if "ADMIN" not in admin.codigos_rol:
        session.add(UsuarioRol(usuario_id=admin.id, rol_codigo="ADMIN"))  # type: ignore
        session.flush()


def seed_configuracion(session: Session) -> None:
    if session.exec(select(ConfiguracionLocal)).first() is None:
        session.add(ConfiguracionLocal(**LOCAL))
    if session.exec(select(HorarioOperativo)).first() is None:
        for dia in range(7):  # 0 = lunes … 6 = domingo
            session.add(HorarioOperativo(dia_semana=dia, hora_apertura=time(11), hora_cierre=time(15)))
            session.add(HorarioOperativo(dia_semana=dia, hora_apertura=time(19), hora_cierre=time(23, 59)))
    if session.exec(select(ZonaCobertura)).first() is None:
        session.add(
            ZonaCobertura(
                nombre="Centro",
                poligono=ZONA_CENTRO,
                tarifa_base=Decimal("1500.00"),
                tarifa_por_km=Decimal("400.00"),
                pedido_minimo=Decimal("8000.00"),
            )
        )


def run() -> None:
    with SessionFactory() as session, session.begin():
        seed_catalogos(session)
        seed_admin(session)
        seed_configuracion(session)
    print("Seed aplicado: roles, estados de pedido, formas de pago, admin y configuración del local.")


if __name__ == "__main__":
    run()
