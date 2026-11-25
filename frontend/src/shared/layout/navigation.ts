import type { RolCodigo } from "@/shared/types/api";

export interface NavItem {
  label: string;
  to: string;
  roles: RolCodigo[];
  disponible: boolean;
}

export const ROL_NOMBRE: Record<RolCodigo, string> = {
  ADMIN: "Administrador",
  STOCK: "Gestor de stock",
  PEDIDOS: "Gestor de pedidos",
  CLIENT: "Cliente",
};

/** Menú lateral. Cada ítem se muestra solo a los roles indicados. */
export const NAV: NavItem[] = [
  {
    label: "Inicio",
    to: "/",
    roles: ["ADMIN", "STOCK", "PEDIDOS", "CLIENT"],
    disponible: true,
  },
  { label: "Catálogo", to: "/catalogo", roles: ["CLIENT"], disponible: false },
  {
    label: "Mis pedidos",
    to: "/mis-pedidos",
    roles: ["CLIENT"],
    disponible: false,
  },
  {
    label: "Pedidos",
    to: "/pedidos",
    roles: ["ADMIN", "PEDIDOS"],
    disponible: false,
  },
  {
    label: "Inventario",
    to: "/inventario",
    roles: ["ADMIN", "STOCK"],
    disponible: false,
  },
  { label: "Usuarios", to: "/Usuarios", roles: ["ADMIN"], disponible: false },
  {
    label: "Configuración",
    to: "/configuracion",
    roles: ["ADMIN"],
    disponible: false,
  },
  {
    label: "Direcciones",
    to: "/direcciones",
    roles: ["CLIENT"],
    disponible: true,
  },
];
