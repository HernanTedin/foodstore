export type RolCodigo = "ADMIN" | "STOCK" | "PEDIDOS" | "CLIENT";

export interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  telefono: string | null;
  roles: RolCodigo[];
}

/** Formato estándar de error de la API: { detail, code, field }. */
export interface ApiError {
  detail: string;
  code: string;
  field: string | null;
}
