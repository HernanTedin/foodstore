import type { RolCodigo } from "@/shared/types/api";

/** Usuario tal como lo ve el administrador. */
export interface UsuarioAdmin {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  telefono: string | null;
  disabled: boolean;
  roles: RolCodigo[];
  created_at: string;
  deleted_at: string | null;
}

export type EstadoListado = "activos" | "inactivos" | "todos";

export interface UsuariosFiltros {
  page: number;
  size: number;
  search: string;
  rol: string;
  estado: EstadoListado;
}
